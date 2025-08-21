import streamlit as st
from PIL import Image

# sidebar, columns, tabs, expander
img = Image.open('./data/고양이_ai.png')
img1 = Image.open('./data/minidog.jpg')
st.title("스트림릿 앱 페이지 구성하기")

col1, col2 = st.columns(2)

def make_anal_tab():
    tab1, tab2, tab3 = st.tabs(['차트','데이터','설정'])
    with tab1:
        st.subheader('차트 탭')
        st.bar_chart({'데이터': [1,2,3,4,5]})
    
    with tab2:
        st.subheader('데이터 탭')
        st.bar_chart({'기준': ['a','b','c','d','e'], '값' :[1,2,3,4,5]})
    
    with tab3:
        st.subheader('설정 탭')
        check = st.checkbox('자동 업데이트 활성화 여부')
        if check:
            st.write('활성화')
        st.slider('업데이트 주기 (sec)', 1,60,10)
    
st.sidebar.header('웰컴 메뉴')
selected_menu = st.sidebar.selectbox(
    '메뉴 선택', ['메인','분석','설정']
)

    
if selected_menu == '메인':
    st.subheader('*메인 페이지*')
    st.write('환영합니다.!!')
    with col1:
        st.image(img, caption='작은 고양이',width=300)
    with col2:
        st.image(img1, caption='작은 강아지', width=300)
elif selected_menu == '분석':
    st.subheader('*분석 보고서*')
    st.write('해당 구역에서 데이터를 선택하실 수 있습니다.!!')
    
    make_anal_tab()
else:
    st.subheader('*설정 변경*')
    st.write('앱 설정을 변경할 수 있습니다.!!')

if st.sidebar.button('선택'):
    st.sidebar.write('선택을 클릭하셨습니다.')

# 슬라이드바 추가 0~100, 50
    st.slider('선택', 0,100,50)

st.divider()

# 확장영역 추가
st.header('익스팬더 추가')

with st.expander('숨김 영역'):
    st.write('여기는 보이지 않습니다. 클릭해야 보입니다.')
