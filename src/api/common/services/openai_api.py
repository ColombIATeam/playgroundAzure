import json
import logging
import time
from typing import Any

from openai import AzureOpenAI, Stream
from openai.types.chat import ChatCompletion

from api.common.openai_params import OpenaiParams


class OpenAIAPI:
    def call_api(
        self,
        system_msg: str,
        client: AzureOpenAI,
        params: OpenaiParams,
        user_msg: str | None = None,
        examples: list[dict[str, str]] = [],
        is_json: bool = False,
        seed: int | None = None,
        stream: bool = False,
    ) -> str:
        logging.info(f"call_api input {system_msg=} {user_msg=}")
        wait_multiplier: int = 1
        while wait_multiplier < 10:
            logging.debug("call_api try", wait_multiplier)
            try:
                if stream:
                    result: Stream[str] | None = self.get_completion_stream(
                        params,
                        user_msg,
                        system_msg,
                        examples,
                        is_json=is_json,
                        seed=seed,
                        stream=stream,
                        client=client,
                    )
                    response: str = ""
                    if result is not None:
                        for i in result:
                            if i.choices[0].delta.content is not None:
                                response += i.choices[0].delta.content
                else:
                    response: str | None = self.get_completion(
                        params,
                        user_msg,
                        system_msg,
                        examples,
                        is_json=is_json,
                        seed=seed,
                        stream=stream,
                        client=client,
                    )

                logging.info(f"call_api output {response=}")
                return response

            except Exception as e:
                logging.error(e)
                time.sleep(10 * wait_multiplier)
                wait_multiplier += 1
        return ""

    def get_completion_stream(
        self,
        params: OpenaiParams,
        user_msg: str | None,
        system_msg: str,
        examples: list[dict[str, str]],
        seed: int | None,
        is_json: bool,
        stream: bool,
        client: AzureOpenAI,
    ) -> Stream[str] | None:
        logging.info(
            f"get_completion input {params=} {user_msg=} {system_msg=} {examples=} {seed=} {is_json=} {stream=}"
        )
        args: dict[str, Any] = {
            "messages": [{"role": "system", "content": system_msg}]
            + examples
            + [{"role": "user", "content": user_msg if user_msg is not None else ""}],
            "model": params.deployment_name,
            "temperature": params.temperature,
            "max_tokens": params.max_response_length,
            "top_p": params.top_probablities,
            "frequency_penalty": params.frequency_penalty,
            "presence_penalty": params.presence_penalty,
            "stop": params.stop_sequences,
        }
        if is_json:
            args["response_format"] = {"type": "json_object"}
        if seed:
            args["seed"] = seed
        args["stream"] = True
        return client.chat.completions.create(**args)

    def get_completion(
        self,
        params: OpenaiParams,
        user_msg: str | None,
        system_msg: str,
        examples: list[dict[str, str]],
        seed: int | None,
        is_json: bool,
        stream: bool,
        client: AzureOpenAI,
    ) -> str | None:
        logging.info(
            f"get_completion input {params=} {user_msg=} {system_msg=} {examples=} {seed=} {is_json=} {stream=}"
        )
        args: dict[str, Any] = {
            "messages": [{"role": "system", "content": system_msg}]
            + examples
            + [{"role": "user", "content": user_msg if user_msg is not None else ""}],
            "model": params.deployment_name,
            "temperature": params.temperature,
            "max_tokens": params.max_response_length,
            "top_p": params.top_probablities,
            "frequency_penalty": params.frequency_penalty,
            "presence_penalty": params.presence_penalty,
            "stop": params.stop_sequences,
        }
        if is_json:
            args["response_format"] = {"type": "json_object"}
        if seed:
            args["seed"] = seed
        chat_completion: ChatCompletion = client.chat.completions.create(**args)
        logging.info(f"get_completion output {chat_completion=}")
        return chat_completion.choices[0].message.content

    def load_sys_prompt(
        self, json_name: str
    ) -> tuple[str, OpenaiParams, list[dict[str, str]]]:
        logging.info(f"load_sys_prompt input {json_name=}")
        path = json_name
        with open(path, encoding="utf-8") as json_file:
            json_data = json.load(json_file)

        params = json_data["chatParameters"]
        prompt: str = json_data["systemPrompt"]
        examples = json_data["fewShotExamples"]
        examples_salida: list[dict[str, str]] = []
        examples_salida: list[dict[str, str]] = []
        for i in examples:
            examples_salida.append({"role": "user", "content": i["userInput"]})
            examples_salida.append(
                {"role": "assistant", "content": i["chatbotResponse"]}
            )

        params = OpenaiParams(
            deployment_name=params["deploymentName"],
            temperature=params["temperature"],
            max_response_length=params["maxResponseLength"],
            top_probablities=params["topProbablities"],
            stop_sequences=params["stopSequences"],
            frequency_penalty=params["frequencyPenalty"],
            presence_penalty=params["presencePenalty"],
            past_messages_to_include=params["pastMessagesToInclude"],
        )
        logging.info(f"load_sys_prompt output {prompt=} {params=} {examples_salida=}")
        return prompt, params, examples_salida
