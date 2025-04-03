# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 08:53:06 2025

@author: Admin
"""
import urllib.request
from soynlp import DoublespaceLineCorpus
from soynlp.word import WordExtractor

from konlpy.tag import Okt
tokenizer = Okt()


urllib.request.urlretrieve("https://raw.githubusercontent.com/lovit/soynlp/master/tutorials/2016-10-20.txt", filename="2016-10-20.txt")

# 훈련 데이터를 다수의 문서로 분리
corpus = DoublespaceLineCorpus("2016-10-20.txt")
len(corpus)

# 상위 3개의 문서만 출력
i = 0
for document in corpus:
  if len(document) > 0:
    print(document)
    i = i+1
  if i == 3:
    break

# soynlp는 학습 과정을 거쳐야 한다!!!
# => 전체 코퍼스로부터 응집 확률과 브랜칭 엔트로피 단어 점수표를 만드는 과정
# => WordExtractor.extract()를 통해서 전체 코퍼스에 대해 단어 점수표를 계산

# 응집 확률
# => 내부 문자열(substring)이 얼마나 응집하여 자주 등하는지를 판단하는 척도
# => 문자열을 문자 단위로 분리하여 내부 문자열을 만드는 과정에서 
# => 왼쪽부터 순서대로 문자를 추가하면서 
# => 각 문자열이 주어졌을 때 그 다음 문자가 나올 확률을 계산하여 누적곱을 한 값
# => 이 값이 높을수록 전체 코퍼스에서 이 문자열 시퀀스 하나의 단어로 등장할 가능성이 높다.

word_extractor = WordExtractor()
word_extractor.train(corpus)
'''
word_extractor.train(corpus)
training was done. used memory 0.729 Gb
'''

word_score_table = word_extractor.extract()
'''
word_extractor.extract()
all cohesion probabilities was computed. # words = 223348
all branching entropies was computed # words = 361598
all accessor variety was computed # words = 361598
'''

# '반포한'의 응집 확률 계산 
word_score_table["반포한"].cohesion_forward   # 0.08838002913645132

# '반포한강'의 응집 확률
print(word_score_table["반포한강"].cohesion_forward)   # 0.19841268168224552

# '반포한강공'
word_score_table["반포한강공"].cohesion_forward  # 0.2972877884078849

# '반포한강공원'
word_score_table["반포한강공원"].cohesion_forward # 0.37891487632839754

# '반포한강공원에'
word_score_table["반포한강공원에"].cohesion_forward # 0.33492963377557666

# => 결합도는 '반포한강공원'일 때가 가장 높다
# => 응집도를 통해 판단하기에 하나의 단어로 판단하기에 가장 적합한 문자열은 '반포한강공원'

'''
SOYNLP의 브랜칭 엔트로피(branching entropy)
=> Branching Entropy는 확률 분포의 엔트로피값을 사용.

주어진 문자열에서 얼마나 다음 문자가 등장할 수 있는지를 판단하는 척도

브랜칭 엔트로피의 값은 
하나의 완성된 단어에 가까워질수록 
문맥으로 인해 점점 정확한 예측을 할 수 있게 되면서 점점 줄어든다...

첫번째 문자는 '디'
정답은 '스'

'디스' 다음 문자는 
정답은 '플'
정답은 '레'
정답은 '이'
'''

word_score_table['디스'].right_branching_entropy  # 1.6371694761537934
word_score_table['디스플'].right_branching_entropy  # -0.0
word_score_table['디스플레'].right_branching_entropy # -0.0

word_score_table['디스플레이'].right_branching_entropy  # 3.1400392861792916
# 문자 시퀀스 '디스플레이'라는 문자 시퀀스 다음에 
# 조사나 다른 단어와 같은 다양한 경우가 있을 수 있기 때문

'''
하나의 단어가 끝나면
그 경계부터 엔트로피 값이 증가하게 돔.
=> 단어를 판단하는 것이 가능
'''

'''
SOYNLP의 L tokenizer

한국어 : 띄어쓰기 단위로 나눈 어절 토큰은 주로 L 토큰 + R 토큰의 형식
예) '공원에'는 '공원 + 에' / '공부하는'은 '공부'+'하는'
    
L 토크나이저 : L 토큰 + R 토큰으로 나누되,
              분리 기준을 점수가 가장 높은 L 토큰을 찾아내는 원리
'''

from soynlp.tokenizer import LTokenizer

scores = {word:score.cohesion_forward for word, score in word_score_table.items()}
'''
 '휘': 0,
 '좇': 0,
 '팻': 0,
 '딛': 0,
'''


l_tokenizer = LTokenizer(scores=scores)
l_tokenizer.tokenize("국제사회와 우리의 노력들로 범죄를 척결하자", flatten=False)
'''
 [('국제사회', '와'), ('우리', '의'), ('노력', '들로'), ('범죄', '를'), ('척결', '하자')]
'''

'''
최대 점수 토크나이저: MaxScoreTokenizer

띄어쓰기가 되지 않는 문장에서 점수가 높은 글자 시퀀스를 순차적으로 찾아내는 토크나이저

'''
from soynlp.tokenizer import MaxScoreTokenizer

maxscore_tokenizer = MaxScoreTokenizer(scores=scores)
maxscore_tokenizer.tokenize("국제사회와우리의노력들로범죄를척결하자")
'''
['국제사회', '와', '우리', '의', '노력', '들로', '범죄', '를', '척결', '하자']
'''

'''
반복되는 문자 정제: emticon_normalize() / report_normalize()

SNS나 채팅 데이터와 같은 한국어 데이터의 경우에는 ㅋㅋ, ㅎㅎ등의 이모티콘의 경우
'''

from soynlp.normalizer import *

print(emoticon_normalize('앜ㅋㅋㅋㅋ이영화존잼쓰ㅠㅠㅠㅠㅠ', num_repeats=2))
print(emoticon_normalize('앜ㅋㅋㅋㅋㅋㅋㅋㅋㅋ이영화존잼쓰ㅠㅠㅠㅠ', num_repeats=2))
print(emoticon_normalize('앜ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ이영화존잼쓰ㅠㅠㅠㅠㅠㅠ', num_repeats=2))
print(emoticon_normalize('앜ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ이영화존잼쓰ㅠㅠㅠㅠㅠㅠㅠㅠ', num_repeats=2))


print(repeat_normalize('와하하하하하하하하하핫', num_repeats=2))
print(repeat_normalize('와하하하하하하핫', num_repeats=2))
print(repeat_normalize('와하하하하핫', num_repeats=2))

### Customized KoNLPy ###
'''
형태소 분석 입력: '은경이는 사무실로 갔습니다'
형태소 분석 결과:  ['은', '경이', '는', '사무실', '로', '갔습니다', '.']

pip install customized_konlpy
'''
from ckonlpy.tag import Twitter
twitter = Twitter()
twitter.morphs('은경이는 사무실로 갔습니다.')
#  ['은', '경이', '는', '사무실', '로', '갔습니다', '.']

# 형태소 분석기 Twitter에 add_dictionary('단어', '품사')와 같은 형식으로 사전 추가
twitter.add_dictionary('은경이', 'Noun')
twitter.morphs('은경이는 사무실로 갔습니다.')
# ['은경이', '는', '사무실', '로', '갔습니다', '.']















































