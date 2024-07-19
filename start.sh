#!/bin/bash

cd src
uvicorn gradio_app:app --reload
