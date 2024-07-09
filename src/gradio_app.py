from server.workflow_utils import Work_Flow
work_flow_utils = Work_Flow()

from server.events import Events 
linked_events =Events(work_flow_utils)

from server.gradio_UI import UI
interfas = UI(work_flow_utils, linked_events)

interfas.run_UI()