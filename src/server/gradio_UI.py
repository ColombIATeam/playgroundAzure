import gradio as gr
import os

class UI():
    
    def __init__(self, work_flow_utils, linked_events) -> None:
        
        self.work_flow_utils = work_flow_utils
        self.linked_events = linked_events
        
        self.subjects_dropped_list = [x.subject_name for x in self.work_flow_utils.subjects_table]

        ### Cargar prompts ###

        #Preguntas
        self.preguntas_prompt_box = gr.Textbox(lines=1, label="Prompt para generar preguntas del Temario", value="Carga un prompt", interactive=True, autoscroll=False, )

        self.preguntas_UI = gr.Interface(
            fn=self.work_flow_utils.gen_preguntas,
            inputs=[
                    self.preguntas_prompt_box,
                    ],
            
            outputs=[gr.JSON(value="{}",label="Preguntas generadas"),gr.Markdown(label="LLM tips")],
            
            allow_flagging="never",submit_btn="Generar",clear_btn="Limpiar",stop_btn=gr.Button("Interrumpir", variant="stop", visible=True))


        #Correctas
        self.correctas_prompt_box = gr.Textbox(lines=1, label="Prompt para generar respuestas correctas", value="Carga un prompt", interactive=True, autoscroll=False, )

        self.correctas_UI = gr.Interface(
            fn=self.work_flow_utils.gen_correctas,
            inputs=[
                    self.correctas_prompt_box,
                ],
                
                outputs=[gr.JSON(value="{}",label="Respuestas correctas"),gr.Markdown(label="LLM tips")],
                
                allow_flagging="never",submit_btn="Generar",clear_btn="Limpiar",stop_btn=gr.Button("Interrumpir", variant="stop", visible=True))

        #Incorrectas
        self.incorrectas_prompt_box = gr.Textbox(lines=1, label="Prompt para generar respuestas incorrectas", value="Carga un prompt", interactive=True, autoscroll=False, )

        self.incorrectas_UI = gr.Interface(
            fn=self.work_flow_utils.gen_incorrectas,
            inputs=[
                    self.incorrectas_prompt_box,
                    ],
            
            outputs=[gr.JSON(value="{}",label="Respuestas incorrectas"),gr.Markdown(label="LLM tips")],
            
            allow_flagging="never",submit_btn="Generar",clear_btn="Limpiar",stop_btn=gr.Button("Interrumpir", variant="stop", visible=True))

        ### Guardar prompts ### 
        
        self.save_preguntas_message = gr.Markdown()
        self.save_preguntas_button = gr.Button("Guardar",interactive=True,)
        self.guardar_preguntas_UI = gr.Interface(
            fn=self.linked_events.save_preguntas_prompt,
            inputs=[
                    gr.Textbox(lines=1, label="Nombre del prompt", interactive=True, ),
                    gr.Textbox(lines=1, label="Descripción del prompt", interactive=True, ),
                    ],
            
            outputs=self.save_preguntas_message,allow_flagging="never",
                            submit_btn=self.save_preguntas_button,clear_btn="Limpiar")

        self.save_correctas_message = gr.Markdown()
        self.guardar_correctas_UI = gr.Interface(
            fn=self.linked_events.save_correctas_prompt,
            inputs=[
                    gr.Textbox(lines=1, label="Nombre del prompt", interactive=True, ),
                    gr.Textbox(lines=1, label="Descripción del prompt", interactive=True, ),
                    ],
            
            outputs=self.save_correctas_message,allow_flagging="never",
                            submit_btn="Guardar",clear_btn="Limpiar")

        self.save_incorrectas_message = gr.Markdown()
        self.guardar_incorrectas_UI = gr.Interface(
            fn=self.linked_events.save_incorrectas_prompt,
            inputs=[
                    gr.Textbox(lines=1, label="Nombre del prompt", interactive=True, ),
                    gr.Textbox(lines=1, label="Descripción del prompt", interactive=True, ),
                    ],
            
            outputs=self.save_incorrectas_message ,allow_flagging="never",
                            submit_btn="Guardar",clear_btn="Limpiar")
        
        self.image = gr.Image(os.path.join(os.sep.join(__file__.split(os.sep)[:-1]),"Diagrama.png",))
        self.recomendations = gr.Markdown("Recomendaciones: \n1. No modifique los FORMATOS (salida o entrada) de los prompts y Asegúrese de que contienen la palabra -json-. \n2. Al recargar o modificar un prompt el sistema le pedirá volver a generar ese paso. \n3. Los resultados generados no se guardan en el sistema, puede hacer una copia manual con botón en la esquina superior derecha de cada resultado.")
        self.diagrama = gr.Interface(
            fn=lambda :  [self.image,self.recomendations],
            inputs=[],
            outputs=[
                self.image,
                self.recomendations,
            ],
            allow_flagging="never",
            submit_btn=gr.Button("",visible=False, interactive=False),
            clear_btn=gr.Button("",visible=False, interactive=False),
            
        )
        
        self.manual = gr.Markdown(value="# Claridad y Precisión: \nEn los LLM (modelos de lenguaje de gran escala), es importante formular preguntas y comandos de forma clara y precisa para obtener las respuestas más adecuadas. Evita ambigüedades y especifica lo que necesitas saber.\n# Brevedad y Concisión: \nMantén tus prompts cortos y al grano. Información innecesaria puede confundir al modelo y llevar a respuestas menos precisas.\n# Relevancia: \nAsegúrate de que tu prompt esté directamente relacionado con la información que buscas. Preguntas irrelevantes pueden resultar en información que no es útil para tu propósito.\n# Proporcionar Contexto: \nSi tu pregunta depende de información específica o situacional, incluye ese contexto en tu prompt para guiar al LLM hacia la respuesta correcta.\n# Morfología: \nPresta atención al uso correcto de formas de palabras, como tiempos verbales y pluralidad, para evitar confusiones y garantizar que el LLM comprenda y responda correctamente.\n# Sintaxis: \nEstructura tus frases de manera lógica y gramaticalmente correcta para facilitar la comprensión por parte del LLM y obtener respuestas coherentes.\n# Programática: \nEn el contexto de los LLM se refiere a la capacidad de los modelos de lenguaje para interpretar y ejecutar comandos basados en instrucciones codificadas. En términos de pragmática, esto implica comprender cómo las instrucciones se aplican en diferentes contextos y cómo ciertos comandos pueden variar en significado dependiendo de la situación.")
        self.manual_UI = gr.Interface(
            fn=lambda :  self.manual,
            inputs=[],
            outputs=self.manual,
            allow_flagging="never",
            submit_btn=gr.Button("",visible=False, interactive=False),
            clear_btn=gr.Button("",visible=False, interactive=False),
            
        )

    def run_UI(self):
        with gr.Blocks(theme=gr.themes.Soft()) as demo:
            gr.Markdown("# Generador de preguntas de opción múltiple",)
            
            with gr.Row():
                with gr.Column(scale=2):
                    gr.TabbedInterface([self.diagrama, self.manual_UI], ["Uso", "Buenas practicas"])
                with gr.Column():
                    
                    drop_subject = gr.Dropdown(self.subjects_dropped_list, label="Asignatura", interactive=True,)
                    drop_topic = gr.Dropdown(["seleccione una Asignatura"], label="Temario", interactive=True,)
                    summary = gr.Textbox(lines=30, label="Resumen del Temario (por secciones)", interactive=True,)
                    
            
            
            with gr.Blocks():
                gr.Markdown("---\n# Generar preguntas del Temario\n En este paso generamos las preguntas con respecto al tema seleccionado. Un buen prompt guía de forma específica y clara hacia el tipo o estilo de preguntas deseadas, aprovechando el contexto y estableciendo parámetros precisos dentro del prompt.",)
                drop_preguntas_prompts = gr.Dropdown(["selecciona una Asignatura"], label="Cargar prompt para generar preguntas", interactive=True,)
                Evaluation_switch_preguntas = gr.Checkbox(value=True,label="Activar/Desactivar Evaluación de Prompt", interactive=True,)
                gr.TabbedInterface([self.preguntas_UI, self.guardar_preguntas_UI], ["Prompt editable", "Guardar prompt"])
                
                drop_subject.change(fn=self.linked_events.upload_drop_preguntas_prompt, inputs=[drop_subject], outputs=[drop_preguntas_prompts])
                drop_preguntas_prompts.change(fn=self.linked_events.load_prompt, inputs=[drop_preguntas_prompts], outputs=[self.preguntas_prompt_box])
                Evaluation_switch_preguntas .change(fn=self.work_flow_utils.eval_update_preguntas, inputs=[Evaluation_switch_preguntas ])
                
            
            with gr.Blocks():
                gr.Markdown("---\n# Generar respuestas correctas\n Al responder las preguntas generadas, un prompt efectivo produce respuestas claras y sin ambiguedades, manteniendo la consistencia en el lenguaje e información del contenido original, gracias a razonamientos que acompañan a cada pregunta.")
                drop_correctas_prompts = gr.Dropdown(["selecciona una Asignatura"], label="Cargar prompt para generar respuestas correctas", interactive=True,)
                Evaluation_switch_correctas = gr.Checkbox(value=True,label="Activar/Desactivar Evaluación de Prompt", interactive=True,)

                gr.TabbedInterface([self.correctas_UI, self.guardar_correctas_UI], ["Prompt editable", "Guardar prompt"])
                
                drop_subject.change(fn=self.linked_events.upload_drop_correctas_prompt, inputs=[drop_subject], outputs=[drop_correctas_prompts])
                drop_correctas_prompts.change(fn=self.linked_events.load_prompt, inputs=[drop_correctas_prompts], outputs=[self.correctas_prompt_box])
                Evaluation_switch_correctas .change(fn=self.work_flow_utils.eval_update_correctas, inputs=[Evaluation_switch_correctas ])
                
            with gr.Blocks():
                gr.Markdown("---\n# Generar respuestas incorrectas\n Al generar las opciones incorrectas un resultado óptimo se caracteriza por la creación de respuestas que deliberadamente se desvían de la exactitud, pero lo hacen de manera coherente y metódica. A pesar de que las respuestas no son correctas, estas mantienen claridad y evitan ambigüedades.")
                drop_incorrectas_prompts = gr.Dropdown(["selecciona una Asignatura"], label="Cargar prompt para generar respuestas incorrectas", interactive=True,)
                Evaluation_switch_incorrectas = gr.Checkbox(value=True,label="Activar/Desactivar Evaluación de Prompt", interactive=True,)
                gr.TabbedInterface([self.incorrectas_UI, self.guardar_incorrectas_UI], ["Prompt editable", "Guardar prompt"])
                
                drop_subject.change(fn=self.linked_events.upload_drop_incorrectas_prompt, inputs=[drop_subject], outputs=[drop_incorrectas_prompts])
                drop_incorrectas_prompts.change(fn=self.linked_events.load_prompt, inputs=[drop_incorrectas_prompts], outputs=[self.incorrectas_prompt_box])
                Evaluation_switch_correctas .change(fn=self.work_flow_utils.eval_update_incorrectas, inputs=[Evaluation_switch_incorrectas])
            
            """with gr.Blocks():
                gr.Markdown("---\n# Guardar/Exportar resultados en excel\nAsegurate de tener preguntas generadas del ultimo prompt editado")
                file_name = gr.Textbox(label="Nombre del archivo")
                with gr.Row():
                    with gr.Column():
                        results_check_point = gr.Button("Guardar resultados *")
                    with gr.Column():
                        export_results = gr.Button("Exportar resultados guardados")
                importing_message = gr.Markdown("# * ")"""
            
            drop_subject.change(fn=self.linked_events.subject_change, inputs=[drop_subject], outputs=[drop_topic])
            drop_topic.change(fn=self.linked_events.topic_change, inputs=[drop_topic], outputs=[summary])
            
            summary.change(fn=self.linked_events.summary_change, inputs=[summary])
            
            self.preguntas_prompt_box.change(fn=self.linked_events.init_preguntas_prompt, inputs=[self.preguntas_prompt_box])
            self.correctas_prompt_box.change(fn=self.linked_events.init_correctas_prompt, inputs=[self.correctas_prompt_box])
            self.incorrectas_prompt_box.change(fn=self.linked_events.init_incorrectas_prompt, inputs=[self.incorrectas_prompt_box])
            
            self.save_preguntas_message.change(fn=self.linked_events.refresh_drop_preguntas, outputs=[drop_preguntas_prompts])
            self.save_correctas_message.change(fn=self.linked_events.refresh_drop_correctas, outputs=[drop_correctas_prompts])
            self.save_incorrectas_message.change(fn=self.linked_events.refresh_drop_incorrectas, outputs=[drop_incorrectas_prompts])
            
            #results_check_point.click(fn=self.work_flow_utils.save_record, outputs=[importing_message])
            #export_results.click(fn=self.work_flow_utils.export_table, inputs=[file_name], outputs=[importing_message])
            
            
        return demo
        #demo.launch()