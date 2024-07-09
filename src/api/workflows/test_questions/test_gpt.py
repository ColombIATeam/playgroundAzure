import json  
import logging  
import os  
from langchain_openai import ChatOpenAI
  
class GptTest:   
  
    def __init__(self) -> None:  
        self.model = ChatOpenAI(
            model="gpt-4-turbo",
            temperature=0.95,
            max_tokens=1024,
            timeout=None,
            max_retries=2,
        )
  
    async def get_text_test(self, content: str, input_prompt: str, attempt=0):  
        if attempt > 4:  
            print("El prompt no genera el formato esperado en get_text_test")  
            return  
        
        logging.info(f"get_text_test input question={content}, prompt={input_prompt}")  
        
        if len(input_prompt) <= 5:
            prompt_path = os.path.join(  
                os.sep.join(__file__.split(os.sep)[:-1]),  
                "prompts",  
                "generate_test.json",  
            )  
            
            with open(prompt_path, 'r') as file:  
                prompt_data = json.load(file)  
                prompt_text = prompt_data.get("systemPrompt")  
                input_prompt = prompt_text  
        
        message = [("system", input_prompt), ("human", content)]  
        
        try:  
            response = await self.model.ainvoke(message)  # Assuming self.model.invoke is an asynchronous function  
            result = response.content.replace("```", "").replace("json", "", 1)  
        
            return json.loads(result)  
        except Exception as e:  
            print(e)  
            return await self.get_text_test(content=content, input_prompt=input_prompt, attempt=attempt + 1)  

  
    async def get_question_eval(self, prompt_improving: list):  
        logging.info(f"get_question_eval input prompt={prompt_improving}")  
    
        prompt_path = os.path.join(  
            os.sep.join(__file__.split(os.sep)[:-1]),  
            "prompts",  
            "generate_test_eval.json",  
        )  
    
        with open(prompt_path, 'r') as file:  
            prompt_data = json.load(file)  
            prompt = prompt_data.get("systemPrompt")  
    
        message = [("system", prompt), ("human", prompt_improving)]  
    
        response = await self.model.ainvoke(message)  # Assuming self.model.invoke is an asynchronous function  
        return response.content  

