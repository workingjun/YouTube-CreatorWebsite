# YouTube Creator Website

![GitHub repo size](https://img.shields.io/github/repo-size/workingjun/YouTube-CreatorWebsite)
![GitHub last commit](https://img.shields.io/github/last-commit/workingjun/YouTube-CreatorWebsite)

## 📌 프로젝트 개요
이 프로젝트는 유튜버 또는 마케터가 자신 또는 타인의 유튜브 영상에 대한 데이터를 직관적으로 분석할 수 있도록 돕는 웹사이트입니다. 영상 정보, 댓글, 인기 순위 등을 한눈에 확인할 수 있도록 설계되어 있습니다.
예시: 특정 채널 ID를 입력하면, 그 채널의 영상 목록과 각 영상의 좋아요, 댓글 수, 인기 댓글을 보여줍니다.

## 🚀 주요 기능
- 🔍 **YouTube API 연동**: 채널 및 동영상 데이터를 자동으로 가져오기
- 📄 **채널 및 동영상 정보 표시**: 채널 정보, 구독자 수, 조회 수, 업로드 영상 목록 제공
- 🖼️ **미디어 포함**: 썸네일, 영상 미리보기, 댓글 등 다양한 요소 포함
- 💬 **댓글 분석**: 인기 댓글 및 상위 10개 댓글 데이터 제공
- 🔗 **정렬 기능**: 최신 트랜드 순, 조회수 순, 좋아요 순, 댓글 순 등등 정렬 기능 제공

## 🛠️ 기술 스택
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask)
- **Database**: MySQL
- **API**: YouTube Data API v3

## 📂 프로젝트 구조
```
YouTube-CreatorWebsite/
│── src/              # 설정 관련 파일
│   │── config/              # 설정 관련 파일
│   │── app/             # 어플리케이션의 코어
│   │── modules/             # 어플리케이션 관련 모듈
│   │── routes/              # API 라우트 핸들러
│   │── static/              # 정적 파일 (CSS, JS, 이미지 등)
│   │── templates/           # HTML 템플릿 파일
│   │── manager.py               # 메인 애플리케이션 실행 파일
│   │── local_manager.py         # 로컬 환경 실행 파일
│── .gitignore           # Git 무시 파일 목록
│── main.py              # 메인 스크립트
│── mysql_config.txt     # MySQL 설정 파일
│── requirements.txt     # 필수 패키지 목록
```

## 🔧 설치 및 실행 방법
```bash
# 저장소 클론
git clone https://github.com/workingjun/YouTube-CreatorWebsite.git
cd YouTube-CreatorWebsite

# 필수 패키지 설치
pip install -r requirements.txt

# 로컬 실행
python src/app_local.py 
```

## 채널 아이디 설정
1. [Youtube](https://www.youtube.com/)에서 원하는 크리에이터를 선택합니다
2. 더보기를 클릭한 후 스크롤하여 채널 아이디를 복사합니다
3. channel Id를 붙여넣어 `src/config/channelId.py`에 추가합니다.
```
CHANNELID = {
    "channel name1" : "channel id 1",
    "channel name2" : "channel id 2",
    "channel name3" : "channel id 3"
}
```

## 🔗 YouTube API 키 설정
1. [Google Cloud Console](https://console.cloud.google.com/)에서 프로젝트를 생성합니다.
2. YouTube Data API v3을 활성화합니다.
3. API 키를 생성하고 `src/config/config.py`에 추가합니다.
```python
api_key = [
    "api_key1",
    "api_key2",
    "api_key3",
    "api_key4",
    "api_key5",
    "api_key6"
]
```

## 🚀 배포 (PythonAnywhere)
1. [PythonAnywhere](https://www.pythonanywhere.com/) 계정을 생성합니다.
2. 새 PythonAnywhere 콘솔에서 Git 저장소를 클론합니다.
   ```bash
   git clone https://github.com/workingjun/YouTube-CreatorWebsite.git
   cd YouTube-CreatorWebsite
   ```
3. PythonAnywhere의 **Web** 탭에서 새 웹 애플리케이션을 생성하고 Flask를 선택합니다.
4. 가상 환경을 설정하고 필요한 패키지를 설치합니다.
   ```bash
   pip install -r requirements.txt
   ```
5. WSGI 설정을 변경하여 `app.py`를 실행하도록 설정합니다.
6. MySQL을 사용하는 경우 PythonAnywhere의 **Databases** 탭에서 설정을 완료합니다.
7. 변경 사항을 반영하려면 **Reload** 버튼을 눌러 애플리케이션을 다시 시작합니다.

## PythonAnywhere Database 설정
1. [PythonAnywhere](https://www.pythonanywhere.com/)의 mysql bash를 엽니다.
2. `mysql_config.py`를 참고하여 비디오 아이디, 비디오 데이터 등등 테이블을 생성합니다.
3. 테이블 생성 후에 unique 제약 조건을 추가합니다.
4. 그 후 `src/config/db_config.py`에서 자신의 계정 정보와 데이터 베이스 이름, 비밀번호를 입력합니다.

## 📌 사용 예시
- 특정 YouTube 채널의 최신 영상 정보를 정리하여 제공
- 인기 댓글 및 썸네일을 포함한 영상 카드 스타일 출력
- 채널 성장 추이 및 데이터 요약 제공