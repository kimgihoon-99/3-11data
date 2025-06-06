# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 14:17:37 2025

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


# 6. 노무현 대통령 연설문 분석
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from konlpy.tag import Okt

# 연설문 텍스트
speech_text = """존경하는 국민 여러분, 사랑하는 해외동포 여러분, 우리는 오늘 참으로 위대한 승리를 거두었습니다. 
우리의 이 승리에는 승자도 패자도 없습니다. 모두가 승리했습니다. 온 국민 모두의 승리이고, 대한민국의 승리입니다. 저는 이 모든 영광을 국민 여러분과 해외동포 여러분께 바칩니다.

존경하는 국민 여러분, 이제 새로운 대한민국을 향한 희망찬 새 역사가 시작되었습니다.
 갈등과 분열의 시대가 끝났습니다. 7천만 온 겨레가 하나가 되는 대통합의 시대가 시작되었습니다. 원칙과 신뢰의 새로운 정치를 시작하겠습니다. 평화의 번영의 한반도 시대를 열어가겠습니다. 정직하게 열심히 일하는 사람들이 성공하는 진정한 보통 사람들의 사회를 만들겠습니다. 투명하고 공정한 경제, 노사가 화합하는 경제로 기업하기 가장 좋은 나라를 만들겠습니다. 일자리 경제를 일으켜 취업과 실업의 어려움을 조속히 해결하겠습니다. 농어민들에게 새로운 희망을 드리고, 불우이웃과 장애인 등 모든 소외계층에게 따뜻한 나라를 만들겠습니다. 그리고 무엇보다 실패를 겪은 모든 사람들이 새로운 재기의 꿈을 키울 수 있는, 그런 나라를 만들겠습니다. 

끝까지 선전하신 한나라당 이회창 후보에게 심심한 위로를 전합니다. 
민주노동당 권영길 후보에게도 격려의 말씀을 드립니다.

존경하는 국민 여러분, 저는 이번 대통령 선거에서 국민 여러분이 보여주신 열망과 기대를
 잘 알고 있습니다. 이번 선거에서도 지역주의의 장벽을 허물지 못한 데 대해서는 큰 아쉬움이 남습니다. 그러나 충분히 가능하다는 희망은 발견했습니다. 포기하지 않겠습니다. 열심히 노력하여 국민통합을 이루어 내겠습니다. 

저는 또한 지금 우리 대한민국이 안고 있는 긴급한 과제와 험난한 도전도 잘 알고 있습니다. 
저는 대통령 당선자로서 북한 핵문제로 드리워진 한반도의 긴장을 해소하는 데 최선을 다하겠습니다. 북한의 핵문제를 평화적으로 해결하기 위해 우리의 주도적인 역할과 함께 한.미간의 긴밀한 공조협력을 해나가겠습니다. SOFA 개정 등 한.미간의 현안에 대해서도 우리 국민의 절실한 기대와 저의 입장을 우리 정부와 미국 정부에 전달하도록 하겠습니다. 전통적인 한.미간의 우호.동맹관계는 21세기에도 더욱 성숙, 발전돼야 합니다. 한.미관계는 정부차원을 넘어 양국 국민의 진정한 이해와 협력을 통해 더욱 깊어져야 합니다. 저는 양국이 인류의 보편적 가치를 함께 지향하고, 추구하는 문화국가로서 서로의 존엄을 인정하고, 발전시켜 나가도록 힘써 나갈 것입니다. 

저는 한반도의 평화를 지키고 발전시키기 위해 일본, 중국, 러시아, EU 등 우방국과도 더욱
 긴밀히 협력해 나가겠습니다. 정권 인수작업도 차질없이 해 나가겠습니다. 빠른 시일내에 대통령직 인수위원회를 구성하여 새 정부 출범에 만전을 기하도록 하겠습니다. 정권인수활동을 통해 현정권의 임기말까지 국정운영에 어던 빈틈도 발생하지 않도록 할 것입니다. 유능한 인재를 등용하기 위해 국민여론을 광범위하게 수렴하겠습니다. 일거에 모든 것을 다하려 하지 않겠습니다. 서두르지 않고 차근차근 해 나가겠습니다. 

존경하는 국민 여러분, 이번 대통령 선거는 우리 민족의 위대한 저력을 다시 한 번 과시한
 역사적 계기였습니다. 우리 국민은 사상 최초로 돈 안 드는 선거, 가장 깨끗한 선거를 실천한 대통령을 뽑았습니다. 우리 국민은 사상 최초로 수십만 유권자의 자발적 성금과 자원봉사를 통해 대통령을 당선시켰습니다. 우리 국민은 사상 최초로 정책과 비전 대결을 주도한 대통령을 선출했습니다. 그리고 우리 국민은 사상 최초로 국민통합과 정치혁명을 주창한 대통령을 선택했습니다. 그토록 열망하던 정치의 혁명적 변화가 이미 시작된 것입니다. 세계에 자랑할 만한 일류 정치가 우리 앞에 펼쳐지고 있습니다. 

우리는 보았습니다. 우리는 해냈습니다. IMF 위기를 가장 훌륭하게 극복해낸 국민답게, 첫
 도입된 국민경선제를 성공시킨 국민답게, 사상 최대의 월드컵 대회를 성공시킨 국민답게, 마침내 21세기 첫 대통령 선거를 세계가 놀랄 만큼 훌륭하게 성공시켰습니다. 모든 것이 국민의 힘이었습니다. 모든 것이 국민의 높은 의식수준의 결과였습니다. 이제 그 누구도 우리가 선진국민, 일류 문화민족임을 부인할 수 없습니다. 오늘 이 순간 우리는 세계에 당당한 선진국민, 일류 문화민족임을 확인하고 있습니다. 

이제 정치와 행정, 경제, 언론, 법조 등 사회 시스템을 높은 국민의식 수준에 걸맞게 변화
시키고, 개혁하는 것이 과제입니다. 그것은 21세기 국가 경쟁력의 핵심입니다. 저와 차기
 정부의 시대적 소명입니다. 저는 이번 대통령 선거에서 우리 국민이 보여준 위대한 저력과 가능성을 희망찬 미래로 실현시켜 나가겠습니다. 반드시 국민이 바라는 새로운 대한민국을 건설하여 국민 여러분께 보답하겠습니다. 기필코 해내겠습니다. 

국민 여러분이 저의 힘입니다. 국민 여러분의 변함없는 성원을 당부드립니다. 
국민 여러분의 모든 가정에 건강과 행복이 함께 하시기를 기원합니다. 
국민 여러분, 정말 감사합니다."""

