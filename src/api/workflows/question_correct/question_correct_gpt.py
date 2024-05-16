from api.common.services.openai_api import OpenAIAPI
from openai import AzureOpenAI
import json, logging
import os


class GptQuestionCorrect:
    _gpt_utils: OpenAIAPI
    _openai_client: AzureOpenAI

    def __init__(self, client: AzureOpenAI) -> None:
        self._gpt_utils = OpenAIAPI()
        self._openai_client = client

    def get_question_correct(self, input_prompt:str, questions:str):
        logging.info(
            f"get_answer_correct_gpt input questions={questions}"
        )
        prompt, params, _ = self._gpt_utils.load_sys_prompt(
            os.path.join(
                os.sep.join(__file__.split(os.sep)[:-1]),
                "prompts",
                "question_correct.json",
            )
        )
        if len(input_prompt)<=5:
            input_prompt = prompt
        output = self._gpt_utils.call_api(
            system_msg=input_prompt,
            user_msg=questions,
            params=params,
            is_json=True,
            client=self._openai_client,
        )
        json_answer = json.loads(str(output))
        logging.info(f"get_answers_correct_gpt output correct_answer={json_answer['correctas']}")
        return json_answer['correctas']
    
    def get_question_correct_eval(self, prompt_improving:str):
        logging.info(
            f"get_answer_correct_gpt input prompt={prompt_improving}"
        )
        prompt, params, _ = self._gpt_utils.load_sys_prompt(
            os.path.join(
                os.sep.join(__file__.split(os.sep)[:-1]),
                "prompts",
                "question_correct_eval.json",
            )
        )
        output = self._gpt_utils.call_api(
            system_msg=prompt,
            user_msg=prompt_improving,
            params=params,
            is_json=False,
            client=self._openai_client,
        )
        answer = str(output)
        return answer