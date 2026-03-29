import streamlit as st
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

FALLBACK_NARRATIVE = """
March was a food-heavy month. Nearly 4 in every 10 rupees went toward eating — mostly Swiggy, and mostly after 9pm on weekdays. Your Swiggy habit alone cost more than your entire transport budget.

The good news: your utility bills were all paid on time, and your shopping stayed controlled. Making bulk grocery orders instead of daily pickups shows real planning discipline.

The pattern worth watching: Fridays are your most expensive day by far. Weekend dinners and late-night rides home seem to be the culprit — something to keep in mind heading into April.
"""

FALLBACK_TIP = "Cutting just two late-night Swiggy orders per week could save you around ₹800/month — enough for a 13-month Netflix subscription."

def render():
    st.markdown('<div class="sec-head">Screen 3 — Your money story</div>', unsafe_allow_html=True)

    if "summary" not in st.session_state or not st.session_state["summary"]:
        st.info("Upload your CSV or try demo data on the Upload tab first.")
        return

    s       = st.session_state["summary"]
    api_key = st.session_state.get("api_key", "")

    # Generate or show cached narrative
    if "narrative" not in st.session_state:
        if api_key:
            with st.spinner("Writing your money story..."):
                try:
                    from utils.ai_engine import generate_narrative, generate_april_tip
                    st.session_state["narrative"] = generate_narrative(s, api_key)
                    st.session_state["tip"]       = generate_april_tip(s, api_key)
                except Exception as e:
                    st.warning(f"AI generation failed: {e}. Showing sample narrative.")
                    st.session_state["narrative"] = FALLBACK_NARRATIVE
                    st.session_state["tip"]       = FALLBACK_TIP
        else:
            st.session_state["narrative"] = FALLBACK_NARRATIVE
            st.session_state["tip"]       = FALLBACK_TIP

    narrative = st.session_state.get("narrative", FALLBACK_NARRATIVE)
    tip       = st.session_state.get("tip", FALLBACK_TIP)

    # Month label
    df    = st.session_state.get("df", None)
    month = df["month"].iloc[0] if df is not None and not df.empty else "This month"

    # Main narrative card
    st.markdown(f"""
    <div class="narr-box">
        <div class="narr-title">{month} — your money story</div>
        <div class="narr-body">{narrative.replace(chr(10), '<br><br>')}</div>
    </div>
    """, unsafe_allow_html=True)

    # Forward-looking tip card
    st.markdown(f"""
    <div class="narr-box" style="border-color:#2d1f5e;">
        <div class="narr-title" style="color:#c084fc;">What this means for next month</div>
        <div class="narr-body" style="border-color:#7F77DD;">{tip}</div>
    </div>
    """, unsafe_allow_html=True)

    # Quick stats strip
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Total transactions</div>
            <div class="metric-val">{s['n_trans']}</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Late night orders</div>
            <div class="metric-val">{s['late_night_pct']}%</div>
            <div class="metric-sub down">{s['late_night_n']} transactions</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Busiest day</div>
            <div class="metric-val" style="font-size:16px;">{s['busiest_day']}</div>
        </div>""", unsafe_allow_html=True)

    # Regenerate button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Regenerate story →"):
        for k in ["narrative", "tip"]:
            st.session_state.pop(k, None)
        st.rerun()
