#Events functions
import gradio as gr
from server.sql_utils import SQL_Utils
from domain.entities import topic, section, summary

class Events():
    
    def __init__(self, work_flow_utils) -> None:
        self.global_subject =""
        self.global_topic =""
        self.sql_utils = SQL_Utils()
        
        self.topic_table = self.sql_utils.select_table(topic.Topic)
        self.section_table = self.sql_utils.select_table(section.Section)
        self.summaries_table = self.sql_utils.select_table(summary.Summary)
        
        self.work_flow_utils = work_flow_utils

    #Seleccion de Tema
    def subject_change(self, rs):
        
        subject_id = [x.subject_id for x in self.work_flow_utils.subjects_table if x.subject_name == rs]
        self.global_subject=rs
        
        self.work_flow_utils.global_subject_id = subject_id[0]
        topic_dropped_list = [x.topic_name for x in self.topic_table if x.subject_id == subject_id[0]]
        
        
        # System refresh
        self.work_flow_utils.global_content = ""
        self.work_flow_utils.global_preguntas_message = ""
        self.work_flow_utils.global_correctas_message = ""
        self.work_flow_utils.global_incorrectas_message = ""
        
        return gr.update(choices=topic_dropped_list, value=None)

    def topic_change(self,rs):
        if rs:
            self.global_topic = rs
            content = ""
            
            try:
                topic_id = [x.topic_id for x in self.topic_table if x.topic_name == rs]
                sections_ids_list = [x.section_id for x in self.section_table if x.topic_id == topic_id[0]]
                sections_ids_list.sort()
                for sec_id in sections_ids_list:
                    content = content +str([x.summary for x in self.summaries_table if x.section_id == sec_id][0])+"\n\n"
            except:
                content = "seleccione una Asignatura primero"
                
            self.work_flow_utils.global_content = content
            return gr.update(value=content)
        else:
            return gr.update(value="seleccione un Temario")
        
    def summary_change(self, content):
        self.work_flow_utils.global_content = content
        

    #Seleccion de prompt  
    def upload_drop_preguntas_prompt(self,subject):
        try:
            return self.work_flow_utils.load_specialized_prompts_list(subject, "test_preguntas")
        except:
            return ["selecciona una Asignatura"]

    def upload_drop_correctas_prompt(self,subject):
        try:
            return self.work_flow_utils.load_specialized_prompts_list(subject, "test_correctas")
        except:
            return ["selecciona una Asignatura"]

    def upload_drop_incorrectas_prompt(self,subject):
        try:
            return self.work_flow_utils.load_specialized_prompts_list(subject, "test_incorrectas")
        except:
            return ["selecciona una Asignatura"]


    def load_prompt(self,prompt_id):
        try:
            return gr.update(value=[x.system_message for x in self.work_flow_utils.prompts_table if x.prompt_id == prompt_id][0])
        except:
            return gr.update(value="Carga un prompt")
    
    
    #Instanciar prompt y Guardar prompts
    #
    def init_preguntas_prompt(self, message):
        self.work_flow_utils.global_questions =[]
        self.work_flow_utils.global_preguntas_message = message
    
    def save_preguntas_prompt(self,name, description):
        return self.work_flow_utils.guardar_prompt(name, description, category="test_preguntas")#, self.work_flow_utils.load_specialized_prompts_list(self.global_subject,"test_preguntas")
    
    #
    def init_correctas_prompt(self, message):
        self.work_flow_utils.global_correctas =[]
        self.work_flow_utils.global_correctas_message = message
    
    def save_correctas_prompt(self,name, description):
        return self.work_flow_utils.guardar_prompt(name, description, category="test_correctas")
    
    #
    def init_incorrectas_prompt(self, message):
        self.work_flow_utils.global_incorrect =[]
        self.work_flow_utils.global_incorrectas_message = message
    
    def save_incorrectas_prompt(self,name, description):
        return self.work_flow_utils.guardar_prompt(name, description, category="test_incorrectas")
    
    def refresh_drop_preguntas(self):
        return self.upload_drop_preguntas_prompt(self.global_subject)
    
    def refresh_drop_correctas(self):
        return self.upload_drop_correctas_prompt(self.global_subject)
    
    def refresh_drop_incorrectas(self):
        return self.upload_drop_incorrectas_prompt(self.global_subject)