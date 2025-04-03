# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 11:29:05 2025

@author: Admin
"""
import nltk
nltk.download('stopwords')

from konlpy.tag import Okt

okt = Okt()

### Bag of Words 함수 ###
# 입력된 문서에 대해서 단어 집합(vocaburary)을 만들어
# 각 단어에 점수 인덱스를 할당하고, BoW

def build_bag_of_words(document):
  # 온점 제거 및 형태소 분석
  document = document.replace('.', '')
  tokenized_document = okt.morphs(document)

  word_to_index = {}
  bow = []

  for word in tokenized_document:  
    if word not in word_to_index.keys():
      word_to_index[word] = len(word_to_index)  
      # BoW에 전부 기본값 1을 넣는다.
      bow.insert(len(word_to_index) - 1, 1)
    else:
      # 재등장하는 단어의 인덱스
      index = word_to_index.get(word)
      # 재등장한 단어는 해당하는 인덱스의 위치에 1을 더한다.
      bow[index] = bow[index] + 1

  return word_to_index, bow

doc1 = "정부가 발표하는 물가상승률과 소비자가 느끼는 물가상승률은 다르다."
vocab, bow = build_bag_of_words(doc1)
print('vocabulary :', vocab)
'''
vocabulary : {'정부': 0, '가': 1, '발표': 2, '하는': 3, '물가상승률': 4, '과': 5, '소비자': 6, '느끼는': 7, '은': 8, '다르다': 9}
'''
print('bag of words vector :', bow)
'''
bag of words vector : [1, 2, 1, 1, 2, 1, 1, 1, 1, 1]
'''

doc2 = '소비자는 주로 소비하는 상품을 기준으로 물가상승률을 느낀다.'

vocab, bow = build_bag_of_words(doc2)
print('vocabulary :', vocab)
'''
vocabulary : {'소비자': 0, '는': 1, '주로': 2, '소비': 3, '하는': 4, '상품': 5, '을': 6, '기준': 7, '으로': 8, '물가상승률': 9, '느낀다': 10}
'''
print('bag of words vector :', bow)
'''
bag of words vector : [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1]
'''

doc3 = doc1 + ' ' + doc2
vocab, bow = build_bag_of_words(doc3)
print('vocabulary :', vocab)
'''
vocabulary : {'정부': 0, '가': 1, '발표': 2, '하는': 3, '물가상승률': 4, '과': 5, '소비자': 6, '느끼는': 7, '은': 8, '다르다': 9, '는': 10, '주로': 11, '소비': 12, '상품': 13, '을': 14, '기준': 15, '으로': 16, '느낀다': 17}
'''
print('bag of words vector :', bow)
'''
bag of words vector : [1, 2, 1, 2, 3, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1]
'''

'''
BoW는 각 단어가 등장한 횟수를 수치화하는 텍스트 표현 방법
주로 어던 단어가 얼마나 등장했는지를 기준으로 
문서가 어떤 성격의 문서인지를 판단하는 작업

즉, 분류 문제나 여러 문서 간의 유사도를 구하는 문제

'달리기', '체력', '근력'과 같은 단어가 자주 등장하면 해당 문서를 체육 관련 문서
'미분', '방정식', '부등식'과 같은 단어가 자주 등장한다면 수학 관련 문서
'''

### CounterVectorizer 클래스로 BoW 만들기 ###
from sklearn.feature_extraction.text import CountVectorizer

corpus = ['you know I want your love. because I love you.']

vector = CountVectorizer()

# 코퍼스로부터 각 단어의 빈도수를 기록 : CountVectorizer.fit_transform()
print('bag of words vector :', vector.fit_transform(corpus).toarray()) 
# bag of words vector : [[1 1 2 1 2 1]]

# 각 단어의 인덱스가 어떻게 부여되었는지를 출력 : vocabulary_
print('vocabulary :',vector.vocabulary_)
# vocabulary : {'you': 4, 'know': 1, 'want': 3, 'your': 5, 'love': 2, 'because': 0}

'''
you와 love는 두 번씩 언급되었으므로 각각 인덱스 2와 인덱스 4에서 2의 값

알파벳 I는 BoW를 만드는 과정에서 사라졌는데
CountVectorizer가 기본적으로 길이가 2이상인 문자에 대해서만 토큰으로 인식하기 때문
'''
corpus = ["정부가 발표하는 물가상승률과 소비자가 느끼는 물가상승률은 다르다."]
vector = CountVectorizer()
print('bag of words vector :', vector.fit_transform(corpus).toarray()) 
# bag of words vector : [[1 1 1 1 1 1 1]

print('vocabulary :',vector.vocabulary_)
'''
vocabulary : {'정부가': 6, '발표하는': 4, '물가상승률과': 2, '소비자가': 5, '느끼는': 0, '물가상승률은': 3, '다르다': 1}
'''

'''
CountVectorizer는 띄어쓰기를 기준으로 분리한 뒤에 
'물가상승률과'와 '물가상승률은'으로 조사를 포함해서 하나의 단어로 판단하기 때문에
서로 다른 두 단어로 인식
'''

### 불용어를 제거한 BoW ###
'''
영어의 BoW를 만들기 위해 사용하는 Countvectorizer는 
불용어를 지정하면,
불용어는 제외하고 BoW를 만들 수 있도록 불용어 제거 기능 지원
'''


from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
## 사용자가 직접 정의한 불용어 사용
text = ["Family is not an important thing. It's everything."]

vect = CountVectorizer(stop_words=['the', 'a', 'an', 'is', 'not'])
print('bag of words vector :', vector.fit_transform(text).toarray()) 
# bag of words vector : [[1 1 1 1 1 1 1 1]]

print('vocabulary :',vect.vocabulary_)
# vocabulary : {'family': 2, 'is': 4, 'not': 6, 'an': 0, 'important': 3, 
#              'thing': 7, 'it': 5, 'everything': 1}

## CounterVectorizer에서 제공하는 자체 불용어 사용
text = ["Family is not an important thing. It's everything."]

vect = CountVectorizer(stop_words='english')
print('bag of words vector :', vect.fit_transform(text).toarray()) 
# bag of words vector : [[1 1 1]]
print('vocabulary :',vect.vocabulary_)
# vocabulary : {'family': 0, 'important': 1, 'thing': 2}

# NLTK에서 지원하는 불용어 사용 : stopwords
text = ["Family is not an important thing. It's everything."]

stop_words = stopwords.words("english")

vect = CountVectorizer(stop_words=stop_words)

print('bag of words vector :',vect.fit_transform(text).toarray()) 
# bag of words vector : [[1 1 1 1]]
print('vocabulary :',vect.vocabulary_)
# vocabulary : {'family': 1, 'important': 2, 'thing': 3, 'everything': 0}

'''
TF-IDF(Term Frequency- Inverse Document Frequency)
=> DTM 내에 있는 각 단어에 대한 중요도를 계산 할 수 있는 TF-IDF 가중치
=> DTM을 사용하는 것보다 보다 많은 정보를 고려하여 문서들을 비교

   주로 문서의 유사도를 구하는 직업
   검색 시스템에서 검색 결과의 중요도를 정하는 작업
   문서 내에서 특정 단어의 중요도를 구하는 작업
   
TF-IDF : TF와 IDF를 곱한 값

문서를 d, 단어를 t, 문서의 총 개수를 n이라고 표현할 때 TF, DF, IDF는

     tf(d,t) : 특정 문서 d에서 특정 단어 t의 등장 횟수.
     
     df(t) : 특정 단어 t가 등장한 문서의 수.
     
     idf(t) : df(t)에 반비례하는 수 : log 가 필수 
     
'''

### 파이썬으로 TF-IDF 직접 구현 ###
from math import log 
import pandas as pd


docs = [
  '먹고 싶은 사과',
  '먹고 싶은 바나나',
  '길고 노란 바나나 바나나',
  '저는 과일이 좋아요'
] 

vocab = list(set(w for doc in docs for w in doc.split()))
vocab.sort()
print('단어장의 크기:', len(vocab)) # 단어장의 크기: 9
# =>  ['과일이', '길고', '노란', '먹고', '바나나', '사과', '싶은', '저는', '좋아요']

## TF, IDF, 그리고 TF-IDF 값을 구하는 함수를 구현
# 총 문서의 수
N = len(docs) 

def tf(t, d):
  return d.count(t)

def idf(t):
  df = 0
  for doc in docs:
      df += t in doc
  return log(N/(df+1))

def tfidf(t, d):
  return tf(t,d)* idf(t)

# DTM을 데이터프레임에 저장하여 출력
result = []

# 각 문서에 대해서 아래 연산을 반복
for i in range(N):
  result.append([])
 
  d = docs[i]
  for j in range(len(vocab)):
    t = vocab[j]
    result[-1].append(tf(t, d))

tf_ = pd.DataFrame(result, columns = vocab)
'''
   과일이  길고  노란  먹고  바나나  사과  싶은  저는  좋아요
0    0   0   0   1    0   1   1   0    0
1    0   0   0   1    1   0   1   0    0
2    0   1   1   0    2   0   0   0    0
3    1   0   0   0    0   0   0   1    1
'''

## 각 단어에 대한 IDF값 
result = []

for j in range(len(vocab)):
    t = vocab[j]
    result.append(idf(t))

idf_ = pd.DataFrame(result, index=vocab, columns=["IDF"])
'''
          IDF
과일이  0.693147
길고   0.693147
노란   0.693147
먹고   0.287682
바나나  0.287682
사과   0.693147
싶은   0.287682
저는   0.693147
좋아요  0.693147
'''
## TF-IDF 행렬
result = []
for i in range(N):
  result.append([])
  d = docs[i]
  for j in range(len(vocab)):
    t = vocab[j]
    result[-1].append(tfidf(t,d))

tfidf_ = pd.DataFrame(result, columns = vocab)
'''
    과일이        길고        노란  ...        싶은        저는       좋아요
0  0.000000  0.000000  0.000000  ...  0.287682  0.000000  0.000000
1  0.000000  0.000000  0.000000  ...  0.287682  0.000000  0.000000
2  0.000000  0.693147  0.693147  ...  0.000000  0.000000  0.000000
3  0.693147  0.000000  0.000000  ...  0.000000  0.693147  0.693147
'''

'''
사이킷런을 이용한 DTM과 TF-IDF 실습
'''
from sklearn.feature_extraction.text import CountVectorizer

corpus = [
    'you know I want your love',
    'I like you',
    'what should I do ',    
]

vector = CountVectorizer()

print(vector.fit_transform(corpus).toarray())
'''
[[0 1 0 1 0 1 0 1 1]
 [0 0 1 0 0 0 0 1 0]
 [1 0 0 0 1 0 1 0 0]]
'''

print(vector.vocabulary_)
'''
{'you': 7, 'know': 1, 'want': 5, 'your': 8, 'love': 3, 'like': 2, 'what': 6, 'should': 4, 'do': 0}
'''

### 사이킷런은 TF-IDF를 자동 계산해주는 TfidVectorizer를 제공
from sklearn.feature_extraction.text import TfidfVectorizer

corpus = [
    'you know I want your love',
    'I like you',
    'what should I do ',    
]

# 1. TfidVectorizer.fit() 로 학습
tfidfv = TfidfVectorizer().fit(corpus)

# transform()를 이용
print(tfidfv.transform(corpus).toarray())
'''
[[0.         0.46735098 0.         0.46735098 0.         0.46735098
  0.         0.35543247 0.46735098]
 [0.         0.         0.79596054 0.         0.         0.
  0.         0.60534851 0.        ]
 [0.57735027 0.         0.         0.         0.57735027 0.
  0.57735027 0.         0.        ]]
'''
print(tfidfv.vocabulary_)
'''
{'you': 7, 'know': 1, 'want': 5, 'your': 8,
 'love': 3, 'like': 2, 'what': 6, 'should': 4, 'do': 0}
'''













































