import streamlit as st
from streamlit_sortables import sort_items
import random

# --- 1. 기본 설정 ---
st.set_page_config(page_title="국어 지문 순서 맞추기", page_icon="📖", layout="wide")

st.title("🧩 국어 지문 순서 맞추기")
st.info("지문을 입력한 뒤, 섞여 있는 문장을 마우스로 끌어서 원래 순서대로 배열해 보세요!", icon="💡")

# --- 2. 사이드바 설정 ---
with st.sidebar:
    st.header("⚙️ 설정")
    # '새로 섞기' 버튼을 사이드바로 이동시켜 로직 충돌을 방지합니다.
    if st.button("🔄 새로 섞기", use_container_width=True):
        # 'shuffled_sentences'와 'sorted_items_key'를 session_state에서 삭제하여 초기화
        if 'shuffled_sentences' in st.session_state:
            del st.session_state['shuffled_sentences']
        if 'sorted_items_key' in st.session_state:
            # sort_items 위젯의 키를 변경하여 강제로 다시 그리게 만듭니다.
            st.session_state.sorted_items_key += 1
        st.rerun() # 앱을 새로고침하여 변경사항을 즉시 적용

st.divider()

# --- 3. 지문 입력 ---
st.subheader("1. 지문을 입력하세요")
default_text = "다람쥐는 도토리를 좋아합니다. 겨울이 오기 전에 도토리를 숨깁니다. 하지만 가끔은 어디에 숨겼는지 잊어버리기도 합니다. 덕분에 싹이 터서 나무가 자라납니다."
text_input = st.text_area(
    "교과서 지문을 복사해서 넣어주세요:",
    default_text,
    height=150
)

# --- 4. 문장 처리 및 섞기 (가장 중요한 로직) ---
# session_state에 'sorted_items_key'가 없으면 초기화
if 'sorted_items_key' not in st.session_state:
    st.session_state.sorted_items_key = 0

# 섞인 문장 목록이 없으면 새로 생성
if 'shuffled_sentences' not in st.session_state and text_input:
    original_sentences = [s.strip() + "." for s in text_input.split('.') if s.strip()]
    
    # 원본 문장 목록을 session_state에 저장 (정답 비교용)
    st.session_state.original_sentences = original_sentences
    
    shuffled = original_sentences[:] # 원본을 복사하여 섞기
    random.shuffle(shuffled)
    
    # 섞인 문장 목록을 session_state에 저장
    st.session_state.shuffled_sentences = shuffled

# --- 5. 드래그 앤 드롭 화면 ---
# 섞인 문장이 있을 때만 화면에 표시
if 'shuffled_sentences' in st.session_state:
    st.subheader("2. 문장을 끌어서 순서를 바꾸세요")
    
    # sort_items에 고유한 key를 부여하여 위젯의 상태를 안정적으로 관리
    sorted_items = sort_items(
        st.session_state.shuffled_sentences, 
        key=f"sortable_list_{st.session_state.sorted_items_key}"
    )

    st.divider()

    # --- 6. 정답 확인 로직 ---
    if st.button("✅ 정답 확인하기", use_container_width=True):
        # session_state에 저장된 원본(정답)과 사용자가 정렬한 결과를 비교
        if sorted_items == st.session_state.original_sentences:
            st.balloons()
            st.success("🎉 우와! 완벽한 정답입니다. 문장의 흐름을 아주 잘 파악했네요!")
        else:
            st.error("아쉽지만, 아직 순서가 맞지 않아요. 아래 '원문 정답'과 비교하며 다시 한번 생각해볼까요?")
            # 틀렸을 경우 정답 공개
            st.subheader("✨ 원문 정답")
            # 번호와 함께 원문 순서를 보여줌
            original_text_display = "\n\n".join(
                [f"**{i+1}.** {s}" for i, s in enumerate(st.session_state.original_sentences)]
            )
            st.markdown(original_text_display)
