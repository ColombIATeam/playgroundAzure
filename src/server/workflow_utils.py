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
        self.global_content: Optional[str] = ""
        self.global_questions = []
        self.global_correct = []
        self.global_incorrect = []
        self.prompts_improvings = ["", "", ""]
        self.prompts = ["", "", ""]
        self.eval_switch_preguntas = True
        self.eval_switch_correctas = True
        self.eval_switch_incorrectas = True

        self.global_subject_id: Optional[int] = None
        self.global_preguntas_message: Optional[str] = ""
        self.global_correctas_message: Optional[str] = ""
        self.global_incorrectas_message: Optional[str] = ""
        
        
        DC = DependencyContainer()
        DC.initialize()
        self.DC = DC
        self.sql_utils = SQL_Utils()
        self.subjects_table = self.sql_utils.select_table(subject.Subject)
        self.prompts_table = self.sql_utils.select_table(prompt.Prompt)
        self.subject_prompt_table = self.sql_utils.select_table(subject_prompt.Subject_Prompt)


    def gen_preguntas(self, prompt_pregunta):
        self.prompts[0] = prompt_pregunta
        if prompt_pregunta == "Carga un prompt":
            return {"error":"seleccione/escriba un prompt"}, ""
        elif not("json" in prompt_pregunta):
            return {"error":"conflictos de formato"}, ""
        if self.global_content == "" or self.global_content =="seleccione un Temario":
            return {"error":"primero seleccione un Temario"}, ""
        request = TestRequest(text=str(self.global_content), prompt=prompt_pregunta)
        result = self.DC.get_text_test_workflow(self.eval_switch_preguntas).execute(request)
        self.prompts_improvings[0] = result.prompt_improving
        self.global_questions = result.test
        return [i.Enunciado for i in result.test], result.prompt_improving

    def gen_correctas(self, prompt_correcta):
        self.prompts[1] = prompt_correcta
        if prompt_correcta == "Carga un prompt":
            return {"error":"seleccione/escriba un prompt"}, ""
        elif not("json" in prompt_correcta):
            return {"error":"conflictos de formato"}, ""
        if self.global_questions == []:
            return {"error":"primero genere alguna preguntas"}, ""
        request=ListQuestionCorrectRequest(Questions=[QuestionCorrectRequest(Enunciado=i.Enunciado, 
                                                                             Razonamiento=i.Razonamiento
                                                                            ) for i in self.global_questions],
                                           prompt_table=prompt_correcta)
        result=self.DC.get_question_correct_workflow(self.eval_switch_correctas).execute(request)
        self.prompts_improvings[1] = result.prompt_improving
        self.global_correct = result.correct_answer_list
        return [i.respuesta_correcta for i in result.correct_answer_list], result.prompt_improving

    def gen_incorrectas(self, prompt_incorrecta):
        self.prompts[2] = prompt_incorrecta
        if prompt_incorrecta == "Carga un prompt":
            return {"error":"seleccione/escriba un prompt"}, ""
        elif not("json" in prompt_incorrecta):
            return {"error":"conflictos de formato"}, ""
        if self.global_correct == []:
            return {"error":"primero genere preguntas y respuestas correctas"}, ""
        request = ListQuestionIncorrectRequest(Questions=[QuestionIncorrectRequest(Enunciado=i.enunciado,
                                                                                   Respuesta_correcta=i.respuesta_correcta,
                                                                                   razonamiento_correcto=i.razonamiento_correcto 
                                                                                  ) for i in self.global_correct], 
                                           prompt=prompt_incorrecta)
        result = self.DC.get_question_incorrect_workflow(self.eval_switch_correctas).execute(request)
        self.prompts_improvings[2] = result.prompt_improving
        self.global_incorrect = result.incorrect_answer_list
        return [i.incorrect_answers for i in result.incorrect_answer_list], result.prompt_improving

    def save_record(self):
        message_type = 0
        for k in range(4):
            if k == 0:
                if self.global_questions:
                    from itertools import zip_longest  
                    for q,c,i in zip_longest(self.global_questions, self.global_correct, self.global_incorrect):
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
                if self.global_questions:
                    for q in self.global_questions:  
                        row_data = {  
                            'index': 1 if len(self.index[k])==0 else self.index[k][-1]+1,  
                            'Pregunta': q.Enunciado if q else None,  
                            'Razonamiento pregunta': q.Razonamiento if q else None,  
                            'Prompt pregunta': self.prompts[0],  
                            'Mejoras del prompt': self.prompts_improvings[0]  
                        }  
                        self.dfs[k] = pd.concat([self.dfs[k], pd.DataFrame([row_data])])  
                    self.index[k]=list(self.dfs[k]['index']) 
                    message_type = 1
            if k == 2:  
                if self.global_correct and self.global_questions:
                    for c in self.global_correct:  
                        row_data = {  
                            'index': 1 if len(self.index[k])==0 else self.index[k][-1]+1,  
                            'Pregunta': c.enunciado if c else None,  
                            'Respuesta correcta': c.respuesta_correcta if c else None,  
                            'Razonamiento respuesta correcta': str(c.razonamiento_correcto) if c else None,  
                            'Prompt respuesta correcta': self.prompts[1] if c else None,  
                            'Mejoras del prompt': self.prompts_improvings[1] if c else None,
                        }  
                        self.dfs[k] = pd.concat([self.dfs[k], pd.DataFrame([row_data])])  
                    self.index[k]=list(self.dfs[k]['index']) 
                    message_type = 2 
            if k == 3:  
                if self.global_correct and self.global_incorrect and self.global_questions:
                    for inc in self.global_incorrect:  
                        row_data = {  
                            'index': 1 if len(self.index[k])==0 else self.index[k][-1]+1,  
                            'Respuesta incorrecta 1': str(inc.incorrect_answers['respuesta_1']['Respuesta_incorrecta']) if inc else None,  
                            'Razonamiento respuesta incorrecta 1': str(inc.incorrect_answers['respuesta_1']['Razonamiento_incorrecto']) if inc else None,  
                            'Respuesta incorrecta 2': str(inc.incorrect_answers['respuesta_2']['Respuesta_incorrecta']) if inc else None,  
                            'Razonamiento respuesta correcta 2': str(inc.incorrect_answers['respuesta_2']['Razonamiento_incorrecto']) if inc else None,  
                            'Respuesta incorrecta 3': str(inc.incorrect_answers['respuesta_3']['Respuesta_incorrecta']) if inc else None,  
                            'Razonamiento respuesta correcta 3': str(inc.incorrect_answers['respuesta_3']['Razonamiento_incorrecto']) if inc else None,  
                            'Prompt respuesta incorrecta': self.prompts[2] if c else None,  
                            'Mejoras del prompt': self.prompts_improvings[2] if c else None  
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

    def load_specialized_prompts_list(self,subject, category):
        subject_id = [x.subject_id for x in self.subjects_table if x.subject_name == subject]
        prompt_id = [x.prompt_id for x in self.subject_prompt_table if x.subject_id == subject_id[0]]
        return gr.update(choices=[(x.name+" - "+ x.description, x.prompt_id ) for x in self.prompts_table if (x.prompt_id in prompt_id) and (x.category == category)])

    def guardar_prompt(self,name, description, category,):
        with self.sql_utils.sql_session() as session:
            match category:
                case "test_preguntas":
                    message = self.global_preguntas_message
                case "test_correctas":
                    message = self.global_correctas_message
                case "test_incorrectas":
                    message = self.global_incorrectas_message
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
            self.sql_utils.insert_data(temp_1,session)
            temp_id=temp_1.prompt_id
            temp_2 = subject_prompt.Subject_Prompt(subject_id=self.global_subject_id, prompt_id=temp_id)
            self.sql_utils.insert_data(temp_2,session)
            session.close()
        self.prompts_table = self.sql_utils.select_table(prompt.Prompt)
        self.subject_prompt_table = self.sql_utils.select_table(subject_prompt.Subject_Prompt)
        return "Tu prompt se a guardado como {}, con id = {} y descripcion :\n {}".format(name,temp_id,description)
    
    def eval_update_preguntas(self,check_box):
        self.eval_switch_preguntas = check_box
        
    def eval_update_correctas(self,check_box):
        self.eval_switch_correctas = check_box
        
    def eval_update_incorrectas(self,check_box):
        self.eval_switch_incorrectas = check_box