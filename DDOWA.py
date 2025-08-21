import streamlit as st
from PIL import Image
import datetime

month = datetime.datetime.now().month
img = Image.open('./data/그림1.png')

col1, col2 = st.columns(2)  # col1에는 이번 달 매출, col2에는 어떤 종류의 맛이 잘팔리는 지 

with col1:
    st.metric(
        f'{month}월 매출 현황',
        value='10만원',
        delta='+3'
    )

with col2:
    st.metric(
        f'{month}월의 맛',
        value='초코',
        delta='이번 달 초코 맛 선택 수 : {} '
        
    )
  
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

def make_anal_tab():
    tab1, tab2 = st.tabs(['매출 현황', '아이스크림 관리 창고 온도 현황'])
    
    
st.sidebar.header('메뉴')
selected_menu = st.sidebar.selectbox(
    '메뉴 선택', ['메인 페이지','아이스크림 골라보기','매출 현황','설정']
)

if selected_menu == '메인 페이지':
    st.subheader('*또와요 아이스크림 메인 페이지 입니다.!!*')
    st.image(img,width=500,caption='파스쿠치 사이트에서 갖고 온 사진으로 이름만 변경하였습니다 해당 이미지는 실습용 목적으로 사용하는 것이며 수익적인 목적을 가지고 사용하지 않습니다' )

elif selected_menu == '아이스크림 골라보기':
    st.subheader('🍦*사내 복지 서비스* 🍦사내 아이스크림 배달 선택 메뉴입니다.!!')
    st.write('해당 구역에서 아이스크림 맛과 사이즈를 선택하시면 자리로 배달이 갑니다.!!')
    choice_icecream()
    
elif selected_menu == '매출 현황':
    st.subheader('*매출 현황 확인 메뉴입니다.!!*')
    st.write('관리자 메뉴로 매출 현황을 확인할 수 있습니다.!!')

else:
    st.subheader('*설정 메뉴입니다*')
    st.write('앱의 설정을 바꿀 수 있습니다.')
