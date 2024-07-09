from api.common.services.openai_api import OpenAIAPI
from openai import AzureOpenAI
import json, logging, os


class GptQuestionIncorrect:
    _gpt_utils: OpenAIAPI
    _openai_client: AzureOpenAI

    def __init__(self, client: AzureOpenAI) -> None:
        self._gpt_utils = OpenAIAPI()
        self._openai_client = client

    def get_prompt_incorrect(self, input_prompt:str, questions:str):
        logging.info(
            f"get_question_incorrect_gpt input question={questions}"
        )
        prompt, params, _ = self._gpt_utils.load_sys_prompt(
            os.path.join(
                os.sep.join(__file__.split(os.sep)[:-1]),
                "prompts",
                "question_incorrect.json",
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
        logging.info(f"get_answer_incorrect_gpt output incorrect_answers={json_answer['incorrectas']}")
        return json_answer['incorrectas']
    
    def get_prompt_incorrect_eval(self, prompt_improving:str, msg=[]):
        logging.info(
            f"get_question_incorrect_gpt input prompt_improving={prompt_improving}"
        )
        prompt, params, _ = self._gpt_utils.load_sys_prompt(
            os.path.join(
                os.sep.join(__file__.split(os.sep)[:-1]),
                "prompts",
                "question_incorrect_eval.json",
            )
        )
        last_msg: list[dict[str, str]] = []
        for i in msg[-4:]:
            last_msg.append({"role": "user", "content": i["Alumno"]})
            last_msg.append({"role": "assistant", "content": i["Profesor"]})
        output = self._gpt_utils.call_api(
            system_msg=prompt,
            user_msg=prompt_improving,
            params=params,
            examples=last_msg,
            is_json=False,
            client=self._openai_client,
        )
        answer = str(output)
        return answer