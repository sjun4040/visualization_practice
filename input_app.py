import streamlit as st
from PIL import Image
img = Image.open('./data/고양이_ai.png')

st.title('Title')
# 이미지 보기
st.image(img, caption='고양이',width=300 )
st.header('header')
st.subheader('subheader')

st.write('write 문장입니다.') #p
st.text('text 문장입니다.')
st.markdown(
    ''' 
    여기는 메인 텍스트 입니다.
    :red[ㄱ] :blue[ㅇ] :green[ㅇ] \n
    ** 굵게도 할 수 있고** 그리고 *이탤릭체*로도 표현 할 수 있어요
    '''
)
st.code(
    '''
    st.title('Title')
    st.header('header')
    ''',
    language='Python'
)

st.divider()

st.button('Hello',icon='🐍') #secondary type
st.button('Hello', type='primary')
st.button('Hello', type='tertiary', disabled=True, key=1)   
st.button('Good Bye', type='tertiary', width='content')

st.divider()

st.button('Reset', type='primary')

def button_write():
    st.write('버튼이 클릭되었습니다!')
    
st.button('activate', on_click=button_write)

clicked = st.button('activate2', type='primary')
if clicked:
    st.write('버튼2가 클릭되었습니다')
    
st.header('같은 버튼 여러개 만들기')

for i in range(0,5):
    key= i+1
    st.button(f'activated{key}', on_click=button_write, key={key})
    
st.divider()
