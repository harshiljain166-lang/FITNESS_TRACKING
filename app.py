import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FitPulse Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── THEME DEFINITIONS ────────────────────────────────────────────────────────
THEMES = {
    "🌌 Cosmic Dark": {
        "bg": "#0a0a1a",
        "card_bg": "#12122a",
        "accent": "#7c3aed",
        "accent2": "#06b6d4",
        "accent3": "#f59e0b",
        "text": "#e2e8f0",
        "subtext": "#94a3b8",
        "border": "#1e1e4a",
        "gradient": "linear-gradient(135deg, #7c3aed 0%, #06b6d4 100%)",
        "plotly_template": "plotly_dark",
        "colors": ["#7c3aed", "#06b6d4", "#f59e0b", "#10b981"],
    },
    "🔥 Neon Inferno": {
        "bg": "#0f0a00",
        "card_bg": "#1a1000",
        "accent": "#ff4500",
        "accent2": "#ff8c00",
        "accent3": "#ffd700",
        "text": "#fff8e7",
        "subtext": "#d4a96a",
        "border": "#3a1a00",
        "gradient": "linear-gradient(135deg, #ff4500 0%, #ffd700 100%)",
        "plotly_template": "plotly_dark",
        "colors": ["#ff4500", "#ff8c00", "#ffd700", "#ff6347"],
    },
    "🌿 Bio Pulse": {
        "bg": "#010f07",
        "card_bg": "#041a0c",
        "accent": "#00ff87",
        "accent2": "#00d4aa",
        "accent3": "#a3e635",
        "text": "#dcfce7",
        "subtext": "#86efac",
        "border": "#064e3b",
        "gradient": "linear-gradient(135deg, #00ff87 0%, #00d4aa 100%)",
        "plotly_template": "plotly_dark",
        "colors": ["#00ff87", "#00d4aa", "#a3e635", "#34d399"],
    },
    "❄️ Arctic Pro": {
        "bg": "#f0f7ff",
        "card_bg": "#ffffff",
        "accent": "#0ea5e9",
        "accent2": "#6366f1",
        "accent3": "#ec4899",
        "text": "#0f172a",
        "subtext": "#475569",
        "border": "#e2e8f0",
        "gradient": "linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%)",
        "plotly_template": "plotly_white",
        "colors": ["#0ea5e9", "#6366f1", "#ec4899", "#f59e0b"],
    },
    "🩸 Crimson Edge": {
        "bg": "#0d0000",
        "card_bg": "#1a0000",
        "accent": "#dc2626",
        "accent2": "#9f1239",
        "accent3": "#fb7185",
        "text": "#ffe4e6",
        "subtext": "#fda4af",
        "border": "#450a0a",
        "gradient": "linear-gradient(135deg, #dc2626 0%, #9f1239 100%)",
        "plotly_template": "plotly_dark",
        "colors": ["#dc2626", "#9f1239", "#fb7185", "#f87171"],
    },
}

# ── LOAD DATA ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("gym_members_exercise_tracking.csv")
    df["Experience_Label"] = df["Experience_Level"].map({1: "Beginner", 2: "Intermediate", 3: "Advanced"})
    return df

df = load_data()

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚡ FitPulse Analytics")
    st.markdown("---")

    # Theme selector
    theme_name = st.selectbox("🎨 Choose Theme", list(THEMES.keys()), index=0)
    T = THEMES[theme_name]

    st.markdown("---")
    st.markdown("### 🎛️ Filters")

    genders = st.multiselect("Gender", ["Male", "Female"], default=["Male", "Female"])
    workout_types = st.multiselect(
        "Workout Type",
        df["Workout_Type"].unique().tolist(),
        default=df["Workout_Type"].unique().tolist(),
    )
    exp_levels = st.multiselect(
        "Experience Level",
        ["Beginner", "Intermediate", "Advanced"],
        default=["Beginner", "Intermediate", "Advanced"],
    )
    age_range = st.slider("Age Range", int(df["Age"].min()), int(df["Age"].max()), (18, 59))

    st.markdown("---")
    st.markdown("### 📊 Chart Style")
    chart_opacity = st.slider("Opacity", 0.4, 1.0, 0.85, 0.05)
    show_gridlines = st.toggle("Show Gridlines", value=True)

    st.markdown("---")
    st.caption("FitPulse Analytics v2.0 · Built with ❤️")

