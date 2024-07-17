from api.workflows.question_incorrect.question_incorrect_gpt import GptQuestionIncorrect
from api.workflows.question_incorrect.question_incorrect_request import ListQuestionIncorrectRequest
from api.workflows.question_incorrect.question_incorrect_response import *
from openai import AzureOpenAI
from sqlalchemy import Engine
import logging


class QuestionIncorrectWorkflow:
    _database_engine: Engine
    _gpt_question_incorrect: GptQuestionIncorrect
    
    def __init__(
        self,
        eval_switch,
        database_engine: Engine,
        azure_openai_client: AzureOpenAI
    ) -> None:
        self._database_engine = database_engine
        self._gpt_question_incorrect = GptQuestionIncorrect(client=azure_openai_client)
        self.eval_switch = eval_switch

    def execute(self, request:ListQuestionIncorrectRequest) -> ListQuestionIncorrectResponse:
        logging.info(f"Executing QuestionIncorrectWorkflow request={request}")
        incorrect_answers = self._gpt_question_incorrect.get_prompt_incorrect(input_prompt=request.prompt,
                                                                              questions=str(request.Questions))
        if self.eval_switch:
            prompt_improving = self._gpt_question_incorrect.get_prompt_incorrect_eval(prompt_improving=request.prompt)
            logging.info(f"QuestionIncorrectWorkflow output incorrect_answers={incorrect_answers}, prompt_improving={prompt_improving}")
            return ListQuestionIncorrectResponse(incorrect_answer_list=[QuestionIncorrectResponse(incorrect_answers=i) for i in incorrect_answers], 
                                                prompt_improving=prompt_improving)
        else:
            return ListQuestionIncorrectResponse(incorrect_answer_list=[QuestionIncorrectResponse(incorrect_answers=i) for i in incorrect_answers], 
                                                prompt_improving="Evaluación de Prompt Desactivada")