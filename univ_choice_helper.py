import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# JSON 파일 경로
DATA_FILE = "data.json"

# 데이터 불러오기
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_json(DATA_FILE)
    return pd.DataFrame(columns=["날짜", "1순위", "2순위", "3순위", "학과"])

# 데이터 저장
def save_data(df):
    df.to_json(DATA_FILE, force_ascii=False)

# 세션 상태에 데이터 로딩
if "data" not in st.session_state:
    st.session_state.data = load_data()

st.title("'가은이'의 목표대학 탐방기:cityscape::sparkles:")

# 대학 정보 데이터프레임
df = pd.DataFrame({
    '대학': ["가톨릭대", "경기대", "광운대", "단국대", "서울여대", "아주대", "연세대", "인하대"],
    '사진': [
        '<img src="https://search.pstatic.net/common/?src=http%3A%2F%2Fimgnews.naver.net%2Fimage%2F5312%2F2024%2F07%2F24%2F0000276511_001_20240724102213680.png&type=l340_165">',
        '<img src="https://search.pstatic.net/common/?src=http%3A%2F%2Fimgnews.naver.net%2Fimage%2F003%2F2021%2F05%2F25%2FNISI20201215_0000656602_web_20201215155749_20210525154010763.jpg&type=l340_165">',
        '<img src="https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMjA1MThfNjkg%2FMDAxNjUyODU1ODgxODQ3.o6AYz3YGvos7n3yBDh7J9VAN9PfKilowp2H3gfWuizYg.JENHy-sSwiZx-WXY81o0sV0x50VmhNAtly6aU63nOGsg.PNG.17anlllab%2Fimage.png&type=a340">',
        '<img src="https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2F20161014_106%2Fmelone83_1476420856103VOc1T_JPEG%2F2016-10-13-14-31-16.jpg&type=a340">',
        '<img src="https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyNDEwMTJfMjEy%2FMDAxNzI4Njg3OTM5NzYy.wqbAfgvSMyWafNy578esMJ8XCbziQCAQaUnTQfd9ga8g.OqW5-5DZEeMSRh0PT-A9lbxx_zSBUOpuUSBj06rBbeQg.PNG%2Fimage.png&type=a340">',
        '<img src="https://search.pstatic.net/sunny/?src=https%3A%2F%2Fimg3.dcinside.com%2FPUD%2Fba%2Fjw0%2FIMG%2F20091017%2F1255784929_200910172209538987250901_0.jpg&type=a340">',
        '<img src="https://search.pstatic.net/sunny/?src=https%3A%2F%2Fcdnweb01.wikitree.co.kr%2Fwebdata%2Feditor%2F202407%2F01%2Fimg_20240701182116_632566ab.webp&type=a340">',
        '<img src="https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMzExMjBfMjkw%2FMDAxNzAwNDYzMzU1MzQ3.tL8QjwmtxLNiI08Mq6ZVvCugBoNJjUcav4hT0r90oUAg.wakuV9Q7KLY_h5dobCmJSUP0WcZS0uvOrLzMmL0oyFAg.JPEG.cmstorygo%2F3.jpg&type=l340_165">'
    ],
    '위치': [
        "경기도 부천시 원미구 지봉로 43", "경기도 수원시 영통구 광교산로 154-42",
        "서울특별시 노원구 광운로 20", "경기도 용인시 수지구 죽전로 152",
        "서울특별시 노원구 화랑로 621", "경기도 수원시 영통구 월드컵로 206",
        "서울특별시 서대문구 연세로 50", "인천광역시 미추홀구 인하로 100"
    ],
    '외국 관련 학과 현황': [
        "영어영문학부, 중국언어문화학과, 일어일본문화학과, 국제학부",
        "글로벌어문학부(독일어, 프랑스어, 일본어, 중국어, 러시아어), 정치외교학전공",
        "영어산업학과, 동북아문화산업학부, 국제학부, 국제통상학부",
        "영미인문학과, 무역학과, 정치외교학과",
        "영어영문학과, 중어중문학과, 일어일문학과",
        "자유전공학부, 정치외교학과, 사회학과",
        "정치외교학과, 사회학과, 불어불문학과, 독어독문학과, 영어영문학과, 노어노문학과, 중어중문학과",
        "중국학과, 일본언어문화학과, 영미유럽인문융합학부, 정치외교학과, 국제통상학과"
    ]})
