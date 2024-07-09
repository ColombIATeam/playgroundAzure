import json, logging, os
from langchain_openai import ChatOpenAI


class GptQuestionIncorrect:

    def __init__(self) -> None:
        self.model = ChatOpenAI(
            model="gpt-4-turbo",
            temperature=0.95,
            max_tokens=4096,
            timeout=None,
            max_retries=2,
        )

    async def get_prompt_incorrect(self, input_prompt:str, questions:str, attempt = 0):
        
        if attempt >4:
            return print("El prompt no genera el formato esperado en get_prompt_incorrect")
        
        logging.info(
            f"get_question_incorrect_gpt input question={questions}"
        )
        
        if len(input_prompt) <= 5:
            prompt_path = os.path.join(  
                os.sep.join(__file__.split(os.sep)[:-1]),  
                "prompts",  
                "question_incorrect.json",  
            )  
            
            with open(prompt_path, 'r') as file:  
                prompt_data = json.load(file)  
                prompt_text = prompt_data.get("systemPrompt")  
                input_prompt = prompt_text
                
            
        message = [("system", input_prompt),("human", questions)]
  
        try:
            response = await self.model.ainvoke(message)
            result= response.content.replace("```","").replace("json","",1)
            
            return json.loads(result)['incorrectas']
        except Exception as e:
            print(e)
            return await self.get_prompt_incorrect(questions=questions, input_prompt=input_prompt,attempt = attempt+1)    
    
    async def get_prompt_incorrect_eval(self, prompt_improving:str, msg=[]):
        logging.info(
            f"get_question_incorrect_gpt input prompt_improving={prompt_improving}"
        )
        
        prompt_path = os.path.join(  
            os.sep.join(__file__.split(os.sep)[:-1]),  
            "prompts",  
            "question_incorrect_eval.json",  
        )  
            
        with open(prompt_path, 'r') as file:  
            prompt_data = json.load(file)  
            prompt_text = prompt_data.get("systemPrompt")  
            prompt = prompt_text
          
        message = [("system", prompt),("human", prompt_improving)]    
        
        response = await self.model.ainvoke(message)
        result= response.content
            
        return result  