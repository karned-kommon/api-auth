FROM python:3.12-slim

ENV APP_HOME=/app
ENV PORT=8000

EXPOSE $PORT

WORKDIR $APP_HOME

RUN apt-get update -qq \
    && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY main.py ./

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]