# ── APPLY FILTERS ────────────────────────────────────────────────────────────
exp_map = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}
exp_nums = [exp_map[e] for e in exp_levels]
filtered = df[
    df["Gender"].isin(genders)
    & df["Workout_Type"].isin(workout_types)
    & df["Experience_Level"].isin(exp_nums)
    & df["Age"].between(age_range[0], age_range[1])
]

# ── DYNAMIC CSS ──────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    html, body, [class*="css"] {{
        font-family: 'DM Sans', sans-serif;
        background-color: {T['bg']} !important;
        color: {T['text']} !important;
    }}
    
    /* Main container */
    .stApp {{
        background-color: {T['bg']} !important;
    }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: {T['card_bg']} !important;
        border-right: 1px solid {T['border']} !important;
    }}
    [data-testid="stSidebar"] * {{
        color: {T['text']} !important;
    }}
    
    /* All text */
    h1, h2, h3, h4, h5, h6, p, label, span, div {{
        color: {T['text']} !important;
    }}

    /* Metric cards */
    [data-testid="metric-container"] {{
        background: {T['card_bg']} !important;
        border: 1px solid {T['border']} !important;
        border-radius: 16px !important;
        padding: 20px !important;
        box-shadow: 0 4px 24px rgba(0,0,0,0.2) !important;
    }}
    [data-testid="stMetricValue"] {{
        font-family: 'Syne', sans-serif !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
        color: {T['accent']} !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: {T['subtext']} !important;
        font-weight: 500 !important;
    }}
    [data-testid="stMetricDelta"] {{
        color: {T['accent2']} !important;
    }}

    /* Selectbox & Widgets */
    .stSelectbox > div > div, .stMultiSelect > div > div {{
        background: {T['card_bg']} !important;
        border-color: {T['border']} !important;
        color: {T['text']} !important;
        border-radius: 10px !important;
    }}
    .stSlider [data-testid="stTickBarMin"], .stSlider [data-testid="stTickBarMax"] {{
        color: {T['subtext']} !important;
    }}

    /* Section headers */
    .section-title {{
        font-family: 'Syne', sans-serif;
        font-size: 1.35rem;
        font-weight: 700;
        color: {T['text']};
        margin: 28px 0 16px;
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    .section-title::after {{
        content: '';
        flex: 1;
        height: 1px;
        background: {T['border']};
        margin-left: 12px;
    }}

    /* Hero banner */
    .hero-banner {{
        background: {T['gradient']};
        border-radius: 20px;
        padding: 28px 36px;
        margin-bottom: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    .hero-title {{
        font-family: 'Syne', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        color: #ffffff !important;
        margin: 0;
        text-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }}
    .hero-sub {{
        color: rgba(255,255,255,0.85) !important;
        font-size: 0.95rem;
        margin-top: 6px;
    }}
    .hero-badge {{
        background: rgba(255,255,255,0.2);
        border-radius: 50px;
        padding: 8px 20px;
        font-family: 'Syne', sans-serif;
        font-weight: 700;
        color: #ffffff !important;
        font-size: 0.9rem;
        backdrop-filter: blur(10px);
    }}

    /* Chart containers */
    .chart-card {{
        background: {T['card_bg']};
        border: 1px solid {T['border']};
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
    }}

    /* Plotly chart backgrounds */
    .js-plotly-plot .plotly, .js-plotly-plot .plotly .main-svg {{
        background: transparent !important;
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        background: {T['card_bg']} !important;
        border-radius: 12px !important;
        padding: 4px !important;
        border: 1px solid {T['border']} !important;
        gap: 4px !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px !important;
        color: {T['subtext']} !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
        padding: 8px 16px !important;
    }}
    .stTabs [aria-selected="true"] {{
        background: {T['accent']} !important;
        color: #ffffff !important;
    }}

    /* Scrollbar */
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: {T['bg']}; }}
    ::-webkit-scrollbar-thumb {{ background: {T['border']}; border-radius: 6px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: {T['accent']}; }}

    /* Filter container */
    .filter-row {{
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
        margin-bottom: 20px;
    }}
    .filter-chip {{
        background: {T['card_bg']};
        border: 1px solid {T['accent']};
        color: {T['accent']};
        border-radius: 50px;
        padding: 4px 14px;
        font-size: 0.8rem;
        font-weight: 600;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ── HELPER ───────────────────────────────────────────────────────────────────
def styled_chart(fig):
    bg = "rgba(0,0,0,0)" if T["plotly_template"] == "plotly_dark" else "rgba(255,255,255,0)"
    grid_color = T["border"] if show_gridlines else "rgba(0,0,0,0)"
    fig.update_layout(
        paper_bgcolor=bg,
        plot_bgcolor=bg,
        font_family="DM Sans",
        font_color=T["text"],
        title_font_family="Syne",
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font_color=T["text"],
        ),
        xaxis=dict(gridcolor=grid_color, zerolinecolor=grid_color, color=T["subtext"]),
        yaxis=dict(gridcolor=grid_color, zerolinecolor=grid_color, color=T["subtext"]),
    )
    return fig

# ── HERO BANNER ──────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <div class="hero-banner">
        <div>
            <div class="hero-title">⚡ FitPulse Analytics</div>
            <div class="hero-sub">Gym Member Performance & Insights Dashboard</div>
        </div>
        <div class="hero-badge">📊 {len(filtered):,} Members Loaded</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── KPI METRICS ──────────────────────────────────────────────────────────────
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("👥 Members", f"{len(filtered):,}", f"{len(filtered)/len(df)*100:.0f}% of total")
with col2:
    st.metric("🔥 Avg Calories", f"{filtered['Calories_Burned'].mean():.0f}", "kcal/session")
with col3:
    st.metric("⏱️ Avg Session", f"{filtered['Session_Duration (hours)'].mean():.2f} hr", "duration")
with col4:
    st.metric("💧 Avg Water", f"{filtered['Water_Intake (liters)'].mean():.2f} L", "intake")
with col5:
    st.metric("📈 Avg BMI", f"{filtered['BMI'].mean():.1f}", "body mass index")

st.markdown("<br>", unsafe_allow_html=True)

# ── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["🏋️ Workout Analysis", "💓 Health Metrics", "👥 Demographics", "🔬 Correlation Lab"])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — WORKOUT ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-title">Calories by Workout Type</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([3, 2])
    with c1:
        agg = filtered.groupby("Workout_Type")["Calories_Burned"].mean().reset_index()
        fig = px.bar(
            agg, x="Workout_Type", y="Calories_Burned",
            color="Workout_Type", color_discrete_sequence=T["colors"],
            labels={"Calories_Burned": "Avg Calories Burned", "Workout_Type": "Workout"},
            title="Average Calories Burned per Workout Type",
            opacity=chart_opacity,
        )
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(styled_chart(fig), use_container_width=True)

    with c2:
        wt_counts = filtered["Workout_Type"].value_counts().reset_index()
        wt_counts.columns = ["Workout_Type", "Count"]
        fig2 = px.pie(
            wt_counts, names="Workout_Type", values="Count",
            color_discrete_sequence=T["colors"],
            title="Workout Type Distribution",
            hole=0.52,
        )
        fig2.update_traces(textfont_color=T["text"], opacity=chart_opacity)
        st.plotly_chart(styled_chart(fig2), use_container_width=True)

    st.markdown('<div class="section-title">Session Duration vs Calories</div>', unsafe_allow_html=True)
    fig3 = px.scatter(
        filtered, x="Session_Duration (hours)", y="Calories_Burned",
        color="Workout_Type", size="Weight (kg)",
        color_discrete_sequence=T["colors"],
        facet_col="Experience_Label",
        title="Session Duration vs Calories — by Experience Level",
        opacity=chart_opacity,
        trendline="ols",
    )
    st.plotly_chart(styled_chart(fig3), use_container_width=True)

    st.markdown('<div class="section-title">Workout Frequency & Performance</div>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        freq_cal = filtered.groupby(["Workout_Frequency (days/week)", "Workout_Type"])["Calories_Burned"].mean().reset_index()
        fig4 = px.line(
            freq_cal, x="Workout_Frequency (days/week)", y="Calories_Burned",
            color="Workout_Type", markers=True,
            color_discrete_sequence=T["colors"],
            title="Frequency vs Calories by Workout",
        )
        st.plotly_chart(styled_chart(fig4), use_container_width=True)

    with c4:
        freq_dur = filtered.groupby("Workout_Frequency (days/week)")["Session_Duration (hours)"].mean().reset_index()
        fig5 = px.area(
            freq_dur, x="Workout_Frequency (days/week)", y="Session_Duration (hours)",
            color_discrete_sequence=[T["accent"]],
            title="Avg Session Duration by Workout Frequency",
            line_shape="spline",
        )
        fig5.update_traces(opacity=chart_opacity)
        st.plotly_chart(styled_chart(fig5), use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — HEALTH METRICS
# ════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">Heart Rate Analysis</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        bpm_data = filtered.melt(
            id_vars="Workout_Type",
            value_vars=["Max_BPM", "Avg_BPM", "Resting_BPM"],
            var_name="BPM Type", value_name="BPM"
        )
        fig6 = px.box(
            bpm_data, x="Workout_Type", y="BPM", color="BPM Type",
            color_discrete_sequence=T["colors"],
            title="Heart Rate Ranges by Workout Type",
        )
        st.plotly_chart(styled_chart(fig6), use_container_width=True)

    with c2:
        fig7 = px.violin(
            filtered, y="Resting_BPM", x="Experience_Label",
            color="Gender", box=True, points="outliers",
            color_discrete_sequence=T["colors"],
            title="Resting BPM by Experience & Gender",
        )
        st.plotly_chart(styled_chart(fig7), use_container_width=True)

    st.markdown('<div class="section-title">BMI & Body Composition</div>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        fig8 = px.histogram(
            filtered, x="BMI", color="Gender",
            color_discrete_sequence=T["colors"],
            title="BMI Distribution by Gender",
            barmode="overlay", nbins=30, opacity=chart_opacity,
        )
        st.plotly_chart(styled_chart(fig8), use_container_width=True)

    with c4:
        fig9 = px.scatter(
            filtered, x="BMI", y="Fat_Percentage",
            color="Experience_Label", size="Calories_Burned",
            color_discrete_sequence=T["colors"],
            title="BMI vs Fat Percentage",
            opacity=chart_opacity,
        )
        st.plotly_chart(styled_chart(fig9), use_container_width=True)

    st.markdown('<div class="section-title">BPM Gauge — Average Metrics</div>', unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    metrics = [
        ("Max BPM", filtered["Max_BPM"].mean(), 220, T["colors"][0]),
        ("Avg BPM", filtered["Avg_BPM"].mean(), 180, T["colors"][1]),
        ("Resting BPM", filtered["Resting_BPM"].mean(), 100, T["colors"][2]),
    ]
    for col, (label, val, mx, color) in zip([g1, g2, g3], metrics):
        with col:
            fig_g = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=val,
                title={"text": label, "font": {"family": "Syne", "size": 16, "color": T["text"]}},
                delta={"reference": mx * 0.6, "increasing": {"color": T["accent2"]}},
                gauge={
                    "axis": {"range": [None, mx], "tickcolor": T["subtext"]},
                    "bar": {"color": color},
                    "bgcolor": T["card_bg"],
                    "bordercolor": T["border"],
                    "steps": [
                        {"range": [0, mx * 0.5], "color": T["bg"]},
                        {"range": [mx * 0.5, mx * 0.8], "color": T["border"]},
                    ],
                    "threshold": {"line": {"color": T["accent3"], "width": 3}, "value": mx * 0.85},
                },
                number={"font": {"color": T["accent"], "family": "Syne"}, "suffix": " bpm"},
            ))
            fig_g.update_layout(
                height=250,
                paper_bgcolor="rgba(0,0,0,0)",
                font_color=T["text"],
                margin=dict(l=20, r=20, t=60, b=20),
            )
            st.plotly_chart(fig_g, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — DEMOGRAPHICS
# ════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">Age & Gender Distribution</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        fig10 = px.histogram(
            filtered, x="Age", color="Gender",
            color_discrete_sequence=T["colors"],
            title="Age Distribution by Gender",
            nbins=25, barmode="overlay", opacity=chart_opacity,
        )
        st.plotly_chart(styled_chart(fig10), use_container_width=True)

    with c2:
        age_bins = pd.cut(filtered["Age"], bins=[18, 25, 35, 45, 60], labels=["18-25", "26-35", "36-45", "46-60"])
        age_wt = filtered.copy()
        age_wt["Age Group"] = age_bins
        grp = age_wt.groupby(["Age Group", "Workout_Type"]).size().reset_index(name="Count")
        fig11 = px.bar(
            grp, x="Age Group", y="Count", color="Workout_Type",
            color_discrete_sequence=T["colors"],
            title="Workout Preference by Age Group",
            barmode="stack", opacity=chart_opacity,
        )
        st.plotly_chart(styled_chart(fig11), use_container_width=True)

    st.markdown('<div class="section-title">Experience Level Breakdown</div>', unsafe_allow_html=True)
    c3, c4 = st.columns([2, 3])
    with c3:
        exp_cnt = filtered["Experience_Label"].value_counts().reset_index()
        exp_cnt.columns = ["Level", "Count"]
        fig12 = px.funnel(
            exp_cnt, x="Count", y="Level",
            color_discrete_sequence=T["colors"],
            title="Member Experience Funnel",
        )
        fig12.update_traces(opacity=chart_opacity)
        st.plotly_chart(styled_chart(fig12), use_container_width=True)

    with c4:
        radar_df = filtered.groupby("Experience_Label")[
            ["Calories_Burned", "Session_Duration (hours)", "Water_Intake (liters)", "Workout_Frequency (days/week)", "BMI"]
        ].mean().reset_index()

        cats = ["Calories (÷10)", "Session (×60)", "Water (×20)", "Frequency (×20)", "BMI (×4)"]
        fig13 = go.Figure()
        for i, row in radar_df.iterrows():
            vals = [
                row["Calories_Burned"] / 10,
                row["Session_Duration (hours)"] * 60,
                row["Water_Intake (liters)"] * 20,
                row["Workout_Frequency (days/week)"] * 20,
                row["BMI"] * 4,
            ]
            vals += [vals[0]]
            fig13.add_trace(go.Scatterpolar(
                r=vals, theta=cats + [cats[0]],
                fill="toself", name=row["Experience_Label"],
                line_color=T["colors"][i],
                fillcolor=T["colors"][i],
                opacity=0.35 + i * 0.1,
            ))
        fig13.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, gridcolor=T["border"], color=T["subtext"]),
                angularaxis=dict(gridcolor=T["border"], color=T["text"]),
                bgcolor=T["card_bg"],
            ),
            showlegend=True,
            title="Fitness Radar — Experience Levels",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color=T["text"],
            title_font_family="Syne",
            margin=dict(l=20, r=20, t=50, b=20),
        )
        st.plotly_chart(fig13, use_container_width=True)

    st.markdown('<div class="section-title">Weight & Height Distribution</div>', unsafe_allow_html=True)
    fig14 = px.scatter(
        filtered, x="Height (m)", y="Weight (kg)",
        color="Gender", symbol="Workout_Type",
        size="BMI", hover_data=["Age", "Experience_Label"],
        color_discrete_sequence=T["colors"],
        title="Height vs Weight (size = BMI)",
        opacity=chart_opacity,
    )
    st.plotly_chart(styled_chart(fig14), use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — CORRELATION LAB
# ════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">Correlation Heatmap</div>', unsafe_allow_html=True)
    num_cols = ["Age", "Weight (kg)", "Height (m)", "Max_BPM", "Avg_BPM", "Resting_BPM",
                "Session_Duration (hours)", "Calories_Burned", "Fat_Percentage",
                "Water_Intake (liters)", "Workout_Frequency (days/week)", "BMI"]
    corr = filtered[num_cols].corr()

    fig15 = go.Figure(go.Heatmap(
        z=corr.values,
        x=[c.replace("(", "<br>(") for c in corr.columns],
        y=[c.replace("(", "<br>(") for c in corr.index],
        colorscale=[
            [0.0, T["accent2"]],
            [0.5, T["bg"]],
            [1.0, T["accent"]],
        ],
        zmin=-1, zmax=1,
        text=corr.round(2).values,
        texttemplate="%{text}",
        hoverongaps=False,
    ))
    fig15.update_layout(
        title="Pearson Correlation Matrix",
        height=520,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=T["text"],
        title_font_family="Syne",
        margin=dict(l=10, r=10, t=50, b=10),
    )
    st.plotly_chart(fig15, use_container_width=True)

    st.markdown('<div class="section-title">Custom Scatter Explorer</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        x_axis = st.selectbox("X Axis", num_cols, index=7)
    with c2:
        y_axis = st.selectbox("Y Axis", num_cols, index=6)
    with c3:
        color_by = st.selectbox("Color By", ["Workout_Type", "Gender", "Experience_Label"], index=0)

    fig16 = px.scatter(
        filtered, x=x_axis, y=y_axis, color=color_by,
        color_discrete_sequence=T["colors"],
        trendline="ols", marginal_x="histogram", marginal_y="box",
        title=f"{x_axis} vs {y_axis}",
        opacity=chart_opacity,
    )
    st.plotly_chart(styled_chart(fig16), use_container_width=True)

    st.markdown('<div class="section-title">Parallel Coordinates</div>', unsafe_allow_html=True)
    pc_cols = ["Age", "BMI", "Calories_Burned", "Session_Duration (hours)", "Fat_Percentage", "Water_Intake (liters)"]
    pc_df = filtered.copy()
    pc_df["exp_num"] = pc_df["Experience_Level"]
    fig17 = px.parallel_coordinates(
        pc_df, dimensions=pc_cols,
        color="exp_num",
        color_continuous_scale=[T["colors"][0], T["colors"][1], T["colors"][2]],
        title="Parallel Coordinates — All Key Metrics",
    )
    fig17.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=T["text"],
        title_font_family="Syne",
    )
    st.plotly_chart(fig17, use_container_width=True)

# ── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    f"""
    <div style="text-align:center; color:{T['subtext']}; font-size:0.85rem; padding: 12px 0;">
        ⚡ <strong style="color:{T['accent']}">FitPulse Analytics</strong> · 
        {len(filtered):,} members · {len(filtered.columns if hasattr(filtered, 'columns') else [])} metrics · 
        Powered by Streamlit & Plotly
    </div>
    """,
    unsafe_allow_html=True,
)