import streamlit as st
import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.processor import load_and_clean, get_summary

def render():
    st.markdown('<div class="sec-head">Screen 1 — Upload your transactions</div>', unsafe_allow_html=True)

    # API key input
    with st.expander("OpenAI API Key (required for AI narrative)", expanded=False):
        api_key = st.text_input(
            "Paste your OpenAI API key",
            type="password",
            placeholder="sk-...",
            help="Get a free key at platform.openai.com. Your key is never stored."
        )
        if api_key:
            st.session_state["api_key"] = api_key
            st.success("API key saved for this session.")

    st.markdown("""
    <div class="upload-zone">
        <div class="upload-title">Drop your UPI transaction CSV here</div>
        <div class="upload-sub">
            Export from GPay → Profile → Statements & Transactions → Download<br>
            or PhonePe → History → Download Statement
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Choose your CSV file",
        type=["csv"],
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="step-card">
            <div class="step-num">Step 1</div>
            <div class="step-title">Export your CSV</div>
            <div class="step-desc">Open GPay or PhonePe and download your transaction history as a CSV file</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="step-card">
            <div class="step-num">Step 2</div>
            <div class="step-title">Upload here</div>
            <div class="step-desc">Drop the file above. Your data never leaves your browser — fully private.</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="step-card">
            <div class="step-num">Step 3</div>
            <div class="step-title">Get your story</div>
            <div class="step-desc">AI analyses your spending and writes a personalised money narrative in seconds</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Load demo data button
    if st.button("Try with demo data (no upload needed) →"):
        demo_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "data", "demo_transactions.csv"
        )
        with open(demo_path, "rb") as f:
            df = load_and_clean(f)
        st.session_state["df"]      = df
        st.session_state["summary"] = get_summary(df)
        st.success(f"Demo data loaded! {len(df)} transactions ready. Switch to the Dashboard tab.")

    # Process uploaded file
    if uploaded:
        df = load_and_clean(uploaded)
        if df.empty:
            st.error("Could not parse this file. Please make sure it's a valid UPI CSV export.")
        else:
            st.session_state["df"]      = df
            st.session_state["summary"] = get_summary(df)
            st.success(f"Loaded {len(df)} transactions. Switch to the Dashboard tab to explore!")
            st.dataframe(
                df[["date","description","amount","category"]].head(10),
                use_container_width=True
            )
