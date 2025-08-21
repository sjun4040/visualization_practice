import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("툭툭 상담 지원 분석/시각화 대시보드 (샘플)")

#------------------------
#샘플 데이터 생성
#------------------------
np.random.seed(42)
n = 200
df_sample = pd.DataFrame({
    "call_id": range(1, n+1),
    "weekday": np.random.choice(["월", "화", "수", "목", "금", "토", "일"], n),
    "hour": np.random.choice(range(9, 19), n),  # 9시~18시
    "agent": np.random.choice(["상담사A","상담사B","상담사C"], n),
    "topic": np.random.choice(["요금", "해지", "장애", "가입"], n),
    "sentiment": np.random.choice(["긍정","중립","부정"], n, p=[0.3,0.4,0.3]),
    "AHT": np.random.normal(300, 50, n).astype(int),   # 평균 300초
    "FCR": np.random.choice([0,1], n, p=[0.3,0.7]),
    "CSAT": np.random.randint(1, 6, n)  # 1~5점
})

#------------------------
#요약 KPI
#------------------------
st.subheader("📌 주요 KPI")
col1, col2, col3 = st.columns(3)
col1.metric("평균 AHT(초)", f"{df_sample['AHT'].mean():.1f}")
col2.metric("FCR(1회 해결률)", f"{df_sample['FCR'].mean()*100:.1f}%")
col3.metric("평균 CSAT", f"{df_sample['CSAT'].mean():.2f}")

#------------------------
#요일 × 시간대 히트맵 (콜 수)
#------------------------
st.subheader("📊 요일×시간대 콜 분포")
pivot = df_sample.pivot_table(index="weekday", columns="hour", values="call_id", aggfunc="count", fill_value=0)
fig_heatmap = px.imshow(pivot, text_auto=True, aspect="auto", color_continuous_scale="Blues")
st.plotly_chart(fig_heatmap, use_container_width=True)

#------------------------
#상담사별 박스플롯 (AHT 분포)
#------------------------
st.subheader("👥 상담사별 AHT 분포")
fig_box = px.box(df_sample, x="agent", y="AHT", points="all")
st.plotly_chart(fig_box, use_container_width=True)

#------------------------
#주제별 감성 분포
#------------------------
st.subheader("📌 주제별 감성 분포")
fig_bar = px.histogram(df_sample, x="topic", color="sentiment", barmode="group")
st.plotly_chart(fig_bar, use_container_width=True)
