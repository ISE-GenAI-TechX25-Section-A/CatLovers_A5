#!/usr/bin/env bash

docker build -t streamlit-app .

docker run -p 8080:8501 streamlit-app
