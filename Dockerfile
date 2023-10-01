FROM python:3.10.1
WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


# Expose the port that the application uses
EXPOSE 8000

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--lifespan=on", "--loop", "uvloop", "--http", "httptools", "--reload"]
# CMD uvicorn main:app --host 0.0.0.0 --port 8000 --lifespan=on --loop uvloop --http httptools --reload

