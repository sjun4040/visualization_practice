# --- 라이브러리 정의
import streamlit as st
from PIL import Image
import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ------ 정의 
img = Image.open('고양이_ai.png')
df_ice = pd.read_csv('icecream_sales.csv')

# --- 테마 함수 
def apply_theme():
    theme = st.session_state.get('theme', '라이트')
    
    if theme == '다크':
        st.markdown("""
        <style>
        /* 전체 앱 배경 */
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        
        /* 사이드바 */
        .stSidebar {
            background-color: #262730;
        }
        .stSidebar .stSelectbox label {
            color: #fafafa;
        }
        
        /* 메인 컨텐츠 영역 */
        .main .block-container {
            background-color: #0e1117;
            color: #fafafa;
        }
        
        /* 헤더와 서브헤더 */
        h1, h2, h3, h4, h5, h6 {
            color: #fafafa !important;
        }
        
        /* 일반 텍스트 */
        .stText, .stMarkdown, p, span {
            color: #fafafa !important;
        }
        
        /* 셀렉트박스 */
        .stSelectbox > div > div {
            background-color: #262730;
            color: #fafafa;
            border: 1px solid #4a4a4a;
        }
        
        /* 텍스트 입력 */
        .stTextInput > div > div > input {
            background-color: #262730;
            color: #fafafa;
            border: 1px solid #4a4a4a;
        }
        
        /* 탭 */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #262730;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #262730;
            color: #fafafa;
        }
        
        /* 메트릭 카드 */
        .metric-container {
            background-color: #1e1e1e;
            border: 1px solid #4a4a4a;
            border-radius: 8px;
            padding: 10px;
        }
        
        /* 체크박스와 라디오 버튼 */
        .stCheckbox label, .stRadio label {
            color: #fafafa !important;
        }
        
        /* 파일 업로더 */
        .stFileUploader label {
            color: #fafafa !important;
        }
        
        /* 날짜 입력 */
        .stDateInput label {
            color: #fafafa !important;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .stApp {
            background-color: #ffffff;
            color: #262626;
        }
        .stSidebar {
            background-color: #f0f2f6;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #262626 !important;
        }
        .stText, .stMarkdown, p, span {
            color: #262626 !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
# --- 분석용 시각화 코드
# 날짜 타입 변환
df_ice['날짜'] = pd.to_datetime(df_ice['날짜'])


# 1. 월별 매출 합계
df_ice['월'] = df_ice['날짜'].dt.month
month = datetime.datetime.now().month 
month_sales_df = df_ice.groupby('월')['매출'].sum().reset_index()
month_sales_df['월_str'] = month_sales_df['월'].astype(str)


# 이번 달 매출 계산 (전역 변수로 정의)
this_month_sales = df_ice[df_ice['월'] == month]['매출'].sum()


def fig1():
    fig1 = px.bar(
        month_sales_df,
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


# ---- 대시보드 상단 메트릭 계산
goal_percent = 89
profit_percent = 12 


# col1 필요 함수 - 전월 대비 매출 변화 계산
before_month = month - 1 if month > 1 else 12
before_month_sales = df_ice[df_ice['월'] == before_month]['매출'].sum()
delta_sales = this_month_sales - before_month_sales
delta_str = f"{delta_sales:+,}원"


# col2 필요 함수 - 이번 달 가장 많이 팔린 맛
flavor_counts = df_ice[df_ice['월'] == month].groupby('맛')['개수'].sum()
best_flavor = flavor_counts.idxmax() if not flavor_counts.empty else "데이터 없음"
best_flavor_count = flavor_counts.max() if not flavor_counts.empty else 0


def main_p():
    col1, col2, col3, col4 = st.columns(4)  # 컬럼 정의를 함수 내부로 이동
    
    with col1:
        st.metric(
            f'{month}월 매출 현황',
            value=(f'{this_month_sales:,}원'),
            delta=delta_str
        )

    with col2:
        st.metric(
            f'{month}월의 맛',
            value=(f'{best_flavor}'),
            delta=(f'{best_flavor} 맛 구매 수 : {best_flavor_count} ')
        )

    with col3:
        st.markdown("##### 매출 현황")
        fig_goal = go.Figure(go.Pie(
            values=[goal_percent, 100-goal_percent],
            hole=0.7,
            marker_colors=['#de4343','#e2e2e2'],
            sort=False,
            direction='clockwise',
            textinfo='none'
        ))
        fig_goal.update_layout(
            showlegend=False,
            margin=dict(t=0,b=0,l=0,r=0),
            annotations=[dict(
                text=f"<b>목표 달성률<br>{goal_percent:.1f}%</b>",
                x=0.5, y=0.5, font_size=18, showarrow=False
            )],
            width=210, height=210
        )
        st.plotly_chart(fig_goal, use_container_width=True)

    with col4:
        st.markdown("##### 수익 현황")
        fig_profit = go.Figure(go.Pie(
            values=[profit_percent, 100-profit_percent],
            hole=0.7,
            marker_colors=['#56ba47','#e2e2e2'],
            sort=False,
            direction='clockwise',
            textinfo='none'
        ))
        fig_profit.update_layout(
            showlegend=False,
            margin=dict(t=0,b=0,l=0,r=0),
            annotations=[dict(
                text=f"<b>수익률<br>{profit_percent}%</b>",
                x=0.5, y=0.5, font_size=18, showarrow=False
            )],
            width=210, height=210
        )
        st.plotly_chart(fig_profit, use_container_width=True)
           

# --- 함수 choice_icecream
def choice_icecream():
    tab1, tab2, tab3 = st.tabs(['맛 선택', '컵 사이즈 선택', '배달 여부'])
    
    with tab1:
        favor_option = st.selectbox('맛 선택',
                     options= ['초코','바닐라','딸기','녹차','커피'],
                     index=None,
                     placeholder='맛을 선택해주세요'
                     )
        if favor_option:
            st.text(f'{favor_option}을 선택하셨습니다.')

    with tab2:
        size_option = st.selectbox('컵 사이즈 선택', 
                                   options = ['소','중','대'],
                                   index=None,
                                   placeholder='컵 사이즈를 선택해주세요'
                                   )
        if size_option:
            st.text(f'{size_option}사이즈를 선택하셨습니다.')
        
    with tab3:
        deliver_option = st.selectbox('배달 유형 선택',
                                      options=['배달', '포장'],
                                      index=None,
                                      placeholder='배달 유형을 선택해주세요')
        if deliver_option == '배달':
             st.text('배달을 선택하셨습니다 자리로 배달하겠습니다')
             chair = st.text_input('자리를 입력해주세요')
             if chair:
                 st.text(f'{chair}로 배달 가겠습니다')
        elif deliver_option == '포장':
            st.text('포장을 선택하셨습니다, 회사 지하1층 아이스크림집으로 10분후 와주세요!')
    if all ([favor_option, deliver_option, size_option]):
        st.caption(f'{size_option}사이즈의 {favor_option}맛 아이스크림을 {deliver_option}해드리겠습니다 ')
    
    # 모든 선택이 완료되었을 때만 성공 메시지 표시
    favor_option = st.session_state.get('favor_option')
    size_option = st.session_state.get('size_option') 
    deliver_option = st.session_state.get('deliver_option')
    
    if favor_option and size_option and deliver_option:
        st.success(f'선택하신 {size_option}사이즈의 {favor_option}맛을 {deliver_option}하겠습니다 ')


# 설정 메뉴 연동 
def setting():
    theme = st.radio("테마 선택", ["라이트", "다크"], 
                     index=0 if st.session_state.get('theme', '라이트') == '라이트' else 1)
    st.session_state['theme'] = theme 
    uploaded_file = st.file_uploader("매출 데이터 업로드(CSV)", type="csv")
    if uploaded_file:
        st.success("파일 업로드 완료!")
    st.info("문의: DDOWAU@icecream.com / 버전: 1.1.0")
    

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

# 테마 적용
apply_theme()

# ---- 사이드바 내용 
if selected_menu == '메인 페이지':
    st.subheader('*또와요 아이스크림 메인 페이지 입니다.!!*')
    main_p()
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
    setting()   