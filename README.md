# YouTube Creator Website

![GitHub repo size](https://img.shields.io/github/repo-size/workingjun/YouTube-CreatorWebsite)
![GitHub last commit](https://img.shields.io/github/last-commit/workingjun/YouTube-CreatorWebsite)

## 📌 프로젝트 개요
YouTube Creator Website는 YouTube 크리에이터들이 자신들의 채널 데이터를 수집하고 정리하여 확인할 수 있도록 돕는 웹 애플리케이션입니다. API를 활용하여 최신 데이터를 가져오고, 유용한 정보들을 시각적으로 정리하여 제공합니다.

## 🚀 주요 기능
- 🔍 **YouTube API 연동**: 채널 및 동영상 데이터를 자동으로 가져오기
- 📄 **채널 및 동영상 정보 표시**: 채널 정보, 구독자 수, 조회 수, 업로드 영상 목록 제공
- 🖼️ **미디어 포함**: 썸네일, 영상 미리보기, 댓글 등 다양한 요소 포함
- 💬 **댓글 분석**: 인기 댓글 및 상위 10개 댓글 데이터 제공
- 🔗 **링크 공유 기능**: 특정 영상이나 채널 데이터를 공유 가능

## 🛠️ 기술 스택
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask / Django)
- **Database**: MySQL
- **API**: YouTube Data API v3

## 📂 프로젝트 구조
```
YouTube-CreatorWebsite/
│── config/              # 설정 관련 파일
│── modules/             # 핵심 모듈
│── routes/              # API 라우트 핸들러
│── static/              # 정적 파일 (CSS, JS, 이미지 등)
│── templates/           # HTML 템플릿 파일
│── .gitignore           # Git 무시 파일 목록
│── app.py               # 메인 애플리케이션 실행 파일
│── app_local.py         # 로컬 환경 실행 파일
│── collect_linkdata.py  # 링크 데이터 수집 스크립트
│── mysql_config.txt     # MySQL 설정 파일
│── requirements.txt     # 필수 패키지 목록
│── start_collecting.py  # 데이터 수집 시작 스크립트
```

## 🔧 설치 및 실행 방법
```bash
# 저장소 클론
git clone https://github.com/workingjun/YouTube-CreatorWebsite.git
cd YouTube-CreatorWebsite

# 필수 패키지 설치
pip install -r requirements.txt

# 로컬 실행
python app_local.py 
```

## 🔗 YouTube API 키 설정
1. [Google Cloud Console](https://console.cloud.google.com/)에서 프로젝트를 생성합니다.
2. YouTube Data API v3을 활성화합니다.
3. API 키를 생성하고 `config/config.py`에 추가합니다.
```python
YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"
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

## 📌 사용 예시
- 특정 YouTube 채널의 최신 영상 정보를 정리하여 제공
- 인기 댓글 및 썸네일을 포함한 영상 카드 스타일 출력
- 채널 성장 추이 및 데이터 요약 제공