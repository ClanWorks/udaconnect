FROM python:3.9-alpine

WORKDIR .

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5070

COPY . .
CMD ["python", "main.py"]
