from api.common.services.openai_api import OpenAIAPI
from openai import AzureOpenAI
import json, logging, os


class GptTest:
    _gpt_utils: OpenAIAPI
    _openai_client: AzureOpenAI

    def __init__(self, client: AzureOpenAI) -> None:
        self._gpt_utils = OpenAIAPI()
        self._openai_client = client

    def get_text_test(self, content:str, input_prompt:str, msg=[]):
        logging.info(
            f"get_test_gpt input question={content}, prompt={input_prompt}"
        )
        
        prompt, params, _ = self._gpt_utils.load_sys_prompt(
            os.path.join(
                os.sep.join(__file__.split(os.sep)[:-1]),
                "prompts",
                "generate_test.json",
            )
        )
        
        last_msg: list[dict[str, str]] = []
        for i in msg[-4:]:
            last_msg.append({"role": "user", "content": i["Alumno"]})
            last_msg.append({"role": "assistant", "content": i["Profesor"]})
        
        if len(input_prompt)<=5:
            input_prompt = prompt
        output = self._gpt_utils.call_api(
            system_msg=input_prompt,
            user_msg=content,
            params=params,
            examples=last_msg,
            is_json=True,
            client=self._openai_client,
        )
        
        json_answer = json.loads(str(output))
        
        return json_answer
    
    def get_question_eval(self, prompt_improving:list, msg=[]):
        logging.info(
            f"get_answer_correct_gpt input prompt={prompt_improving}"
        )
        
        prompt, params, _ = self._gpt_utils.load_sys_prompt(
            os.path.join(
                os.sep.join(__file__.split(os.sep)[:-1]),
                "prompts",
                "generate_test_eval.json",
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