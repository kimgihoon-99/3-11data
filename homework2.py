# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 15:11:56 2025

@author: Admin
"""

import pandas as pd
import matplotlib.pyplot as plt

# 한글을 표기하기 위한 글꼴 변경(원도우, macOS에 대한 각각 처리)
from matplotlib import font_manager, rc
import platform

if platform.system() == 'Windows':
    path = 'c:/Windows/Fonts/malgun.ttf'
    font_name = font_manager.FontProperties(fname= path).get_name()
    rc('font', family = font_name)
elif platform.sytem() == 'Darwin':
    rc('font', family = 'AppleGothic')
else:
    print('Check your OS system')

# 1. 서울시 응답소 페이지 분석하기
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

# === 텍스트 파일 읽기 ===
file_path = '서울시_응답소.txt'  # 파일명 또는 경로 지정
with open(file_path, 'r', encoding='cp949') as file:
    raw_text = file.read()

# === 전처리 ===
# 1. 날짜, 숫자 제거
cleaned_text = re.sub(r'\d{4}-\d{2}-\d{2}', '', raw_text)  # 날짜 제거
cleaned_text = re.sub(r'\d+', '', cleaned_text)  # 숫자 제거

# 2. 특수문자, 불필요한 기호 제거
cleaned_text = re.sub(r'[^\w\s]', ' ', cleaned_text)

# === 형태소 분석 (Okt 사용) ===
okt = Okt()

# 명사만 추출
nouns = okt.nouns(cleaned_text)

# 한 글자는 너무 일반적이니 제거 (원하는 경우)
nouns = [noun for noun in nouns if len(noun) > 1]

# === 단어 빈도수 계산 ===
count = Counter(nouns)

# === 워드클라우드 생성 ===
font_path = 'c:/Windows/Fonts/malgun.ttf'  # 한글 폰트 경로 넣기!
wordcloud = WordCloud(
    font_path=font_path,  # 반드시 한글 폰트!
    width=800,
    height=800,
    background_color='white'
).generate_from_frequencies(count)

# === 시각화 ===
plt.figure(figsize=(10, 10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()


# 2 여고생이 가장 고치고 싶어하는 성형부위
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

# === 데이터 입력 ===
file_path = '성형상담.txt'  # 파일명 또는 경로 지정
with open(file_path, 'r', encoding='cp949') as file:
    raw_text = file.read()

# === 전처리 ===
# 숫자, 특수문자 제거
cleaned_text = re.sub(r'\d+', ' ', raw_text)  # 숫자 제거
cleaned_text = re.sub(r'[^\w\s]', ' ', cleaned_text)  # 특수문자 제거
cleaned_text = re.sub(r'\s+', ' ', cleaned_text)  # 다중 공백 제거

# === 형태소 분석 ===
okt = Okt()
nouns = okt.nouns(cleaned_text)

# === 불용어 리스트 설정 ===
stopwords = [
    '성형외과', '추천', '조회', '성형', '경우', '전문', '질문', '지식', '여고생',
    '성형수술', '방법', '의료', '수술', '상태', '가능', '고민', '의사', '한형일',
    '하시', '감사', '소음순', '고등학교', '건강', '하이닥', '-', '정도', '답변',
    '상담', '네이버', 'iN', '안녕', '내용', '본인', '김진왕', '나이', '문의',
    '방문', '대한협회', '입니다', '합니다', '그리고', '드리', '있습니다'
,'외과','직접', '따라서', '대해','전문의', '회수','지식인', '한형','하루', '때문','대한의사협회', '조금','부작용']

# === 불용어 제거 및 한 글자 명사 제외 ===
filtered_nouns = [noun for noun in nouns if noun not in stopwords and len(noun) > 1]

# === 단어 빈도수 계산 ===
count = Counter(filtered_nouns)

# === 상위 10개만 선택 ===
top_10_words = dict(count.most_common(20))

# === 워드클라우드 생성 ===
font_path = 'c:/Windows/Fonts/malgun.ttf'  # 한글 폰트 경로 업로드 후 절대경로 지정 필요!

wordcloud = WordCloud(
    font_path=font_path,
    width=800,
    height=800,
    background_color='white'
).generate_from_frequencies(top_10_words)

# === 시각화 ===
plt.figure(figsize=(10, 10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

# === 참고: 상위 10개 출력도 가능 ===
print("여고생이 자주 언급한 부위 Top 10")
for word, freq in top_10_words.items():
    print(f'{word}: {freq}회')


# 3. 성형수술 부작용

# === 데이터 입력 ===
file_path = '성형부작용.txt'  # 파일명 또는 경로 지정
with open(file_path, 'r', encoding='cp949') as file:
    raw_text = file.read()

# === 전처리 ===
# 숫자, 특수문자 제거
cleaned_text = re.sub(r'\d+', ' ', raw_text)  # 숫자 제거
cleaned_text = re.sub(r'[^\w\s]', ' ', cleaned_text)  # 특수문자 제거
cleaned_text = re.sub(r'\s+', ' ', cleaned_text)  # 다중 공백 제거

# === 형태소 분석 ===
okt = Okt()
nouns = okt.nouns(cleaned_text)

stopwords = [
    '성형외과', '대한의사협회', '상담', '내용', '선택', '충분',
    '네이버', '지식iN', 'iN', '답변', '안녕', '추천', '조회', '성형',
    '경우', '전문', '질문', '지식', '여고생', '성형수술', '방법', '의료',
    '수술', '상태', '가능', '고민', '의사', '한형일', '하시', '감사',
    '소음순', '고등학교', '건강', '하이닥', '-', '정도', '부작용', '정치',
    '필요', '때문', '과실', '문의', '재수', '사회', '발생', '문제',
    '정확', '과정', '생각', '관련'
]


# === 불용어 제거 및 한 글자 명사 제외 ===
filtered_nouns = [noun for noun in nouns if noun not in stopwords and len(noun) > 1]

# === 단어 빈도수 계산 ===
count = Counter(filtered_nouns)

# === 단어 빈도수 계산 ===
count = Counter(nouns)

# === 워드클라우드 생성 ===
font_path = 'c:/Windows/Fonts/malgun.ttf'  # 한글 폰트 경로 넣기!
wordcloud = WordCloud(
    font_path=font_path,  # 반드시 한글 폰트!
    width=800,
    height=800,
    background_color='white'
).generate_from_frequencies(count)

# === 시각화 ===
plt.figure(figsize=(10, 10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()


# 5 서울 명소 분석

from konlpy.tag import Okt
from collections import Counter
import re

# === 텍스트 예시 ===
file_path = '서울명소.txt'  # 파일명 또는 경로 지정
with open(file_path, 'r', encoding='cp949') as file:
    raw_text = file.read()

# === 사용자 정의 명사 리스트 ===
custom_words = [
    '북촌한옥마을', '삼청동', '하늘공원', '청계천', '올림픽공원',
    '국립중앙박물관', '창경궁', '강남', '홍대', '명동', '선유도공원',
    '전쟁기념관', '팔각정', '고궁', '낙산공원', '워커힐', '광화문',
    '센트럴시티', '국립현충원', '국립민속박물관', '치킨집', 'PC방',
    '스크린골프', '골프', '스몰비어', '애견', '노래방', '막창집', '카페', '치킨'
]

# === 사용자 단어들을 보호하기 위해 특수 문자로 감싸기 ===
for word in custom_words:
    raw_text = raw_text.replace(word, f'#{word}#')

# === 전처리 ===
cleaned_text = re.sub(r'\d+', ' ', raw_text)  # 숫자 제거
cleaned_text = re.sub(r'[^\w\s#]', ' ', cleaned_text)  # 특수문자 제거 (단, #는 유지)
cleaned_text = re.sub(r'\s+', ' ', cleaned_text)  # 다중 공백 제거

# === 형태소 분석 ===
okt = Okt()
nouns = okt.nouns(cleaned_text)

# === 특수문자로 감싼 단어는 원래대로 복원 ===
nouns = [noun.replace('#', '') for noun in nouns]

# === 불용어 리스트 ===
stopwords = [
    '블로그', '검색', 'blog', 'naver', 'com', 'me', '데이트', '약도', '사진', '야경',
    '여행', '근교', '이야기', '안녕', '도시', '관광', '벛꽃', '벚꽃', '코스', '오늘',
    '요한', '축제', '행복', '가볼만한곳', '걷기', 'km', '거리', '공원', '문화', '마을',
    '가을', '단풍', '나들이', '주말', '출사', '하게', '구경', '유명', '좋은곳', 'daum',
    '시간', 'cognos', 'eardoumi', 'tistory', '모습', 'ㅎㅎ', '사람', '이곳', '오랜만',
    '이태', 'netcognos', 'net', '트릭', '국내', '사이', '아침', '어제', '특별시', '장소',
    '날씨', '서울', '명소', '관광명소','일전', '소개', '추천']

# === 불용어 제거 ===
filtered_nouns = [noun for noun in nouns if noun not in stopwords and len(noun) > 1]

# === 빈도수 집계 ===
count = Counter(filtered_nouns)

from wordcloud import WordCloud
import matplotlib.pyplot as plt

font_path = 'c:/Windows/Fonts/malgun.ttf'  # 네가 업로드한 폰트 경로를 여기에!

wordcloud = WordCloud(
    font_path=font_path,
    background_color='white',
    width=800,
    height=800
).generate_from_frequencies(count)

plt.figure(figsize=(10, 10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

















































