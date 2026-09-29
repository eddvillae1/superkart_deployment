# Slim Python 3.10 base for a lightweight frontend container
FROM python:3.10-slim

WORKDIR /app

# Install dependencies before copying app code for faster layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Streamlit application
COPY . .

# Streamlit defaults to port 8501
EXPOSE 8501

# Launch Streamlit bound to all interfaces so Codespace can forward the port
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
