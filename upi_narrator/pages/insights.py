import streamlit as st
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

FALLBACK_INSIGHTS = [
    {"tag": "Late night spender", "tag_type": "amber",
     "text": "You placed 11 out of 18 Swiggy orders after 10pm. Your average late-night order costs ₹340 — 28% more than daytime orders."},
    {"tag": "Friday pattern",     "tag_type": "blue",
     "text": "Fridays cost you ₹980 on average — your most expensive day by far. Weekend dinners and Uber rides home seem to be the main driver."},
    {"tag": "Good habit spotted", "tag_type": "green",
     "text": "You paid all utility bills before the 10th of the month. No late fees — saving you an estimated ₹150 in penalties."},
    {"tag": "Subscription check", "tag_type": "purple",
     "text": "You're paying for Netflix, Spotify, and Amazon Prime simultaneously — ₹1,067/month on streaming, ₹12,804/year."},
    {"tag": "UPI frequency",      "tag_type": "amber",
     "text": "You made 84 transactions in 31 days — nearly 3 per day. Your most transacted hours are 1pm (lunch) and 9pm (dinner)."},
    {"tag": "Saving opportunity", "tag_type": "blue",
     "text": "Switching 2 Uber rides per week to Metro could save around ₹840/month based on your most frequent routes."},
]

def render():
    st.markdown('<div class="sec-head">Screen 4 — Spending insights</div>', unsafe_allow_html=True)

    if "summary" not in st.session_state or not st.session_state["summary"]:
        st.info("Upload your CSV or try demo data on the Upload tab first.")
        return

    s       = st.session_state["summary"]
    api_key = st.session_state.get("api_key", "")

    if "insights" not in st.session_state:
        if api_key:
            with st.spinner("Generating insights..."):
                try:
                    from utils.ai_engine import generate_insights
                    insights = generate_insights(s, api_key)
                    st.session_state["insights"] = insights if insights else FALLBACK_INSIGHTS
                except Exception:
                    st.session_state["insights"] = FALLBACK_INSIGHTS
        else:
            # Build rule-based insights from data when no API key
            insights = list(FALLBACK_INSIGHTS)

            # Override with real numbers where possible
            total       = s.get("total", 0)
            top_cat     = s.get("top_cat", "Food")
            top_cat_amt = s.get("top_cat_amt", 0)
            top_cat_pct = s.get("top_cat_pct", 0)
            late_pct    = s.get("late_night_pct", 0)
            late_n      = s.get("late_night_n", 0)
            busiest     = s.get("busiest_day", "Friday")

            insights[0]["text"] = f"You made {late_n} late-night transactions ({late_pct}% of total). Late-night spending tends to be impulsive — worth watching."
            insights[1]["text"] = f"{busiest} is your most expensive day. Weekend patterns often drive 30–40% higher spending than weekday averages."
            insights[2]["text"] = f"Your top category is {top_cat} at ₹{top_cat_amt:,.0f} ({top_cat_pct}% of total spending this month."
            insights[3]["text"] = f"Total spend of ₹{total:,.0f} across {s.get('n_trans',0)} transactions — averaging ₹{s.get('avg_day',0):,.0f} per day."

            st.session_state["insights"] = insights

    insights = st.session_state.get("insights", FALLBACK_INSIGHTS)

    # Render insights in 2-column grid
    col1, col2 = st.columns(2)
    for i, ins in enumerate(insights):
        tag      = ins.get("tag", "Insight")
        tag_type = ins.get("tag_type", "blue")
        text     = ins.get("text", "")
        card_html = f"""
        <div class="insight-card">
            <span class="insight-tag tag-{tag_type}">{tag}</span>
            <div class="insight-body">{text}</div>
        </div>"""
        if i % 2 == 0:
            col1.markdown(card_html, unsafe_allow_html=True)
        else:
            col2.markdown(card_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Regenerate insights →"):
        st.session_state.pop("insights", None)
        st.rerun()
