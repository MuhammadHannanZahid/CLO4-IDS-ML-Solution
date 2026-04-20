"""# AI-Powered Intrusion Detection: Augmenting NIDS with Machine Learning

## Objective
The objective of this project is to explore the viability of Machine Learning as a tool to augment traditional Network Intrusion Detection Systems (NIDS). By developing a proof-of-concept Random Forest classification model, this solution automatically classifies network traffic as either benign or malicious, specifically targeting DDoS attacks, to enhance proactive defense mechanisms.

## Dataset Setup Instructions
This project utilizes the **CIC-IDS2017** dataset, specifically optimized using the Parquet file format. 
1. Place the required CIC-IDS2017 `.parquet` data files (e.g., `Benign-Monday-no-metadata.parquet` and `DDoS-Friday-no-metadata.parquet`) into a directory named `data/` at the root of the project.
2. Ensure the dataset contains the `Label` column for model evaluation.

## How to Run the Code
1. Create and activate a Python virtual environment.
2. Install the necessary dependencies: `pip install pandas numpy scikit-learn matplotlib seaborn streamlit joblib pyarrow`.
3. Run the Jupyter Notebook `IDS_Solution.ipynb` sequentially to preprocess the data, train the Random Forest model, and generate the required model artifacts (`rf_model.pkl`, `scaler.pkl`, `label_encoder.pkl`).
4. Launch the interactive dashboard by executing the following command in the terminal: `streamlit run app.py`.

## Brief Summary of Results
The Random Forest classifier achieved exceptional performance in distinguishing benign background traffic from malicious DDoS attacks. The model successfully prioritized recall, significantly minimizing false negatives, which is a critical security requirement to ensure threats do not bypass the NIDS undetected. The deployed dashboard provides a real-time interface for batch traffic prediction, confusion matrix evaluation, and feature importance visualization.
"""