# 학교별 학과 매핑 (학교 -> 학과 목록)
school_to_major = {
    "가톨릭대": ["영어영문학부", "중국언어문화학과", "일어일본문화학과", "국제학부"],
    "경기대": ["글로벌어문학부(독일어, 프랑스어, 일본어, 중국어, 러시아어)", "정치외교학전공"],
    "광운대": ["영어산업학과", "동북아문화산업학부", "국제학부", "국제통상학부"],
    "단국대": ["영미인문학과", "무역학과", "정치외교학과"],
    "서울여대": ["영어영문학과", "중어중문학과", "일어일문학과"],
    "아주대": ["자유전공학부", "정치외교학과", "사회학과"],
    "연세대": ["정치외교학과", "사회학과", "불어불문학과", "독어독문학과", "영어영문학과", "노어노문학과", "중어중문학과"],
    "인하대": ["중국학과", "일본언어문화학과", "영미유럽인문융합학부", "정치외교학과", "국제통상학과"]
}

# 표 출력 함수
urls = [
    "https://www.catholic.ac.kr/",
    "https://www.kyonggi.ac.kr/",
    "https://www.kw.ac.kr/",
    "https://www.dankook.ac.kr/",
    "https://www.swu.ac.kr/",
    "https://www.ajou.ac.kr/",
    "https://www.yonsei.ac.kr/",
    "https://www.inha.ac.kr/"
]

df['학교 홈페이지'] = [f'<a href="{url}" target="_blank">{url}</a>' for url in urls]
def df_to_html_table(df):
    html = '''
    <style>
    .responsive-table-container {
        width: 100%;
        overflow-x: auto;
        margin-bottom: 1em;
    }
    table.responsive-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 1em;
        min-width: 600px;
        max-width: 100%;
    }
    table.responsive-table th, table.responsive-table td {
        text-align: center;
        padding: 10px 6px;
        border: 1px solid #ddd;
        vertical-align: middle;
        word-break: break-word;
        font-size: 1em;
    }
    table.responsive-table th {
        background: #f5f6fa;
        font-weight: bold;
    }
    img {
        max-width: 60px;
        height: auto;
        display: block;
        margin: 0 auto;
    }
    @media screen and (max-width: 600px) {
        table.responsive-table {
            font-size: 0.85em;
            min-width: 400px;
        }
        img {
            max-width: 36px;
        }
        table.responsive-table th, table.responsive-table td {
            padding: 6px 2px;
            font-size: 0.85em;
        }
    }
    </style>
    <div class="responsive-table-container">
    <table class="responsive-table">
    '''
    # 헤더
    html += '<tr>'
    for col in df.columns:
        html += f'<th>{col}</th>'
    html += '</tr>'
    # 데이터
    for row in df.values:
        html += '<tr>'
        for val in row:
            html += f'<td>{val}</td>'
        html += '</tr>'
    html += '</table></div>'
    return html

# 출력
st.markdown(df_to_html_table(df), unsafe_allow_html=True)
st.write("----")

# 입력 파트
st.markdown("### ✍️ 원하는 대학과 학과를 입력해주세요 (1~3순위)")

col1, col2, col3 = st.columns(3)
with col1:
    univ1 = st.selectbox(":first_place_medal: 1순위 대학", df['대학'])
    major1 = st.selectbox(f"{univ1} 학과", school_to_major[univ1])

with col2:
    univ2 = st.selectbox(":second_place_medal: 2순위 대학", df['대학'])
    major2 = st.selectbox(f"2순위 {univ2} 학과", school_to_major[univ2])

with col3:
    univ3 = st.selectbox(":third_place_medal: 3순위 대학", df['대학'])
    major3 = st.selectbox(f"3순위 {univ3} 학과", school_to_major[univ3])

if st.button("입력"):
    if univ1 and univ2 and univ3 and major1 and major2 and major3:
        new_row = {
            "날짜": datetime.now().strftime('%Y-%m-%d %H:%M'),
            "1순위 대학": univ1,
            "1순위 학과": major1,
            "2순위 대학": univ2,
            "2순위 학과": major2,
            "3순위 대학": univ3,
            "3순위 학과": major3
        }
        st.session_state.data = pd.concat(
            [st.session_state.data, pd.DataFrame([new_row])],
            ignore_index=True
        )
        save_data(st.session_state.data)
        st.rerun()

# 입력 내역 표시
st.markdown("### 📌 입력 내역")
for idx, row in st.session_state.data.iterrows():
    cols = st.columns([2, 2, 2, 2, 1])
    cols[0].write(f"입력 날짜: {row['날짜']}")
    cols[1].write(f"1순위: {row['1순위 대학']} - {row['1순위 학과']}")
    cols[2].write(f"2순위: {row['2순위 대학']} - {row['2순위 학과']}")
    cols[3].write(f"3순위: {row['3순위 대학']} - {row['3순위 학과']}")
    if cols[4].button("삭제", key=f"del_{idx}"):
        st.session_state.data = st.session_state.data.drop(idx).reset_index(drop=True)
        save_data(st.session_state.data)
        st.rerun()
