==실행을 위한 과정==

1. Antlr를 이용한 smali parser 생성
- https://github.com/psygate/smali-antlr4-grammar 에서 g4 파일을 다운로드
- https://www.antlr.org/ 에서 antlr 빌드를 위한 jar 파일 다운로드
- antlr jar 파일을 이용해 python parser 실행
`java -jar [antlr jar] -Dlanguage=Python3 [g4 file]`

2. Python 환경 설정
- Python3 환경설정
- antlr4 runtime 라이브러리 다운로드
`pip install antlr4-python3-runtime`

3. 안드로이드 SDK 설정
- Android Studio가 설치된 경우, SDK가 설치된 경로에서 command tools 중 apkanalyzer가 존재하는 경로 파악 필요
- 설치하지 않은 경우
  1. https://developer.android.com/studio#command-tools 에서 command line tools 다운로드
  2. [android sdk가 설치될 root dir]/cmdline-tools/latest/ 에 NOTICE.txt, bin, lib, source.properties가 보이도록 압축 해제
  3. [android sdk가 설치될 root dir]/cmdline-tools/latest/bin/sdkmanager 를 이용하여 최신 build tool 다운로드
  `./sdkmanager --install "buildtools;[version]"`
    - 최신 버전은 `./sdkmanager --list` 를 통해 확인 가능
    

4. 스크립터 환경설정
- extractor.py 내에 두 가지 변수 값 변경
- APK_ROOT=[apk가 모여 있는 디렉터리 경로]
- APK_ANALYZER_BIN=[android command tool 중 apkanalyzer의 경로]
`python extractor.py`