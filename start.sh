#!/bin/bash

cd src
uvicorn gradio_app:app --host 0.0.0.0 --port 8000 --reload
