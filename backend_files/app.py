# Flask application serving the SuperKart sales prediction pipeline
# Two endpoints: single-record JSON inference and batch CSV inference

import io
import joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify

# Initialize the Flask application with a descriptive name
superkart_api = Flask(__name__)

# Load the trained pipeline (preprocessor + Random Forest) once at startup
# Loading here rather than per-request keeps latency low during inference
model = joblib.load('superkart_model.joblib')


@superkart_api.post('/v1/predict')
def predict():
    """
    Online inference endpoint.
    Expects a JSON body with the 10 feature fields and returns a single prediction.
    """
    # Parse the incoming JSON into a one-row DataFrame matching the pipeline's input format
    data     = request.get_json()
    input_df = pd.DataFrame([data])

    # Pipeline preprocesses and predicts in one call
    prediction = model.predict(input_df)

    return jsonify({'prediction': round(float(prediction[0]), 2)})


@superkart_api.post('/v1/predictbatch')
def predict_batch():
    """
    Batch inference endpoint.
    Expects a CSV file uploaded as multipart form data under the key 'file'.
    Returns a JSON dict mapping row index to predicted sales value.
    """
    # Read the CSV file uploaded by the client
    file     = request.files['file']
    input_df = pd.read_csv(io.StringIO(file.read().decode('utf-8')))

    # Generate predictions for all rows in a single vectorized call
    predictions = model.predict(input_df)

    return jsonify({str(i): round(float(p), 2) for i, p in enumerate(predictions)})


if __name__ == '__main__':
    # Binding to 0.0.0.0 allows Docker to route external traffic to the container
    superkart_api.run(host='0.0.0.0', port=7860, debug=False)
