FROM python:3.12-slim

ENV APP_HOME=/app
ENV PORT=8000

ENV PYTHONUNBUFFERED=True \
    PORT=8000 \
    WORKERS=1 \
    API_NAME=api-auth \
    API_TAG_NAME=authentification

WORKDIR $APP_HOME

RUN apt-get update -qq \
    && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . ./

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
