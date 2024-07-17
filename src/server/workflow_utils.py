from api.workflows.test_questions.test_request import TestRequest 
from api.workflows.question_correct.question_correct_request import ListQuestionCorrectRequest, QuestionCorrectRequest
from api.workflows.question_incorrect.question_incorrect_request import ListQuestionIncorrectRequest, QuestionIncorrectRequest
from api.common.dependency_container import DependencyContainer
from domain.entities import subject, prompt, subject_prompt
from server.sql_utils import SQL_Utils
from typing import Optional, List
import pandas as pd
import gradio as gr


class Work_Flow():
    
    def __init__(self, ) -> None:
        self.dfs = [pd.DataFrame()]*4
        self.index = [[]]*4
        
        
        DC = DependencyContainer()
        DC.initialize()
        self.DC = DC
        self.sql_utils = SQL_Utils()
        
    async def init_subject_drop(self):
        table = await self.sql_utils.select_table(subject.Subject)
        #print("A" + table + "\n")
        return gr.update(choices=[(x.subject_name, x.subject_id) for x in table])
    

    def transform_preguntas_to_md(self,data):  
        md_output = ""  
        for item in data:  
            md_output += f"### {item.Enunciado}\n\nRazonamiento: {item.Razonamiento}\n\n"  
        return md_output 

    async def gen_preguntas(self, prompt_pregunta, vars):  
        vars['questions']['prompts'] = prompt_pregunta  
        if prompt_pregunta == "Carga un prompt":  
            return {"error": "seleccione/escriba un prompt"}, "", vars  
        elif not("json" in prompt_pregunta):  
            return {"error": "conflictos de formato"}, "", vars  
        if vars['content'] == "" or vars['content'] == "seleccione un Temario":  
            return {"error": "primero seleccione un Temario"}, "", vars  
        request = TestRequest(text=str(vars['content']), prompt=prompt_pregunta)  
        result = await self.DC.get_text_test_workflow(vars['questions']['switch']).execute(request)  
        vars['questions']['eval'] = result.prompt_improving  
        vars['questions']['result'] = result.test  
        return self.transform_preguntas_to_md(result.test), result.prompt_improving, vars 
    
    
    def transform_correctas_to_md(self,data):  
        md_output = ""  
        for item in data:  
            md_output += f"### {item.respuesta_correcta}\n\nRazonamiento: {item.razonamiento_correcto}\n\n"  
        return md_output

    async def gen_correctas(self, prompt_correcta, vars):
        vars['correct_answers']['prompts'] = prompt_correcta
        if prompt_correcta == "Carga un prompt":
            return {"error":"seleccione/escriba un prompt"}, "", vars
        elif not("json" in prompt_correcta):
            return {"error":"conflictos de formato"}, "", vars
        if vars['questions']['result'] == []:
            return {"error":"primero genere alguna preguntas"}, "", vars
        request=ListQuestionCorrectRequest(Questions=[QuestionCorrectRequest(Enunciado=i.Enunciado, 
                                                                             Razonamiento=i.Razonamiento
                                                                            ) for i in vars['questions']['result']],
                                           prompt_table=prompt_correcta)
        result= await self.DC.get_question_correct_workflow(vars['correct_answers']['switch']).execute(request)
        vars['correct_answers']['eval'] = result.prompt_improving
        vars['correct_answers']['result'] = result.correct_answer_list
        return self.transform_correctas_to_md(result.correct_answer_list), result.prompt_improving, vars
    
    
    def transform_incorrectas_to_md(self,data):  
        md_output = ""  
        for index, item in enumerate(data):  
            md_output += f"### Pregunta {index + 1}\n\n"  
            for key, value in item.incorrect_answers.items():  
                md_output += f"- **{value['Respuesta_incorrecta']}**:\n{value['Razonamiento_incorrecto']}\n"  
            md_output += "\n"  
        return md_output 

    async def gen_incorrectas(self, prompt_incorrecta, vars):
        vars['incorrect_answers']['prompts'] = prompt_incorrecta
        if prompt_incorrecta == "Carga un prompt":
            return {"error":"seleccione/escriba un prompt"}, "", vars
        elif not("json" in prompt_incorrecta):
            return {"error":"conflictos de formato"}, "", vars
        if vars['correct_answers']['result'] == []:
            return {"error":"primero genere preguntas y respuestas correctas"}, "", vars
        request = ListQuestionIncorrectRequest(Questions=[QuestionIncorrectRequest(Enunciado=i.enunciado,
                                                                                   Respuesta_correcta=i.respuesta_correcta,
                                                                                   razonamiento_correcto=i.razonamiento_correcto 
                                                                                  ) for i in vars['correct_answers']['result']], 
                                           prompt=prompt_incorrecta)
        result = await self.DC.get_question_incorrect_workflow(vars['incorrect_answers']['switch']).execute(request)
        vars['incorrect_answers']['eval'] = result.prompt_improving
        vars['incorrect_answers']['result'] = result.incorrect_answer_list
        return self.transform_incorrectas_to_md(result.incorrect_answer_list), result.prompt_improving, vars

    def save_record(self, vars):
        message_type = 0
        for k in range(4):
            if k == 0:
                if vars['questions']['result']:
                    from itertools import zip_longest  
                    for q,c,i in zip_longest(vars['questions']['result'], vars['correct_answers']['result'], vars['incorrect_answers']['result']):
                        row_data = {  
                            'index': 1 if len(self.index[k])==0 else self.index[k][-1]+1,
                            'Pregunta': q.Enunciado if q else None,  
                            'Respuesta correcta': c.respuesta_correcta if c else None,  
                            'Respuesta incorrecta 1': str(i.incorrect_answers['respuesta_1']['Respuesta_incorrecta']) if i else None,  
                            'Respuesta incorrecta 2': str(i.incorrect_answers['respuesta_2']['Respuesta_incorrecta']) if i else None,  
                            'Respuesta incorrecta 3': str(i.incorrect_answers['respuesta_3']['Respuesta_incorrecta']) if i else None, 
                        }  
                        self.dfs[k] = pd.concat([self.dfs[k], pd.DataFrame([row_data])])
                    self.index[k]=list(self.dfs[k]['index']) 
            if k == 1: 
                if vars['questions']['result']:
                    for q in vars['questions']['result']:  
                        row_data = {  
                            'index': 1 if len(self.index[k])==0 else self.index[k][-1]+1,  
                            'Pregunta': q.Enunciado if q else None,  
                            'Razonamiento pregunta': q.Razonamiento if q else None,  
                            'Prompt pregunta': vars['questions']['prompts'],  
                            'Mejoras del prompt': vars['questions']['eval']
                        }  
                        self.dfs[k] = pd.concat([self.dfs[k], pd.DataFrame([row_data])])  
                    self.index[k]=list(self.dfs[k]['index']) 
                    message_type = 1
            if k == 2:  
                if vars['correct_answers']['result'] and vars['questions']['result']:
                    for c in vars['correct_answers']['result']:  
                        row_data = {  
                            'index': 1 if len(self.index[k])==0 else self.index[k][-1]+1,  
                            'Pregunta': c.enunciado if c else None,  
                            'Respuesta correcta': c.respuesta_correcta if c else None,  
                            'Razonamiento respuesta correcta': str(c.razonamiento_correcto) if c else None,  
                            'Prompt respuesta correcta': vars['correct_answers']['prompts'] if c else None,  
                            'Mejoras del prompt': vars['correct_answers']['eval'] if c else None,
                        }  
                        self.dfs[k] = pd.concat([self.dfs[k], pd.DataFrame([row_data])])  
                    self.index[k]=list(self.dfs[k]['index']) 
                    message_type = 2 
            if k == 3:  
                if vars['correct_answers']['result'] and vars['incorrect_answers']['result'] and vars['questions']['result']:
                    for inc in vars['incorrect_answers']['result']:  
                        row_data = {  
                            'index': 1 if len(self.index[k])==0 else self.index[k][-1]+1,  
                            'Respuesta incorrecta 1': str(inc.incorrect_answers['respuesta_1']['Respuesta_incorrecta']) if inc else None,  
                            'Razonamiento respuesta incorrecta 1': str(inc.incorrect_answers['respuesta_1']['Razonamiento_incorrecto']) if inc else None,  
                            'Respuesta incorrecta 2': str(inc.incorrect_answers['respuesta_2']['Respuesta_incorrecta']) if inc else None,  
                            'Razonamiento respuesta correcta 2': str(inc.incorrect_answers['respuesta_2']['Razonamiento_incorrecto']) if inc else None,  
                            'Respuesta incorrecta 3': str(inc.incorrect_answers['respuesta_3']['Respuesta_incorrecta']) if inc else None,  
                            'Razonamiento respuesta correcta 3': str(inc.incorrect_answers['respuesta_3']['Razonamiento_incorrecto']) if inc else None,  
                            'Prompt respuesta incorrecta': vars['incorrect_answers']['prompts'] if c else None,  
                            'Mejoras del prompt': vars['incorrect_answers']['eval'] if c else None  
                        }  
                        self.dfs[k] = pd.concat([self.dfs[k], pd.DataFrame([row_data])])  
                    self.index[k]=list(self.dfs[k]['index']) 
                    message_type = 3
                    
        match message_type:   
            case 0:
                return  "No tienes objetos generados para guardar"
            case 1:
                return  "Preguntas guardadas"       
            case 2:
                return  "Preguntas y respuestas correctas guardadas"
            case 3:
                return  "Preguntas, respuestas correctas y respuestas incorrectas guardadas"  

    def export_table(self, file_name):
        if file_name == "":
            file_name= "export"
        
        with pd.ExcelWriter('docs/'+file_name+'.xlsx') as writer:
            try: 
                df1 = self.dfs[0].set_index('index', inplace=False); df1.index.name = None
                df1.to_excel(writer, sheet_name='Resumen')  
                df2 = self.dfs[1].set_index('index', inplace=False); df2.index.name = None
                df2.to_excel(writer, sheet_name='Preguntas')  
                df3 = self.dfs[2].set_index('index', inplace=False); df3.index.name = None
                df3.to_excel(writer, sheet_name='Respuestas correctas')  
                df4 = self.dfs[3].set_index('index', inplace=False); df4.index.name = None
                df4.to_excel(writer, sheet_name='Respuestas incorrectas')  
            except: 'Error:No se a podido guardar'
        return 'Archivo guardado con éxito.'

    async def load_specialized_prompts_list(self,subject_id, category):
        
        prompts_table = await self.sql_utils.select_table(prompt.Prompt)
        subject_prompt_table = await self.sql_utils.select_table(subject_prompt.Subject_Prompt)
        
        prompt_id = [x.prompt_id for x in subject_prompt_table if x.subject_id == subject_id]
        return gr.update(choices=[(x.name+" - "+ x.description, x.prompt_id ) for x in prompts_table if (x.prompt_id in prompt_id) and (x.category == category)])

    async def guardar_prompt(self,name, description, category,vars):
        with await self.sql_utils.sql_session() as session:
            match category:
                case "test_preguntas":
                    message = vars['questions']['prompts']
                case "test_correctas":
                    message = vars['correct_answers']['prompts']
                case "test_incorrectas":
                    message = vars['incorrect_answers']['prompts']
                case _:
                    return "No se pudo indentficar la categoria del porompt"
            if not(name) or not(description):
                return "Complete los campos antes de Guardar"
            if not("json" in message):
                return "Escoja/Redacte un prompt valido antes de Guardar"
            temp_1 = prompt.Prompt(name=name, description=description, system_message=message, 
                                category=category,llm_model_id=1,max_response_length=4096,
                                temperature=0.95,top_probabilities=0.95,frequency_penalty=0.4,
                                stream=0, stop_sequences=None, presence_penalty=0)
            await self.sql_utils.insert_data(temp_1,session)
            temp_id=temp_1.prompt_id
            temp_2 = subject_prompt.Subject_Prompt(subject_id=vars['subject_id'], prompt_id=temp_id)
            await self.sql_utils.insert_data(temp_2,session)
            session.close()
        
        return "Tu prompt se a guardado como {}, con id = {} y descripcion :\n {}".format(name,temp_id,description)
    
    def eval_update_preguntas(self,check_box, vars):
        vars['questions']['switch'] = check_box
        return vars
        
    def eval_update_correctas(self,check_box, vars):
        vars['correct_answers']['switch'] = check_box
        return vars
        
    def eval_update_incorrectas(self,check_box, vars):
        vars['incorrect_answers']['switch'] = check_box
        return vars