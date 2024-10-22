# ChatBoard
![logo](https://github.com/user-attachments/assets/8130676a-b775-47b9-a3da-4fda8e95cf83)
#### 해당 프로젝트는 국민대학교 2024 여름방학 LLM Application 부트캠프의 일환으로 진행 되었습니다.

## 1.1. 프로젝트 명
ChatBoard ~ Boardgame Assistant using LLM model

## 1.2. 프로젝트 기간
* 프로젝트 기간 : 2024.07.22 ~ 2024.07.26 (5일)

## 1.3. 프로젝트 인원
- Front : 김성호, 박재영
- Server : 조현상
- LLM : 이준우, 정채원

## 2.1. 기획의도 및 요구사항 분석
보드 게임을 진행하기 전 게임 규칙 학습 및 보드 게임을 진행 하면서 생길 수 있는 규칙에 대한 모호한 부분에 대해서 상황에 따른 해결 방안을 LLM을 통해서 질의 이후 사용자에게 전달 한다.
- 여러가지 보드게임에 대해서 사용자는 단순한 검색을 통해 그 게임에 대한 규칙을 알 수 있어야 한다.
- 게임 도중에 생길 수 있는 규칙에 관해 생기는 의견 차이에 대해서 LLM의 학습을 통해 명확하게 해당 상황에 대하여 결론을 내려 줄 수 있어야 한다.

## 2.2. 시나리오 설정
**참가자**

A, B, C

**상황설명**

A와 B와 C가 3인용 보드 게임을 진행하고 있었다. 주사위를 굴려서 칸에 지시 된 명령을 진행하는 게임이다. 게임을 진행 하던 도중 B가 찬스 카드 칸에 도착을 했고 ‘다른 플레이어 한테서 100 포인트를 가져올 수 있다’ 라는 명령을 가진 카드를 얻었다. B는 이때 A하고 C에게 동시에 100 포인트를 요구 했다. 그러나 A가 B에게 한 명만 정해서 포인트를 가져가야 한다고 했고, B는 카드에는 다른 플레이어라고 만 되어 있으니깐 두 명 모두에게 받는게 맞다 라는 의견 차이가 생기게 되었다. 이러한 상황에서 이 시스템 ‘ChatBoard’에게 질의를 함으로 써 해당 게임의 규칙을 자세히 확인 해 보았고, 게임의 기본적인 명령은 무조건 한 사람을 대상으로 한다 라는 것을 알 수 있었다. 최종 적으로 질의에 대한 답변으로 ‘A의 말이 맞다’라는 결과를 얻을 수 있었다.

## 2.3. 주요 기능
- 게임 목록 보기
- 게임 검색 필터
- 게임 검색 하기
- 게임 상세 정보 화면 열기
- 게임 규칙 질문 하기 (텍스트 및 사진)
- 챗봇에게 질문 시 답변 받기

## 3.1. 개발환경
* Front-end : 
* Server : 
* Back-end :
* Developer Tools : VS Code
* GitHub

## 3.2. 사용한 API
```
#East-US
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_REGION=
OPENAI_API_VERSION=
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=
```

## 3.3. 필요한 라이브러리
### 사용된 목록
```
Flask==2.2.5
Flask-Cors==4.0.1
python-dotenv==1.0.1
langchain==0.2.10
langchain-community==0.2.9
langchain-core==0.2.22
langchain-openai==0.1.17
langchain-text-splitters==0.2.2
langsmith==0.1.93
pypdf==4.3.1
python-dotenv==1.0.1
typing_extensions==4.12.2
typing-inspect==0.9.0
```
### Terminal 에서 실행
파일이 있는 디렉토리에서 하단의 명령 실행
- `pip install -r requirements.txt` 

##  4.1. Sequence Diagram
![chatboard_sequence_diagram](https://github.com/user-attachments/assets/eed5da70-0c19-4623-a999-5b19365f8792)

##  4.2. 화면설계 및 기능 구현
|![main_screen](https://github.com/user-attachments/assets/11d6dab9-3839-4d82-860d-9f4b186596a8)|![Chat_screen](https://github.com/user-attachments/assets/33924226-1ea8-4ff5-b2ce-1efe459852ee)|
|:---:|:---:|
|메인 화면|챗봇 대화 화면|

##  5.1. 최종 결과
사이트에 접근해서 사용자가 쉽게 원하는 보드게임에 대해서 검색 할 수 있었고, 챗봇과의 대화를 통해 사용자가 원하는 정보를 제공 해줄수 있었다.

##  5.2. 개선 해야 할 사항
(자유롭게 작성)

##  6. LLM 부트캠프를 통해 배운점
- 해당 프로젝트 이전 미니 프로젝트를 진행하면서 직면한 문제로 팀원들 간의 시스템 환경 차이로 인해 라이브러리 충돌이 발생했습니다. 해당 프로젝트에서는 이러한 문제를 방지하기 위해, 팀원들이 모두 동일한 개발 환경에서 작업할 수 있도록 `requirements.txt` 파일을 작성하여 라이브러리 버전을 통일했습니다. 이를 통해 환경 설정의 일관성을 유지하고, 라이브러리 버전 차이로 인한 문제를 효과적으로 해결할 수 있었습니다.

 - 프로젝트 진행 중 파일을 읽어들일 때 파일 경로를 각자의 컴퓨터 절대 경로로 명시함으로써 발생한 충돌이 있었습니다. 이를 해결하기 위해, 이번 프로젝트에서는 `os.path`를 사용하여 상대 경로를 가져오도록 변경했습니다. 이를 통해 파일 경로 충돌을 효과적으로 회피할 수 있었고, 팀원들이 서로 다른 환경에서도 일관된 방식으로 파일을 접근할 수 있었습니다.

##  7. 참고 사항
- 시연 영상 링크 : https://youtu.be/YjaCYeKBIh8?si=xB7BuAm_qrgrkzFt
- 세부 기능 영상 : https://youtu.be/PUaXsZAJu8U
