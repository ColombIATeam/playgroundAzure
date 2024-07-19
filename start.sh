#!/bin/bash

cr src
uvicorn gradio_app:app --reload
