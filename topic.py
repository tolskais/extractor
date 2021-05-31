import gensim
import gensim.corpora as corpora
from gensim.corpora import dictionary
from nltk.corpus import stopwords
import spacy
import os
import re
from pprint import pprint
from multiprocessing import Pool
from nltk.stem import WordNetLemmatizer

def __read_line(f):
    with open(f) as fh:
        for l in fh:
            l = l.strip()
            if len(l) == 0:
                continue

            yield l


stop_words = stopwords.words('english')
lemm = WordNetLemmatizer()
android_words = set(__read_line("android_stopwords.txt"))


def is_stopwords(w):
    return len(w) <= 2 or w in stop_words or w in android_words


def read_apk(name):
    word_set = set()
    for word in __read_line(os.path.join("words", name)): #각각의 apk에서 추출한 단어
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
        
        for w in word:
            parts = re.findall('([a-z0-9]+|[A-Z][a-z0-9]+|[A-Z0-9]+(?=[^A-Z0-9a-z])|[A-Z0-9]+?(?=[A-Z0-9][a-z]))', w)
            # 총 4 가지 패턴의 part를 찾음
            # 1. [a-z0-9]+: 소문자 및 숫자로 이루어진 단어
            # 2. [A-Z][a-z0-9]+: 첫 글자는 대문자, 나머지는 소문자 및 숫자로 이루어진 단어
            # 3. [A-Z0-9]+: 대문자 및 숫자로 이루어진 단어
            # 4. [A-Z0-9]+?(?=[A-Z][a-z]): 대문자 및 숫자로 이루어진 단어이되, 이어지는 두 글자가 대문자 + 소문자로 이루어진 경우
            # 4번은 2번 패턴을 뺏어오는 경우를 방지하고자 추가됨
            # ex) NLPClass -> NLP, Class로 나뉘어야 하나, 4번 규칙이 없다면 NLPC, lass 로 나뉘어짐
            # print(w, parts)
            # for p in map(sp, parts):
            for p in parts:
                # p = p[0].lemma_.lower()
                if p.isdigit():
                    continue

                p = lemm.lemmatize(p.lower())
                if is_stopwords(p):
                    continue

                # print(p)
                word_set.add(p)

    return word_set


def read_apks():
    result = []
    names = []
    pool = Pool(8)
    for name in os.listdir("words"):
        names.append(name)
        result.append(pool.apply_async(read_apk, (name,)))

    pool.close()
    pool.join()

    return names, [r.get() for r in result]


def do():
    names, word_dict = read_apks()
    id2word = corpora.Dictionary(word_dict)
    id2word.filter_extremes()
    corpus = [id2word.doc2bow(t) for t in word_dict]
    
    lda = gensim.models.ldamodel.LdaModel(
        corpus=corpus,
        id2word = id2word,
        update_every=1,
        passes=10,
        num_topics=26) # 26개로 기억하는데, 논문을 찾아서 수치는 바꿔야 함

    pprint(lda.print_topics())

if __name__ == "__main__":
    do()