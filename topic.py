import nltk
import pyLDAvis
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from nltk.corpus import stopwords
import spacy
import os
import re
from pprint import pprint

#stop_words = stopwords.words('english')

def read_apks():
    result = []
    names = []
    for name in os.listdir("words"):
        word_set = set()
        names.append(name)
        with open(os.path.join("words", name)) as fh: #각각의 apk에서 추출한 단어
            for word in fh:
                word = word.strip()
                if len(word) == 0:
                    continue

                if word[0] == "/": # /home/mingwan 과 같이 path를 나타내는 경우인 경우
                    # print("Path?", word)
                    word = word[1:].split("/")
                elif "/" in word: # Landroid/google/... 과 같이 class name을 나타내는 경우
                    # print("ClassName?", word)
                    word = word.split("/")
                    if word[0][0] == 'L':
                        word[0] = word[0][1:]

                    word[-1] = word[-1].replace(';', '')
                else: # 그 외의 경우
                    word = (word,)
                
                # print(word)
                for w in word:
                    parts = re.findall('([a-z0-9]{2,}|[A-Z][a-z0-9]+|[A-Z0-9]{2,}|[A-Z0-9]{2,}?(?=[A-Z0-9][a-z]))', w)
                    # 총 4 가지 패턴의 part를 찾음
                    # 1. [a-z0-9]{2,}: 두 글자 이상의 소문자 및 숫자로 이루어진 단어
                    # 2. [A-Z][a-z0-9]+: 첫 글자는 대문자, 나머지는 소문자 및 숫자로 이루어진 단어 (총 두 글자 이상)
                    # 3. [A-Z0-9]{2,}: 두 글자 이상의 대문자 및 숫자로 이루어진 단어
                    # 4. [A-Z0-9]{2,}?(?=[A-Z][a-z]): 두 글자 이상의 대문자 및 숫자로 이루어진 단어이되, 이어지는 두 글자가 대문자 + 소문자로 이루어진 경우
                    # 4번은 2번 패턴을 뺏어오는 경우를 방지하고자 추가됨
                    # ex) NLPClass -> NLP, Class로 나뉘어야 하나, 4번 규칙이 없다면 NLPC, lass 로 나뉘어짐
                    # print(w, parts)
                    for p in parts:
                        word_set.add(p)

        


        result.append(word_set)

    return names, result

def do():
    names, word_dict = read_apks()
    id2word = corpora.Dictionary(word_dict)
    corpus = [id2word.doc2bow(t) for t in word_dict]
    
    lda = gensim.models.ldamodel.LdaModel(
        corpus=corpus,
        id2word = id2word,
        num_topics=26) # 26개로 기억하는데, 논문을 찾아서 수치는 바꿔야 함

    pprint(lda.print_topics())

if __name__ == "__main__":
    do()