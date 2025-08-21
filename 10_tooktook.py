import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# 기본 설정 & 글로벌 스타일
# -----------------------------
st.set_page_config(page_title="툭툭 상담 지원 대시보드", layout="wide")

# 💄 멀티셀렉트/컨트롤 컬러 커스텀 (파스텔 톤)
st.markdown(
    """
    <style>
    /* 멀티셀렉트 태그(선택된 값) 스타일 */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #eef4ff !important; /* 파스텔 블루 */
        color: #0f172a !important;             /* 네이비 텍스트 */
        border: 1px solid #c7d2fe !important;  /* 라벤더 보더 */
        box-shadow: none !important;
    }
    /* 셀렉트 박스 컨테이너 라운드 & 보더 살짝 */
    .stMultiSelect [data-baseweb="select"] > div {
        border-radius: 10px !important;
        border-color: #e5e7eb !important;
    }
    /* 포커스 링 톤 다운 */
    .stMultiSelect [data-baseweb="select"]:focus-within {
        box-shadow: 0 0 0 2px #c7d2fe55 !important;
        border-color: #c7d2fe !important;
    }
    /* 공통 카드 느낌 여백 */
    .block-container {padding-top: 1.5rem !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("툭툭 상담 지원 분석/시각화 대시보드 (샘플)")

# ========================
# 0) 사이드바: 시드/표본크기/필터
# ========================
st.sidebar.header("⚙️ 설정 & 필터")
seed = st.sidebar.number_input("난수 시드", value=42, step=1)
sample_n = st.sidebar.slider("샘플 행 수", min_value=50, max_value=5000, value=600, step=50)

# 도메인: 소상공인 정책자금 관련 주제
TOPICS = [
    "자금상담", "서류보완", "자격요건", "한도·금리", "상환·연체", "기타"
]
weekday_order = ["월", "화", "수", "목", "금"]
hour_min, hour_max = 9, 18

# 샘플 데이터 생성
np.random.seed(seed)
n = sample_n

df = pd.DataFrame({
    "call_id": range(1, n+1),
    "weekday": np.random.choice(weekday_order, n),
    "hour": np.random.choice(range(hour_min, hour_max+1), n),
    "agent": np.random.choice(["상담사A", "상담사B", "상담사C"], n),
    "topic": np.random.choice(TOPICS, n, p=[0.23, 0.18, 0.18, 0.18, 0.15, 0.08]),
    "AHT": np.random.normal(300, 60, n).clip(120, 900).astype(int),
    "FCR": np.random.choice([0, 1], n, p=[0.28, 0.72]),
    "CSAT": np.random.randint(1, 6, n)
})

weekday_cat = pd.api.types.CategoricalDtype(categories=weekday_order, ordered=True)
df["weekday"] = df["weekday"].astype(weekday_cat)

# ----- 사이드바 필터 -----
with st.sidebar.expander("필터", expanded=True):
    sel_days = st.multiselect("요일", options=weekday_order, default=weekday_order, key="ms_days")
    sel_hours = st.slider("시간대(시)", min_value=hour_min, max_value=hour_max, value=(9, 18), key="sl_hours")
    sel_agents = st.multiselect("상담사", options=sorted(df["agent"].unique()), default=sorted(df["agent"].unique()), key="ms_agents")
    sel_topics = st.multiselect("주제", options=TOPICS, default=TOPICS, key="ms_topics")

mask = (
    df["weekday"].isin(sel_days) &
    df["hour"].between(sel_hours[0], sel_hours[1]) &
    df["agent"].isin(sel_agents) &
    df["topic"].isin(sel_topics)
)

df_f = df.loc[mask].copy()

st.caption(f"현재 필터 적용 후 데이터: **{len(df_f):,}건** (전체 {len(df):,}건 중)")

# ========================
# 탭 구성
# ========================
tab_summary, tab_pattern, tab_eff, tab_quality, tab_data = st.tabs([
    "요약", "수요/패턴", "효율", "품질/만족", "데이터"
])

# ---------- (1) 요약 ----------
with tab_summary:
    st.subheader("📌 주요 KPI")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("평균 AHT(초)", f"{df_f['AHT'].mean():.1f}")
    c2.metric("FCR(1회 해결률)", f"{df_f['FCR'].mean()*100:.1f}%")
    c3.metric("평균 CSAT", f"{df_f['CSAT'].mean():.2f}")
    c4.metric("콜 수", f"{len(df_f):,}")

    st.markdown(
        "- **핵심 맥락**: 주제는 *소상공인 정책자금* 문의이며, 피크 시간대 인력배치·전문상담 핸드오프·스크립트 보완 포인트를 찾습니다."
    )

# ---------- (2) 수요/패턴 ----------
with tab_pattern:
    st.subheader("📊 요일×시간대 콜 분포")
    all_hours = list(range(hour_min, hour_max+1))
    pivot = (
        df_f
        .pivot_table(index="weekday", columns="hour", values="call_id", aggfunc="count", fill_value=0)
        .reindex(index=weekday_order)
        .reindex(columns=all_hours, fill_value=0)
    )
    fig_heatmap = px.imshow(
        pivot,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Blues",
        labels=dict(color="콜 수")
    )
    fig_heatmap.update_layout(margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig_heatmap, use_container_width=True)

    st.markdown(
        "- **읽는 법**: 진한 칸일수록 해당 요일·시간대 콜이 많습니다. 반복적인 피크가 보이면 그 슬롯에 **전문상담/서류상담 배치**를 고려하세요."
    )

# ---------- (3) 효율 ----------
with tab_eff:
    st.subheader("👥 상담사별 AHT 분포")
    fig_box = px.box(df_f, x="agent", y="AHT", points="all")
    fig_box.update_layout(margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig_box, use_container_width=True)

    st.subheader("⏱️ 시간대별 FCR 추이")
    line_df = df_f.groupby("hour", as_index=False)["FCR"].mean()
    fig_line = px.line(line_df, x="hour", y="FCR", markers=True)
    fig_line.update_layout(margin=dict(l=10, r=10, t=30, b=10), yaxis_tickformat=",.0%")
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown(
        "- **해석**: 특정 상담사의 AHT가 상시 높다면 *난이도 편향/전환 기준*을, FCR 저하 시간대엔 *핸드오프/중간 휴게*를 검토하세요."
    )

# ---------- (4) 품질/만족 ----------
with tab_quality:
    st.subheader("🎯 AHT vs CSAT 관계")
    fig_scatter = px.scatter(
        df_f, x="AHT", y="CSAT", color="topic",
        hover_data=["agent", "weekday", "hour"], opacity=0.7
    )
    fig_scatter.update_layout(margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig_scatter, use_container_width=True)

    corr = np.corrcoef(df_f["AHT"], df_f["CSAT"])[0,1] if len(df_f) > 1 else np.nan
    st.caption(f"AHT-CSAT 피어슨 상관계수: **{corr:.3f}** (음수면 상담 길수록 만족도 하락 경향)")

# ---------- (5) 데이터 ----------
with tab_data:
    st.subheader("📥 데이터 내려받기")
    cdl1, cdl2 = st.columns(2)
    cdl1.download_button(
        label="원본 데이터 CSV 다운로드",
        data=df.to_csv(index=False).encode("utf-8-sig"),
        file_name="tooktookie_calls_raw.csv",
        mime="text/csv",
        key="dl_raw"
    )
    cdl2.download_button(
        label="필터 적용 데이터 CSV 다운로드",
        data=df_f.to_csv(index=False).encode("utf-8-sig"),
        file_name="tooktookie_calls_filtered.csv",
        mime="text/csv",
        key="dl_flt"
    )

    st.dataframe(df_f.head(200), use_container_width=True)

# ========================
# 퀵 인사이트 가이드
# ========================
st.markdown(
    """
    ---
    ### 🔎 빠르게 보는 해석 포인트 (정책자금 컨텍스트)
    1. **피크 시간대**: 콜 수가 몰리는 구간에 *자격요건/한도·금리* 전문상담 투입.
    2. **상담사 편차**: AHT 상위 상담사는 케이스 난이도 편향인지, 스크립트/전환 기준 문제인지 구분.
    3. **FCR 저하**: 점심 직후/마감 직전 하락 시, *핸드오프 기준*과 *FAQ 링크 전송*으로 보완.
    4. **AHT↔CSAT**: 음의 상관이면 "짧게·정확히", 양의 상관이면 "충분한 설명" 전략.
    """
)
