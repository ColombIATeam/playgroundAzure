from api.workflows.question_correct.question_correct_gpt import GptQuestionCorrect
from api.workflows.question_correct.question_correct_request import ListQuestionCorrectRequest
from api.workflows.question_correct.question_correct_response import *
from openai import AzureOpenAI
from sqlalchemy import Engine
import logging


class QuestionCorrectWorkflow:
    _database_engine: Engine
    _gpt_question_correct: GptQuestionCorrect
    
    def __init__(
        self,
        eval_switch,
        database_engine: Engine,
        azure_openai_client: AzureOpenAI
    ) -> None:
        self._database_engine = database_engine
        self._gpt_question_correct = GptQuestionCorrect(client=azure_openai_client)
        self.eval_switch = eval_switch

    def execute(self, request:ListQuestionCorrectRequest) -> ListQuestionCorrectResponse:
        logging.info(f"Executing QuestionCorrectWorkflow request={request}")
        correct_answers = self._gpt_question_correct.get_question_correct(input_prompt=request.prompt_table,
                                                                          questions=str(request.Questions))
        if self.eval_switch:
            prompt_improving = self._gpt_question_correct.get_question_correct_eval(prompt_improving=request.prompt_table)
            logging.info(f"QuestionCorrectWorkflow output correct_answers={correct_answers}, prompt={prompt_improving}")
            return ListQuestionCorrectResponse(correct_answer_list=[QuestionCorrectResponse(enunciado=str(i['Enunciado']),
                                                                                            respuesta_correcta=str(i['Respuesta_correcta']),
                                                                                            razonamiento_correcto=str(i['razonamiento_correcto'])
                                                                                            ) for i in correct_answers], 
                                            prompt_improving=prompt_improving)
        else:
            return ListQuestionCorrectResponse(correct_answer_list=[QuestionCorrectResponse(enunciado=str(i['Enunciado']),
                                                                                            respuesta_correcta=str(i['Respuesta_correcta']),
                                                                                            razonamiento_correcto=str(i['razonamiento_correcto'])
                                                                                            ) for i in correct_answers], 
                                            prompt_improving="Evaluación de Prompt Desactivada")
        