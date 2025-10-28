FROM python:3.10-slim
WORKDIR /app
RUN pip install gradio
RUN pip install requests
RUN pip install python-dotenv
COPY ./src/ui_main.py /app/
CMD ["python3", "ui_main.py"]
