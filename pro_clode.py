import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import uuid

# 페이지 설정
st.set_page_config(
    page_title="톡톡 상담 지원 시스템",
    page_icon="💬",
    layout="wide"
)

# CSS 스타일링
st.markdown("""
<style>
    .main-header {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        margin: 30px 0;
        color: #2E7D32;
    }
    
    .login-container {
        max-width: 400px;
        margin: 50px auto;
        padding: 40px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }
    
    .counselor-card {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
        margin: 10px 0;
        border: 1px solid #e0e0e0;
    }
    
    .consultation-info {
        background: #E8F5E8;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        border: 1px solid #c8e6c9;
    }
    
    .chat-message {
        padding: 12px 16px;
        margin: 8px 0;
        border-radius: 12px;
        max-width: 70%;
        word-wrap: break-word;
    }
    
    .user-message {
        background: #E3F2FD;
        margin-left: 30%;
        border: 1px solid #bbdefb;
    }
    
    .counselor-message {
        background: #F1F8E9;
        margin-right: 30%;
        border: 1px solid #dcedc8;
    }
    
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        border: none;
        padding: 10px;
        font-weight: 500;
    }
    
    .header-info {
        background: #f5f5f5;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 샘플 데이터 생성 함수
@st.cache_data
def generate_sample_data():
    names = ["김민준", "이서연", "박도윤", "정시우", "최예은", "김하준", "이서진", "박건우", "정나연", "최시은",
             "김준서", "이채원", "박지후", "정서율", "최민서", "김하늘", "이도현", "박유진", "정은우", "최소연",
             "김지안", "이하은", "박민준", "정채은", "최연우", "김소율", "이준혁", "박시연", "정하린", "최도훈"]
    
    consultation_topics = [
        "대출 조건 관련 문의", "신용카드 발급 문의", "적금 상품 안내", "주택담보대출 상담", "개인신용 문의",
        "보험 상품 문의", "투자 상품 안내", "해외송금 문의", "인터넷뱅킹 오류", "모바일앱 사용법",
        "계좌개설 문의", "비밀번호 재설정", "카드 분실 신고", "연체 관련 상담", "금리 문의",
        "펀드 투자 상담", "외환 거래 문의", "기업대출 상담", "퇴직연금 문의", "ISA 계좌 문의",
        "체크카드 발급", "통장 재발급", "이체한도 변경", "공과금 자동이체", "급여이체 설정",
        "부동산 담보대출", "전세자금대출", "사업자대출", "학자금대출", "신혼부부대출"
    ]
    
    data = []
    for i in range(35):
        consultation_date = datetime.now() - timedelta(days=random.randint(0, 90))
        data.append({
            "상담자": random.choice(names),
            "상담 내용 요약": random.choice(consultation_topics),
            "상담일": consultation_date.strftime("%Y-%m-%d"),
            "상담 시간": f"{random.randint(9, 17):02d}:{random.randint(0, 59):02d}",
            "상담 ID": str(uuid.uuid4())[:8]
        })
    
    return pd.DataFrame(data)

# 상세 상담 내용 생성
def generate_consultation_detail(summary):
    conversations = [
        {
            "speaker": "고객",
            "message": f"안녕하세요 상담사님. {summary}에 대해 문의드립니다."
        },
        {
            "speaker": "상담사",
            "message": "안녕하세요. 대출 조건이 어떻게 되는지 궁금하시군요."
        },
        {
            "speaker": "고객", 
            "message": "네, 고객님. 소득 증빙과 신용 등급에 따라 조건이 달라질 수 있습니다. 자세한 안내를 도와드리겠습니다."
        }
    ]
    return conversations

# 메모 관리 함수들
def save_memo(consultation_id, memo_text):
    st.session_state.memos[consultation_id] = {
        'text': memo_text,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")
    }

def get_memo(consultation_id):
    return st.session_state.memos.get(consultation_id, {'text': '', 'timestamp': ''})

def show_memo_popup():
    if st.session_state.show_memo_modal:
        with st.expander("📝 메모", expanded=True):
            consultation_id = st.session_state.selected_consultation['상담 ID'] if st.session_state.selected_consultation else 'general'
            current_memo = get_memo(consultation_id)
            
            memo_text = st.text_area(
                "메모 내용",
                value=current_memo['text'],
                height=150,
                key=f"memo_{consultation_id}"
            )
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("저장", type="primary", key=f"save_memo_{consultation_id}"):
                    save_memo(consultation_id, memo_text)
                    st.success("메모가 저장되었습니다!")
                    st.session_state.show_memo_modal = False
                    st.rerun()
            
            with col2:
                if st.button("닫기", key=f"close_memo_{consultation_id}"):
                    st.session_state.show_memo_modal = False
                    st.rerun()
            
            if current_memo['timestamp']:
                st.caption(f"마지막 저장: {current_memo['timestamp']}")

# 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'counselor_id' not in st.session_state:
    st.session_state.counselor_id = None
if 'sample_data' not in st.session_state:
    st.session_state.sample_data = generate_sample_data()
if 'selected_consultation' not in st.session_state:
    st.session_state.selected_consultation = None
if 'memos' not in st.session_state:
    st.session_state.memos = {}
if 'show_memo_modal' not in st.session_state:
    st.session_state.show_memo_modal = False

# 로그인 페이지
def login_page():
    st.markdown('<div class="main-header">💬 톡톡 상담 지원 시스템</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.container():
            st.markdown("---")
            # 캐릭터 이미지
            st.markdown('<div style="text-align: center; font-size: 60px; margin: 20px 0;">🤖</div>', unsafe_allow_html=True)
            
            st.markdown('<p style="text-align: center; color: #666; margin-bottom: 30px; font-size: 18px;">상담사 로그인</p>', unsafe_allow_html=True)
            
            counselor_number = st.text_input("", placeholder="상담사 번호", help="상담사 번호를 입력하세요")
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                if st.button("상담 시작", type="primary"):
                    if counselor_number.strip():
                        st.session_state.counselor_id = counselor_number
                        st.session_state.page = 'main'
                        st.rerun()
                    else:
                        st.error("상담사 번호를 입력해주세요.")
            st.markdown("---")

# 메인 페이지
def main_page():
    # 헤더 정보
    st.markdown('<div class="header-info">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        st.markdown(f"**👤 상담자:** {st.session_state.counselor_id}")
    
    with col2:
        st.markdown(f"**📅 날짜:** {datetime.now().strftime('%Y/%m/%d')}")
    
    with col3:
        if st.button("상담자 메모"):
            st.session_state.show_memo_modal = True
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 검색 기능
    col1, col2 = st.columns([5, 1])
    
    with col1:
        search_term = st.text_input("🔍", placeholder="상담 이력 검색", label_visibility="collapsed")
    
    with col2:
        if st.button("📅"):
            st.info("날짜 필터")
    
    # 검색 필터링
    if search_term:
        filtered_data = st.session_state.sample_data[
            (st.session_state.sample_data['상담자'].str.contains(search_term, case=False, na=False)) |
            (st.session_state.sample_data['상담 내용 요약'].str.contains(search_term, case=False, na=False))
        ]
    else:
        filtered_data = st.session_state.sample_data
    
    # 상담 이력 목록
    st.markdown("### 상담 이력")

    for idx, row in filtered_data.head(10).iterrows():
        with st.container():
            st.markdown('<div class="counselor-card">', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([2, 4, 1])
            
            with col1:
                st.markdown(f"**상담자**")
                st.markdown(f"{row['상담자']}")
            
            with col2:
                st.markdown(f"**상담 내용 요약**")
                st.markdown(f"{row['상담 내용 요약']}")
                
                # 메모가 있으면 표시
                memo = get_memo(row['상담 ID'])
                if memo['text']:
                    st.markdown(f"📝 *{memo['text'][:30]}{'...' if len(memo['text']) > 30 else ''}*")
            
            with col3:
                if st.button("상세", key=f"detail_{idx}"):
                    st.session_state.selected_consultation = row
                    st.session_state.page = 'detail'
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # 하단 버튼들
    st.markdown("---")
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
    
    with col1:
        if st.button("➕ 새 상담", type="primary"):
            st.session_state.page = 'new_consultation'
            st.rerun()
    
    with col4:
        if st.button("⚙️ 로그아웃"):
            st.session_state.counselor_id = None
            st.session_state.page = 'login'
            st.rerun()
    
    # 메모 팝업 표시
    show_memo_popup()

# 새 상담 페이지
def new_consultation_page():
    # 헤더
    st.markdown('<div class="header-info">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        st.markdown(f"**👤 상담자:** {st.session_state.counselor_id}")
    
    with col2:
        st.markdown(f"**📞 상담자:** 박상준")
    
    with col3:
        st.markdown(f"**📅 날짜:** {datetime.now().strftime('%Y/%m/%d')} **⏰ 시간:** {datetime.now().strftime('%H:%M')}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 자동 서비스 정보
    st.markdown("---")
    st.markdown('<div style="text-align: center; background: #E8F5E8; padding: 20px; border-radius: 10px; margin: 20px 0;">', unsafe_allow_html=True)
    st.markdown('## 톡톡\'s Auto Service')
    st.markdown('<p style="color: #666; font-size: 16px;">키워드 확인: 대기중</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 캐릭터
    st.markdown('<div style="text-align: center; font-size: 100px; margin: 40px 0;">😊</div>', unsafe_allow_html=True)
    
    # 상담 종료 버튼
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col2:
        if st.button("상담 종료", type="primary"):
            st.session_state.page = 'main'
            st.rerun()

# 상담 상세 페이지
def consultation_detail_page():
    if st.session_state.selected_consultation is None:
        st.session_state.page = 'main'
        st.rerun()
        return
    
    consultation = st.session_state.selected_consultation
    
    # 헤더
    st.markdown('<div class="header-info">', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 2])
    
    with col1:
        st.markdown(f"**👤 상담자:** {consultation['상담자']}")
    
    with col2:
        st.markdown(f"**📅 상담일:** {consultation['상담일']}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 상담 요약 정보
    st.markdown('<div class="consultation-info">', unsafe_allow_html=True)
    st.markdown("### 상담 요약 정보")
    st.markdown(f"**상담 요약:** {consultation['상담 내용 요약']}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 메모 섹션 추가
    memo = get_memo(consultation['상담 ID'])
    st.markdown('<div class="consultation-info">', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown("### 📝 상담 메모")
        if memo['text']:
            st.markdown(f"**메모:** {memo['text']}")
            st.caption(f"작성일: {memo['timestamp']}")
        else:
            st.markdown("*저장된 메모가 없습니다.*")

    with col2:
        if st.button("메모 편집", key="edit_memo_detail"):
            st.session_state.show_memo_modal = True
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # 대화 내용
    st.markdown("---")
    st.markdown("### 상담 내용")
    
    conversations = generate_consultation_detail(consultation['상담 내용 요약'])
    
    for conv in conversations:
        if conv['speaker'] == '고객':
            st.markdown(f'<div class="chat-message user-message"><strong>박상준</strong><br>{conv["message"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message counselor-message"><strong>김민준</strong><br>{conv["message"]}</div>', unsafe_allow_html=True)
    
    # 하단 버튼
    st.markdown("---")
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col2:
        if st.button("목록으로", type="primary"):
            st.session_state.page = 'main'
            st.rerun()
    
    # 메모 팝업 표시
    show_memo_popup()

# 메인 실행 함수
def main():
    if st.session_state.page == 'login':
        login_page()
    elif st.session_state.page == 'main':
        main_page()
    elif st.session_state.page == 'new_consultation':
        new_consultation_page()
    elif st.session_state.page == 'detail':
        consultation_detail_page()

# 앱 실행
if __name__ == "__main__":
    main()