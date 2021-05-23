#!/usr/bin/python

import os
import logging
import subprocess
from SmaliLexer import SmaliLexer
from SmaliParser import SmaliParser
from visitor import StringVisitor
from antlr4 import *
from collections import Counter
from multiprocessing import Pool

APK_ROOT=r"/home/mingwan/sealant_testapps"
APK_ANALYZER_BIN=r"/home/mingwan/android/cmdline-tools/latest/bin/apkanalyzer"

logging.basicConfig(level=logging.INFO)
logging.getLogger().addHandler(logging.FileHandler("extractor.log"))


def run(*args):
    logging.info("Run {}".format(" ".join(args)))
    return subprocess.run(args, capture_output=True, check=True, text=True).stdout


# bucket = Counter()
# def list_apk(p):
#     global bucket

#     logging.info(f"Analyze {p}")
#     # 1. apkanalyzer를 이용하여 존재하는 모든 클래스의 이름을 추출
#     try:
#         for l in run(APK_ANALYZER_BIN, "dex", "packages", p, "--defined-only").splitlines():
#             if l[0] != "P": # 클래스 정보가 아닌 경우는 제외
#                 continue

#             name = l.split('\t')[3]
#             bucket[name] += 1
#     except:
#         logging.error("An error occurs")


def read_apk(p):
    logging.info(f"Analyze {p}")
    bucket = set()
    # 1. apkanalyzer를 이용하여 존재하는 모든 클래스의 이름을 추출
    for l in run(APK_ANALYZER_BIN, "dex", "packages", p, "--defined-only").splitlines():
        if l[0] != "C": # 클래스 정보가 아닌 경우는 제외
            continue

        class_name = l.split("\t")[3]

        # 2. 현재 분석 중인 클래스 이름을 단어 수준으로 처리
        for word in class_name.split("."):
            if "$" in word:
                continue

            bucket.add(word)

        # 3. apkanalyzer를 이용하여 smali 코드를 가져와서 코드 내에 존재하는 모든 단어를 추출
        smali_code = run(APK_ANALYZER_BIN, "dex", "code", p, "--class", class_name)
        lexer = SmaliLexer(InputStream(smali_code))
        stream = CommonTokenStream(lexer)
        parser = SmaliParser(stream)
        tree = parser.sFiles()

        walker = ParseTreeWalker()
        visitor = StringVisitor(bucket)
        walker.walk(visitor, tree)


    out_file = os.path.join("words", os.path.basename(p) + ".txt")
    logging.info(f"Output file: {out_file}")
    with open(out_file, "w") as out:
        for w in bucket:
            out.write(w)
            out.write('\n')


def do():
    os.makedirs("words", exist_ok=True)
    
    pool = Pool(4)
    for dir, dirs, files in os.walk(APK_ROOT):
        for f in files:
            if not f.endswith(".apk"):
                continue

            pool.apply_async(read_apk, (os.path.join(dir, f),))

    pool.close()
    pool.join()


if __name__ == "__main__":
    do()
    # for name, count in bucket.most_common():
    #     if count <= 1:
    #         break

    #     print(f"{name}: {count}")
