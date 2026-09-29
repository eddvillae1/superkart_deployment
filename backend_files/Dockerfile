# Use a slim Python 3.10 image to keep the container small and fast to build
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to take advantage of Docker's layer caching
# Only rebuilds the pip install step when requirements.txt changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app and the serialized model into the container
COPY . .

# Expose port 7860 so the Codespace can forward traffic to the Flask server
EXPOSE 7860

# Start the Flask API when the container launches
CMD ["python", "app.py"]
