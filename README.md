# 🛡️ AI-Powered Intrusion Detection: Augmenting NIDS with Machine Learning

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine_Learning-orange?style=for-the-badge&logo=scikit-learn)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit)
![Security](https://img.shields.io/badge/InfoSec-CLO_4-success?style=for-the-badge)

## Objective
The primary objective of this project is to explore the viability of Machine Learning (ML) as a tool to augment traditional Network Intrusion Detection Systems (NIDS). 

Traditional firewalls and NIDS often rely on static, signature-based rules. While essential, they are **reactive** and struggle against novel or high-volume attacks. By developing a proof-of-concept **Random Forest classification model**, this solution automatically categorizes network traffic as either benign or malicious. Specifically targeting **Distributed Denial of Service (DDoS)** attacks, this ML-driven approach enhances the network's **proactive** defense mechanisms, identifying complex threat patterns before they cause server downtime.

---

## Architectural & Design Choices

To build a robust security tool, several options were evaluated. Below are the definitive reasons why specific datasets, algorithms, and data structures were chosen over the alternatives.

### 1. Dataset Selection
| Available Options | Pros / Cons | Why This Approach Was Chosen |
| :--- | :--- | :--- |
| **KDD Cup 99 / NSL-KDD** | Heavily researched, but severely outdated (1990s traffic). | **Rejected:** Does not reflect modern web threats. |
| **UNSW-NB15** | Good modern attack variety, but smaller feature set. | **Rejected:** Lacks the extensive dimensionality needed for web server defense. |
| **CIC-IDS2017** | Highly realistic background traffic; over 80 extracted features; focuses on modern web threats. | **Selected:** Perfectly simulates real-world DoS/DDoS attacks against enterprise web servers, fitting our exact operational scenario. |

### 2. Algorithm Selection
| Available Options | Pros / Cons | Why This Approach Was Chosen |
| :--- | :--- | :--- |
| **Support Vector Machines (SVM)** | Good for high margins, but highly computationally expensive on large network datasets. | **Rejected:** Too slow for training on massive packet logs. |
| **Neural Networks (Deep Learning)** | Exceptional accuracy, but functions as a "black box" requiring massive data to avoid overfitting. | **Rejected:** Overly complex for tabular data and lacks easy interpretability. |
| **Random Forest Classifier** | Handles high-dimensional, non-linear data effortlessly. Provides built-in "Feature Importance." | **Selected:** Chosen for its high accuracy on tabular data, resistance to overfitting, and ability to tell us *exactly which network features* triggered the alarm. |

### 3. Data Storage Selection
| Available Options | Pros / Cons | Why This Approach Was Chosen |
| :--- | :--- | :--- |
| **Standard CSV** | Universal readability, but massive file sizes and very slow read/write speeds. | **Rejected:** Inefficient for processing millions of network traffic rows. |
| **Apache Parquet** | Columnar storage format; heavily compressed; incredibly fast to load into Pandas. | **Selected:** Chosen to drastically reduce memory overhead and ensure the interactive dashboard loads massive log files instantly. |

---

## Dataset Setup Instructions

This project utilizes the **CIC-IDS2017** dataset, specifically optimized using the Parquet file format. 

1. Ensure you have the required CIC-IDS2017 `.parquet` data files (e.g., `Benign-Monday-no-metadata.parquet` and `DDoS-Friday-no-metadata.parquet`).
2. Create a directory named `data/` at the root of this project repository.
3. Place your Parquet files inside the `data/` directory.
> **Note:** Ensure the dataset contains the `Label` column, as this is mandatory for the model to evaluate and predict traffic classifications.

---

## How to Run the Code

**1. Environment Setup**
Create and activate a Python virtual environment to prevent dependency conflicts:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```
**2. Install Dependencies**

```bash
pip install pandas numpy scikit-learn matplotlib seaborn streamlit joblib pyarrow
```

**3. Train the Model**

Run the Jupyter Notebook `IDS_Solution.ipynb` sequentially. This will:

* Clean and preprocess the raw network data.
* Train the Random Forest security model.
* Generate the required model artifacts (`rf_model.pkl`, `scaler.pkl`, `label_encoder.pkl`) needed for the dashboard.

**4. Launch the Security Dashboard**
Execute the following command in your terminal to boot up the interactive UI:
```bash
streamlit run app.py
```

## Brief Summary of Results
The Random Forest classifier achieved exceptional performance in distinguishing benign background traffic from malicious DDoS attacks.

Most importantly, the model successfully prioritized recall, significantly minimizing false negatives. In an enterprise security environment, a false negative is catastrophic, as it allows a real threat to bypass the NIDS undetected. The deployed Streamlit dashboard successfully provides a real-time, visual interface for security analysts to conduct batch traffic prediction, evaluate the confusion matrix, and audit feature importance dynamically.
