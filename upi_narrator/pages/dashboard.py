import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DARK_BG   = "#0F1117"
CARD_BG   = "#161822"
BORDER    = "#2a2d3e"
TEXT_PRI  = "#e2e8f0"
TEXT_MUT  = "#94a3b8"
TEXT_DIM  = "#64748b"
ACCENT    = "#a78bfa"

def dark_fig(fig):
    fig.update_layout(
        paper_bgcolor = DARK_BG,
        plot_bgcolor  = CARD_BG,
        font          = dict(color=TEXT_MUT, size=12),
        margin        = dict(l=12, r=12, t=32, b=12),
        legend        = dict(bgcolor=CARD_BG, bordercolor=BORDER, font=dict(color=TEXT_MUT)),
        xaxis         = dict(gridcolor=BORDER, linecolor=BORDER, tickfont=dict(color=TEXT_DIM)),
        yaxis         = dict(gridcolor=BORDER, linecolor=BORDER, tickfont=dict(color=TEXT_DIM)),
    )
    return fig

def render():
    st.markdown('<div class="sec-head">Screen 2 — Spending dashboard</div>', unsafe_allow_html=True)

    if "summary" not in st.session_state or not st.session_state["summary"]:
        st.info("Upload your CSV or try demo data on the Upload tab first.")
        return

    s  = st.session_state["summary"]
    df = st.session_state.get("df", pd.DataFrame())

    # ── Metric cards ──────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Total spent</div>
            <div class="metric-val">₹{s['total']:,.0f}</div>
            <div class="metric-sub accent">{df['month'].iloc[0] if not df.empty else ''}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Transactions</div>
            <div class="metric-val">{s['n_trans']}</div>
            <div class="metric-sub up">this period</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Avg per day</div>
            <div class="metric-val">₹{s['avg_day']:,.0f}</div>
            <div class="metric-sub" style="color:#64748b;">daily average</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Top category</div>
            <div class="metric-val" style="font-size:17px;">{s['top_cat']}</div>
            <div class="metric-sub accent">₹{s['top_cat_amt']:,.0f} · {s['top_cat_pct']}%</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts row ────────────────────────────────────────────────────────────
    col_left, col_right = st.columns([1.3, 0.7])

    with col_left:
        by_cat    = s["by_cat"]
        cats      = list(by_cat.keys())
        amounts   = list(by_cat.values())
        colors_map= s["colors"]
        bar_colors= [colors_map.get(c, "#94a3b8") for c in cats]

        fig_bar = go.Figure(go.Bar(
            x            = amounts,
            y            = cats,
            orientation  = "h",
            marker_color = bar_colors,
            text         = [f"₹{a:,.0f}" for a in amounts],
            textposition = "outside",
            textfont     = dict(color=TEXT_MUT, size=11),
        ))
        fig_bar.update_layout(
            title      = dict(text="Spending by category", font=dict(color=TEXT_MUT, size=12)),
            xaxis_title= "",
            yaxis_title= "",
            height     = 280,
            showlegend = False,
        )
        dark_fig(fig_bar)
        fig_bar.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_right:
        fig_donut = go.Figure(go.Pie(
            labels      = cats,
            values      = amounts,
            hole        = 0.6,
            marker_colors= bar_colors,
            textinfo    = "percent",
            textfont    = dict(color=TEXT_PRI, size=11),
            hovertemplate= "<b>%{label}</b><br>₹%{value:,.0f}<br>%{percent}<extra></extra>",
        ))
        fig_donut.update_layout(
            title      = dict(text="Category split", font=dict(color=TEXT_MUT, size=12)),
            height     = 280,
            showlegend = True,
            legend     = dict(font=dict(size=10, color=TEXT_DIM)),
            annotations= [dict(
                text      = f"₹{s['total']:,.0f}",
                x=0.5, y=0.5,
                font_size = 14,
                font_color= TEXT_PRI,
                showarrow = False,
            )]
        )
        dark_fig(fig_donut)
        st.plotly_chart(fig_donut, use_container_width=True)

    # ── Day of week chart ─────────────────────────────────────────────────────
    by_day  = s.get("by_day", {})
    day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    days    = [d for d in day_order if d in by_day]
    day_amts= [by_day[d] for d in days]
    day_clrs= [ACCENT if d == s.get("busiest_day") else "#2a2d3e" for d in days]

    fig_day = go.Figure(go.Bar(
        x            = days,
        y            = day_amts,
        marker_color = day_clrs,
        text         = [f"₹{a:,.0f}" for a in day_amts],
        textposition = "outside",
        textfont     = dict(color=TEXT_MUT, size=10),
    ))
    fig_day.update_layout(
        title  = dict(text=f"Spending by day of week  ·  busiest: {s.get('busiest_day','')}", font=dict(color=TEXT_MUT, size=12)),
        height = 220,
        showlegend=False,
    )
    dark_fig(fig_day)
    st.plotly_chart(fig_day, use_container_width=True)

    # ── Top merchants table ───────────────────────────────────────────────────
    st.markdown('<div class="sec-head" style="margin-top:8px;">Top merchants</div>', unsafe_allow_html=True)
    by_merch = s.get("by_merch", {})
    merch_df = pd.DataFrame({"Merchant": list(by_merch.keys()), "Amount (₹)": list(by_merch.values())})
    merch_df["Amount (₹)"] = merch_df["Amount (₹)"].apply(lambda x: f"₹{x:,.0f}")
    st.dataframe(merch_df, use_container_width=True, hide_index=True)