# 형태소 분석기 초기화
okt = Okt()

# 명사 추출
nouns = okt.nouns(speech_text)

# 단어 빈도수 계산
word_counts = Counter(nouns)

# 워드클라우드 생성
wordcloud = WordCloud(
    font_path='malgun.ttf',  # 한글 폰트 경로 (Windows: 'malgun.ttf', Mac: '/Library/Fonts/AppleGothic.ttf')
    width=800, height=400,
    background_color='white'
).generate_from_frequencies(word_counts)

# 워드클라우드 출력
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

# 4. 제주도 추천 여행코스 찾기
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 제주도 추천 여행지 목록
jeju_travel_spots = [
    "주상절리", "협재해변", "성산일출봉", "섭지코지", "천지연폭포",
    "우도", "산방산", "중문관광단지", "잠수함", "러브랜드",
    "용두암", "신비의도로", "한라산", "오설록", "유리의성",
    "한림공원", "용머리해안", "해수욕장", "중문", "제주민속촌",
    "외돌개", "에코랜드"
]

# 단어 빈도 생성
word_freq = {spot: jeju_travel_spots.count(spot) for spot in jeju_travel_spots}

# 워드클라우드 생성
wordcloud = WordCloud(
    font_path="malgun.ttf",  # 한글 폰트 경로 (윈도우), 맥은 "AppleGothic.ttf"
    width=800, height=400,
    background_color="white"
).generate_from_frequencies(word_freq)

# 시각화
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

# 7 박근혜 연설문 
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

# 1️⃣ 연설문 입력 (긴 텍스트라면 파일로 불러오는 걸 추천하지만, 여기선 변수로 가정)
file_path = '박근혜대통령연설문.txt'  # 파일명 또는 경로 지정
with open(file_path, 'r', encoding='utf-8') as file:
    raw_text = file.read()

# 2️⃣ 불용어 설정
stopwords = [
    '올해', '비스', '대한민국', '추진', '우리', '정부', '박근혜', '후보', '시대', '대한',
    '민국', '대통령', '국민', '여러분', '존경하는', '오늘', '새로운', '그리고', '합니다',
    '있습니다', '대한민국의', '저는', '또한', '모든', '위해', '하는', '하는것이',
    '것입니다', '것이다', '수있습니다', '수', '있습니다', '있다', '있고', '해야', '하게',
    '합니다', '하면', '해서', '그것', '이것', '저것', '더', '가장', '될것입니다',
    '될것이다', '대해', '그동안', '때문에', '중', '등', '즉', '예를', '들어', '한편'
]

# 3️⃣ 전처리
# === 전처리 ===
cleaned_text = re.sub(r'\d+', ' ', raw_text)  # 숫자 제거
cleaned_text = re.sub(r'[^\w\s#]', ' ', cleaned_text)  # 특수문자 제거 (단, #는 유지)
cleaned_text = re.sub(r'\s+', ' ', cleaned_text)  # 다중 공백 제거

# 4️⃣ 형태소 분석 및 명사 추출
okt = Okt()
nouns = okt.nouns(cleaned_text)

# 5️⃣ 불용어 및 한 글자 단어 제거
filtered_nouns = [noun for noun in nouns if noun not in stopwords and len(noun) > 1]

# 6️⃣ 단어 빈도수 계산
word_counts = Counter(filtered_nouns)

# 7️⃣ 상위 100개 단어만 추출 (필요하면 수정 가능)
top_words = dict(word_counts.most_common(40))

# 8️⃣ 워드클라우드 생성
font_path = 'c:/Windows/Fonts/malgun.ttf'  # 너가 가지고 있는 한글 폰트 파일 경로! (없다면 다운로드 필요)

wordcloud = WordCloud(
    font_path=font_path,
    background_color='white',
    width=800,
    height=800
).generate_from_frequencies(top_words)

# 9️⃣ 결과 시각화
plt.figure(figsize=(10, 10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()















































