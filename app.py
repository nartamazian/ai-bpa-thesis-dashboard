
import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv("data.csv")

st.set_page_config(page_title="DSS Dashboard", layout="wide")
st.title("📊 DSS Simulation Dashboard for Intelligent Automation")
st.markdown("#### Powered by AI Confidence, Fraud Detection & Business Rules")

# Sidebar Inputs
st.sidebar.header("🔍 Simulate a Claim Decision")
claim_id = st.sidebar.selectbox("Choose Claim ID", df["Claim ID"])
claim_row = df[df["Claim ID"] == claim_id].iloc[0]

# Show details
st.sidebar.markdown(f"**Region:** {claim_row['Region']}")
st.sidebar.markdown(f"**Fraud Score:** {claim_row['Fraud Score']}")
st.sidebar.markdown(f"**Prior Claims:** {claim_row['Prior Claims']}")
st.sidebar.markdown(f"**AI Confidence:** {claim_row['AI Confidence']}%")

# Decision Logic
fraud = claim_row['Fraud Score']
confidence = claim_row['AI Confidence']
prior = claim_row['Prior Claims']

if fraud < 0.2 and confidence > 85:
    decision = "✅ Auto-approved"
    color = "green"
    reason = "Low fraud risk and high AI confidence"
elif fraud < 0.35 and confidence > 60:
    decision = "⚠️ Flagged for Review"
    color = "orange"
    reason = "Moderate fraud risk or mid-level confidence"
else:
    decision = "🔺 Escalated to Manager"
    color = "red"
    reason = "High risk or insufficient AI trust"

# Main Columns
col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("🧠 System Decision")
    st.markdown(f"<h2 style='color:{color}'>{decision}</h2>", unsafe_allow_html=True)
    st.markdown(f"**Reason:** {reason}")

    st.markdown("#### Claim Scenario Overview")
    st.dataframe(claim_row.to_frame().T, use_container_width=True)

    st.markdown("#### 📘 Suggested Actions")
    if decision == "✅ Auto-approved":
        st.success("No action needed. Claim is processed.")
    elif decision == "⚠️ Flagged for Review":
        st.warning("Please review manually for verification.")
    else:
        st.error("Immediate attention required. Possible fraud or policy violation.")

with col2:
    st.subheader("📈 AI Confidence vs Fraud Score")
    fig = px.scatter(df, x="Fraud Score", y="AI Confidence", color="Region",
                     hover_data=["Claim ID", "Prior Claims"], height=400)
    st.plotly_chart(fig, use_container_width=True)

# Extra Insights
st.markdown("---")
st.subheader("📊 Regional Risk Heatmap")
region_counts = df.groupby(["Region"])[["Fraud Score"]].mean().reset_index()
fig2 = px.bar(region_counts, x="Region", y="Fraud Score", color="Region",
              title="Average Fraud Score per Region", height=300)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("🧾 **Developed for Thesis: 'Impact of AI on Business Process Automation' — Nare Tamazyan, 2025**")
