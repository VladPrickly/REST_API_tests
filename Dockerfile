FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /project

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r /project/requirements.txt

COPY . /project

CMD ["pytest", "-v"]

