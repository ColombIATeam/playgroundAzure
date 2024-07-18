from langchain_openai import ChatOpenAI
import json, logging
import os

class GptQuestionCorrect:

    def __init__(self) -> None:
        self.model = ChatOpenAI(
            model="gpt-4-turbo",
            temperature=0.95,
            max_tokens=1024,
            timeout=None,
            max_retries=2,
        )

    async def get_question_correct(self, input_prompt:str, questions:str, attempt = 0):
        
        if attempt >4:
            return print("El prompt no genera el formato esperado en get_question_correct")
        
        logging.info(
            f"get_answer_correct_gpt input questions={questions}"
        )
        if len(input_prompt) <= 5:
            prompt_path = os.path.join(  
                os.sep.join(__file__.split(os.sep)[:-1]),  
                "prompts",  
                "question_correct.json",  
            )  
            
            with open(prompt_path, 'r') as file:  
                prompt_data = json.load(file)  
                prompt_text = prompt_data.get("systemPrompt")  
                input_prompt = prompt_text
        
            
        message = [("system", input_prompt),("human", questions)]    
        
        try:
            response = await self.model.ainvoke(message)
            result= response.content.replace("```","").replace("json","",1)
            
            return json.loads(result)['correctas']
        except Exception as e:
            print(e)
            return await self.get_question_correct(input_prompt=input_prompt, questions=questions, attempt=attempt+1)
        
    
    async def get_question_correct_eval(self, prompt_improving:str):
        logging.info(
            f"get_answer_correct_gpt input prompt={prompt_improving}"
        )
        
        
        prompt_path = os.path.join(  
            os.sep.join(__file__.split(os.sep)[:-1]),  
            "prompts",  
            "question_correct.json",  
        )  
            
        with open(prompt_path, 'r') as file:  
            prompt_data = json.load(file)  
            prompt_text = prompt_data.get("systemPrompt")  
            prompt = prompt_text
        
        
        message = [("system", prompt),("human", prompt_improving)]    
        
        response = await self.model.ainvoke(message)
        result= response.content
            
        return result