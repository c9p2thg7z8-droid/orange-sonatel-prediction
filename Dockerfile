FROM python:3.12-slim

WORKDIR /app

# Installer les deps en premier (cache Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir fastapi uvicorn scikit-learn==1.6.1 pandas python-multipart requests

# Copier le code ensuite
COPY . .

EXPOSE 7860

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "7860"]
