from openai import AzureOpenAI
from sqlalchemy import Engine
from api.workflows.test_questions.test_gpt import GptTest
from api.workflows.test_questions.test_request import TestRequest
from api.workflows.test_questions.test_response import GenerarTestsResponse

class TestWorkflow:
    _database_engine: Engine
    _gpt_test: GptTest
    
    def __init__(self,
        eval_switch,
        database_engine: Engine,
        azure_openai_client: AzureOpenAI
        
    ) -> None:
        self._database_engine = database_engine
        self._gpt_test = GptTest(client=azure_openai_client)
        self.eval_switch = eval_switch
        
    def execute(self, request: TestRequest) -> GenerarTestsResponse:
        preguntas = self._gpt_test.get_text_test(request.text,request.prompt)
        if self.eval_switch:
            prompt_improving = self._gpt_test.get_question_eval(prompt_improving=request.prompt)
            return GenerarTestsResponse(test=preguntas['preguntas'], prompt_improving=prompt_improving)
        else:
            return GenerarTestsResponse(test=preguntas['preguntas'], prompt_improving="Evaluación de Prompt Desactivada")