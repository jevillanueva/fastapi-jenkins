FROM python:3.10-alpine

RUN apk update && apk add --no-cache python3-dev \
    gcc \
    libc-dev \
    libffi-dev
WORKDIR /app/
ADD . /app/
RUN pip install  --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "main:app", "--workers", "1", "--host", "0.0.0.0" ]