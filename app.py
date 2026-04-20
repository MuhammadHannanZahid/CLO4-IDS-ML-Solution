import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

st.set_page_config(page_title="SecureNet IDS Dashboard", layout="wide")

@st.cache_resource
def load_models():
    model = joblib.load('rf_model.pkl')
    scaler = joblib.load('scaler.pkl')
    le = joblib.load('label_encoder.pkl')
    return model, scaler, le

try:
    rf_model, scaler, label_encoder = load_models()
    models_loaded = True
except FileNotFoundError:
    models_loaded = False

if 'shared_df' not in st.session_state:
    st.session_state['shared_df'] = None

def handle_upload(uploaded_file):
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            st.session_state['shared_df'] = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.parquet'):
            st.session_state['shared_df'] = pd.read_parquet(uploaded_file)

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Data Explorer", "Predictions"])

if page == "Dashboard":
    st.title("Machine Learning Dashboard")
    st.markdown("### Intrusion Detection System Overview")
    
    if models_loaded:
        col1, col2, col3 = st.columns(3)
        col1.metric("Active Model", "Random Forest", "Optimal Performance")
        col2.metric("Dataset Format", "CIC-IDS2017", "Parquet Engine")
        
        if st.session_state['shared_df'] is not None:
            col3.metric("Data Status", "Loaded in Memory", "Ready for Prediction")
        else:
            col3.metric("Data Status", "Waiting for Upload", "-")
        
        st.divider()
        
        col_graph1, col_graph2 = st.columns(2)
        
        with col_graph1:
            st.subheader("Top Feature Importances")
            st.write("What the AI considers most important for detecting threats:")
            importances = rf_model.feature_importances_
            indices = np.argsort(importances)[::-1][:10]
            
            fig1, ax1 = plt.subplots(figsize=(6, 4))
            sns.barplot(x=importances[indices], y=[f"Feature {i}" for i in indices], palette="viridis", ax=ax1)
            ax1.set_xlabel("Importance Score")
            ax1.set_ylabel("Network Feature Index")
            st.pyplot(fig1)
            
        with col_graph2:
            st.subheader("Current Data Memory Status")
            if st.session_state['shared_df'] is not None:
                df_status = st.session_state['shared_df']
                if 'Label' in df_status.columns:
                    st.write("Distribution of traffic currently loaded in memory:")
                    fig2, ax2 = plt.subplots(figsize=(6, 4))
                    sns.countplot(y=df_status['Label'], palette="magma", ax=ax2)
                    ax2.set_xlabel("Traffic Count")
                    ax2.set_ylabel("Traffic Label")
                    st.pyplot(fig2)
                else:
                    st.info("Loaded data does not contain a 'Label' column to plot.")
            else:
                st.info("No data loaded yet. Head over to the Data Explorer to initialize the memory!")
                
    else:
        st.error("Model files not found. Please run the Jupyter Notebook first.")

elif page == "Data Explorer":
    st.title("Data Explorer")
    
    uploaded_file = st.file_uploader("Upload Network Traffic File (Updates System-Wide)", type=["csv", "parquet"])
    handle_upload(uploaded_file)
            
    if st.session_state['shared_df'] is not None:
        df = st.session_state['shared_df']
        st.success("Data loaded into global memory! (You can safely switch to Predictions now)")
        
        col1, col2 = st.columns(2)
        col1.write(f"**Total Rows:** {df.shape[0]:,}")
        col2.write(f"**Total Columns:** {df.shape[1]}")
        
        st.write("### Raw Network Traffic Logs")
        st.dataframe(df.head(50))
        
        if st.button("Clear System Memory"):
            st.session_state['shared_df'] = None
            st.rerun()

elif page == "Predictions":
    st.title("Batch Prediction & Visualizations")
    
    if not models_loaded:
        st.warning("Please train the model first.")
    else:
        uploaded_file = st.file_uploader("Upload File for Prediction (Updates System-Wide)", type=["csv", "parquet"])
        handle_upload(uploaded_file)
        
        if st.session_state['shared_df'] is not None:
            st.success("Drawing data from global system memory.")
            df = st.session_state['shared_df'].copy() 
            
            df.columns = df.columns.str.strip()
            df.replace([np.inf, -np.inf], np.nan, inplace=True)
            df.dropna(inplace=True)
            
            if 'Label' in df.columns:
                X_batch = df.drop('Label', axis=1)
                y_true = df['Label']
                
                X_scaled = scaler.transform(X_batch)
                predictions = rf_model.predict(X_scaled)
                pred_labels = label_encoder.inverse_transform(predictions)
                
                st.write("### Prediction Engine Output")
                results_df = X_batch.copy()
                results_df.insert(0, 'Predicted Label', pred_labels)
                results_df.insert(1, 'True Label', y_true)
                st.dataframe(results_df.head(20))
                
                st.divider()
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("### Confusion Matrix")
                    y_true_encoded = label_encoder.transform(y_true)
                    cm = confusion_matrix(y_true_encoded, predictions)
                    fig3, ax3 = plt.subplots(figsize=(5, 4))
                    sns.heatmap(cm, annot=True, fmt='d', cmap='Reds', ax=ax3, 
                                xticklabels=label_encoder.classes_, 
                                yticklabels=label_encoder.classes_)
                    plt.xticks(rotation=45)
                    st.pyplot(fig3)
                    
                with col2:
                    st.write("### Threats Detected Overview")
                    fig4, ax4 = plt.subplots(figsize=(5, 4))
                    sns.countplot(x=pred_labels, palette="Set1", ax=ax4)
                    plt.xticks(rotation=45)
                    ax4.set_xlabel("Predicted Class")
                    st.pyplot(fig4)
                
                if st.button("Clear System Memory"):
                    st.session_state['shared_df'] = None
                    st.rerun()
            else:
                st.error("Uploaded file must contain the 'Label' column to evaluate predictions.")