#Events functions
import gradio as gr
from server.sql_utils import SQL_Utils
from domain.entities import topic, section, summary, prompt

class Events():
    
    def __init__(self, work_flow_utils) -> None:
        self.sql_utils = SQL_Utils()
        
        self.work_flow_utils = work_flow_utils

    #Seleccion de Tema
    async def subject_change(self, subject_id, vars):
        
        topic_table =  await self.sql_utils.select_table(topic.Topic)
        topic_dropped_list = [x.topic_name for x in topic_table if x.subject_id == subject_id]
        
        
        # System refresh
        vars = {'content': "", 'subject_id': subject_id,
                'questions':{'prompts': "", 'result': [], 'eval': "", 'switch': vars['questions']['switch']},
                'correct_answers':{'prompts': "", 'result': [], 'eval': "", 'switch': vars['correct_answers']['switch']},
                'incorrect_answers':{'prompts': "", 'result': [], 'eval': "", 'switch': vars['incorrect_answers']['switch']}}
        
        return gr.update(choices=topic_dropped_list, value=None), vars

    async def topic_change(self,rs,vars):
        if rs:
            content = ""
            topic_table = await self.sql_utils.select_table(topic.Topic)
            section_table = await self.sql_utils.select_table(section.Section)
            summaries_table = await self.sql_utils.select_table(summary.Summary)
            try:
                topic_id = [x.topic_id for x in topic_table if x.topic_name == rs]
                sections_ids_list = [x.section_id for x in section_table if x.topic_id == topic_id[0]]
                sections_ids_list.sort()
                for sec_id in sections_ids_list:
                    content = content +str([x.summary for x in summaries_table if x.section_id == sec_id][0])+"\n\n"
            except:
                content = "seleccione una Asignatura primero"
                
            vars['content'] = content
            return gr.update(value=content), vars
        else:
            return gr.update(value="seleccione un Temario"), vars

    #Seleccion de prompt  
    async def upload_drop_preguntas_prompt(self,subject_id):
        try:
            return await self.work_flow_utils.load_specialized_prompts_list(subject_id, "test_preguntas")
        except:
            return ["selecciona una Asignatura"]

    async def upload_drop_correctas_prompt(self,subject_id):
        try:
            return await self.work_flow_utils.load_specialized_prompts_list(subject_id, "test_correctas")
        except:
            return ["selecciona una Asignatura"]

    async def upload_drop_incorrectas_prompt(self,subject_id):
        try:
            return await self.work_flow_utils.load_specialized_prompts_list(subject_id, "test_incorrectas")
        except:
            return ["selecciona una Asignatura"]


    async def load_prompt(self,prompt_id):
        try:
            prompts_table = await self.sql_utils.select_table(prompt.Prompt)
            return gr.update(value=[x.system_message for x in prompts_table if x.prompt_id == prompt_id][0])
        except:
            return gr.update(value="Carga un prompt")
    
    
    #Instanciar prompt y Guardar prompts
    #
    def save_preguntas_prompt(self,name, description,vars):
        return self.work_flow_utils.guardar_prompt(name, description, category="test_preguntas", vars=vars), vars
    
    #
    def save_correctas_prompt(self,name, description,vars):
        return self.work_flow_utils.guardar_prompt(name, description, category="test_correctas", vars=vars), vars
    
    #
    def save_incorrectas_prompt(self,name, description,vars):
        return self.work_flow_utils.guardar_prompt(name, description, category="test_incorrectas", vars=vars), vars
    
    
    
    def refresh_drop_preguntas(self, vars):
        return self.upload_drop_preguntas_prompt(vars['subject_id'])
    
    def refresh_drop_correctas(self, vars):
        return self.upload_drop_correctas_prompt(vars['subject_id'])
    
    def refresh_drop_incorrectas(self, vars):
        return self.upload_drop_incorrectas_prompt(vars['subject_id'])