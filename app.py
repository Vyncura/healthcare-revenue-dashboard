import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Revenue Integrity Dashboard", layout="wide")

st.title("🏥 Clinic Revenue Integrity Audit (Demo)")
st.write("Bridging healthcare billing data with automated analytics.")

# Mock Data
data = {
    'Payer': ['BlueCross', 'Aetna', 'UnitedHealth', 'Medicare', 'Cigna'],
    'Recoverable Leakage ($)': [35000, 15000, 40000, 5000, 25000]
}
df = pd.DataFrame(data)

# Create a bar chart
fig = px.bar(df, x='Payer', y='Recoverable Leakage ($)', title="Recoverable Leakage by Payer", color='Recoverable Leakage ($)')
st.plotly_chart(fig)

st.info("Support this project: Contributions help keep healthcare tools free and online 24/7.")
