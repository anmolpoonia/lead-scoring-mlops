FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Generate data and train model at build time (optional but convenient for demo)
RUN python generate_data.py && python train_model.py

EXPOSE 8000

CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
