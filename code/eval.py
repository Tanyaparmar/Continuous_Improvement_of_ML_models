"""
Evaluate model performance
"""
import pickle
import json
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
import os
import mlflow

def eval_model():
    # Load test data
    print("Loading data and model...")
    test_data = np.load('./data/processed_test_data.npy')

    # Load trained model
    with open('./data/model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("done.")
    # Divide loaded data-set into data and labels
    labels = test_data[:, 0]
    data = test_data[:, 1:]

    # Run model on test data
    print("Running model on test data...")
    predictions = model.predict(data)
    print("done.")

    # Calculate metric scores
    print("Calculating metrics...")
    metrics = {'accuracy': accuracy_score(labels, predictions)}

    # Save metrics to json file
    with open('./metrics/eval.json', 'w') as f:
        json.dump(metrics, f)
    print("done.")

    with mlflow.start_run() as run:

        mlflow.log_artifact("version.txt")

        #track the accuracy of the model
        for metric in metrics:
            mlflow.log_metric(metric, metrics[metric])

        #model parameters
        params = { 'seed': 42, 'num_sample': 4000}

        #log model parameters
        for key in params:
            mlflow.log_param(key, params[key])

    mlflow.end_run()

if __name__ == '__main__':
    eval_model()
