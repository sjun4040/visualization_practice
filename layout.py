import streamlit as st

# layout 요소
# columns는 요소를 왼쪽 -> 오른쪽으로 배치할 수 있다.

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        '오늘의 날씨',
        value='35도',
        delta='+3'
    )

with col2:
    st.metric(
        '오늘의 미세먼지',
        value='좋음',
        delta='-30',
        delta_color='inverse'
    )
    
with col3:
    st.metric(
        '오늘의 습도',
        value='15%'
    )
    
## 
st.markdown('---')
data= {
    '이름': ['홍길동', '김길동', '박길동'],
    '나이': [10,20,30]
}
import pandas as pd
df=pd.DataFrame(data)
st.dataframe(df)

st.divider()

st.table(df)

st.divider()

st.json(data)

# datafile.csv > load > table 출력 > px.box() > st.plotly_chart()
# 데이터 불러오기
import plotly.express as px
import seaborn as sns
df_co2 = pd.read_csv('./data/CO2_Emissions.csv')
st.table(df_co2.head(10))

x_options = [
    'Fuel Consumption Comb (L/100 km)',
    'Fuel Consumption City (L/100 km)',
    'Fuel Consumption Hwy (L/100 km)',
    'Engine Size(L)',
    'Fuel Consumption Comb (mpg)'
]

hue_options = ['Transmission', 'Vehicle Class']

x_option = st.selectbox('Select X-axis', options=x_options, index=0)
hue_option = st.selectbox('Select hue-axis', options=hue_options, index=0)

fig = px.scatter(
    data_frame=df_co2,
    x=x_option,
    y='CO2 Emissions(g/km)',
    color=hue_option,
    width=500
)
fig.update_layout(
    legend_x=1.0,
    legend_y=1.0
)

st.plotly_chart(fig)