from fastapi import FastAPI
import gradio as gr

app = FastAPI()

from server.workflow_utils import Work_Flow
work_flow_utils = Work_Flow()
 
from server.events import Events#
linked_events =Events(work_flow_utils)
 
from server.gradio_UI import UI
interfas = UI(work_flow_utils, linked_events)
 
gr_app = interfas.run_UI()
app = gr.mount_gradio_app(app, gr_app, path="/gradio")
#interfas.run_UI()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)