# --- 라이브러리 정의
import streamlit as st
from PIL import Image
import datetime
import pandas as pd
import plotly.express as px

# ------ 정의 
img = Image.open('고양이_ai.png')
df_ice = pd.read_csv('icecream_sales.csv')


# --- 분석용 시각화 코드
# 날짜 타입 변환
df_ice['날짜'] = pd.to_datetime(df_ice['날짜'])

# 1. 월별 매출 합계
df_ice['월'] = df_ice['날짜'].dt.month
month_sales = df_ice.groupby('월')['매출'].sum().reset_index()
month_sales['월_str'] = month_sales['월'].astype(str)

def fig1():
    fig1 = px.bar(
        month_sales,
        x='월',
        y='매출',
        title='월별 매출 현황',
        color='월_str',
        text='매출',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig1.update_layout(
        plot_bgcolor='#fffbe6',
        paper_bgcolor='#fffbe6',
        font_family='Nanum Gothic',
        title_font_color='#4c1900',
        title_font_size=22
    )
    fig1.update_traces(texttemplate='%{text:,}원', textposition='outside')
    return fig1


# 2. 맛별 매출 순위
flavor_sales = df_ice.groupby('맛')['매출'].sum().reset_index().sort_values('매출', ascending=False)

def fig2():
    fig2 = px.bar(
        flavor_sales,
        x='맛',
        y='매출',
        title='맛별 매출 순위',
        color='맛',
        text='매출',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig2.update_layout(
        plot_bgcolor='#f7f7f7',
        font_family='Nanum Gothic',
        title_font_color='#7e4a13',
        title_font_size=22
    )
    fig2.update_traces(texttemplate='%{text:,}원', textposition='outside')
    return fig2

# ---- 대시 보드 상단 
month = datetime.datetime.now().month
month_sales = df_ice[df_ice['월'] == month]['매출'].sum()
choco_count = df_ice[(df_ice['월'] == month) & (df_ice['맛'] == '초코')]['개수'].sum()

col1, col2 = st.columns(2)  # col1에는 이번 달 매출, col2에는 어떤 종류의 맛이 잘팔리는 지 

with col1:
    st.metric(
        f'{month}월 매출 현황',
        value=(f'{month_sales:,}원'),
        delta='+'
    )

with col2:
    st.metric(
        f'{month}월의 맛',
        value='초코',
        delta=(f'이번 달 초코 맛 선택 수 : {choco_count} ')
        
    )
    
# --- 함수 chice_icecream
def choice_icecream():
    tab1, tab2, tab3 = st.tabs(['맛 선택', '컵 사이즈 선택', '배달 여부'])
    
    with tab1:
        favor_option = st.selectbox('맛 선택',
                     options= ['초코','바닐라','딸기','녹차','커피'],
                     index=None,
                     placeholder='맛을 선택해주세요'
                     )
        st.text(f'{favor_option}을 선택하셨습니다.')

    with tab2:
        size_option = st.selectbox('컵 사이즈 선택', 
                                   options = ['소','중','대'],
                                   index=None,
                                   placeholder='컵 사이즈를 선택해주세요'
                                   )
        st.text(f'{size_option}사이즈를 선택하셨습니다.')
        
    with tab3:
        deliver_option = st.selectbox('배달 유형 선택',
                                      options=['배달', '포장'],
                                      index=None,
                                      placeholder='배달 유형을 선택해주세요')
        if deliver_option == '배달':
             st.text('배달을 선택하셨습니다 자리로 배달하겠습니다')
             chair = st.text_input('자리를 입력해주세요')
             st.text(f'{chair}로 배달 가겠습니다')
        else :
            st.text('포장을 선택하셨습니다, 회사 지하1층 아이스크림집으로 10분후 와주세요!')
    
    if favor_option and size_option and deliver_option:
        st.success(f'선택하신 {size_option}사이즈의 {favor_option}맛을 {deliver_option}하겠습니다 ')

# ---- 함수 make_anal_tab 정의
# -- 파일명 : icecream_sales.csv 컬럼명 : 날짜,성별,연령대,맛,컵사이즈,개수,매출
def make_anal_tab():
    tab1, tab2 = st.tabs(['월별 매출 현황', '맛별 매출 현황'])
    
    with tab1:
        st.header('월별 매출 현황 입니다')
        st.plotly_chart(fig1(), use_container_width=True)
        
    with tab2:
        st.header('맛별 매출 현황 입니다')
        st.plotly_chart(fig2(), use_container_width=True)
    

# ---사이드바 정의    
st.sidebar.header('메뉴')
selected_menu = st.sidebar.selectbox(
    '메뉴 선택', ['메인 페이지','아이스크림 골라보기','매출 현황','설정']
)

# ---- 사이드바 내용 
if selected_menu == '메인 페이지':
    st.subheader('*또와요 아이스크림 메인 페이지 입니다.!!*')
    st.image(img,width=500,caption='ai 퍼블렉시티로 만든 귀여운 고양이 사진입니다. 실습용도이며 수익성의 목적을 띄고 있지 않음을 말씀드립니다. ' )

elif selected_menu == '아이스크림 골라보기':
    st.subheader('🍦*사내 복지 서비스* 🍦사내 아이스크림 배달 선택 메뉴입니다.!!')
    st.write('해당 구역에서 아이스크림 맛과 사이즈를 선택하시면 자리로 배달이 갑니다.!!')
    choice_icecream()
    
elif selected_menu == '매출 현황':
    st.subheader('*매출 현황 확인 메뉴입니다.!!*')
    st.write('관리자 메뉴로서 매출 현황을 확인할 수 있습니다.!!')
    make_anal_tab()

else:
    st.subheader('*설정 메뉴입니다*')
    st.write('앱의 설정을 바꿀 수 있습니다.')
