FROM python:3.11

RUN pip3 install fastapi uvicorn[standard] python-multipart

WORKDIR /usr/src/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]