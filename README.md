# 프로젝트 문서

이 문서는 현재 프로젝트의 구조, 실행 방법, 데이터베이스 설정, API 동작을 상세히 설명합니다.

## 1) 프로젝트 개요
- FastAPI + SQLAlchemy + MySQL 조합으로 간단한 API를 제공합니다.
- `app/main.py`에서 FastAPI 앱을 실행하고, `app/database.py`에서 DB 연결을 구성합니다.
- 현재 구현된 API는 `/save-od` 하나이며, 탐지 결과를 저장합니다.

## 2) 폴더 구조
```
practice/
  app/
    main.py         # FastAPI 앱 및 API 엔드포인트
    database.py     # DB 연결 및 세션 관리
    model.py        # SQLAlchemy 모델 정의
  venv/             # 가상환경(로컬)
  secrets.json      # DB 접속 정보(수동 생성 필요, Git 제외)
```

## 3) 사전 준비
- Python 3.12+
- MySQL 서버 설치 및 실행
- MySQL Workbench (선택)

## 4) 가상환경 생성/활성화
PowerShell 기준:
```
python -m venv venv
.\venv\Scripts\activate
```

## 5) 의존성 설치
```
pip install fastapi uvicorn sqlalchemy pymysql
```

## 6) DB 생성 (MySQL)
MySQL에서 DB 생성(예: `test_db`):
```sql
CREATE DATABASE test_db CHARACTER SET utf8mb4;
```

## 7) DB 접속 정보 설정
프로젝트 루트(`practice`)에 `secrets.json` 파일을 생성합니다.

`practice/secrets.json`
```json
{
  "DB": {
    "user": "test",
    "password": "비밀번호",
    "host": "127.0.0.1",
    "port": 3306,
    "database": "test_db"
  }
}
```

주의:
- `host`는 `127.0.0.1` 또는 `localhost` 사용
- `local host`처럼 공백이 들어가면 연결 실패
- 이 파일은 보안상 Git에 포함하지 않는 것을 권장

## 8) DB 연결 코드 구조
`app/database.py`에서 DB 연결을 구성합니다.

- `DB_URL`을 생성하여 `create_engine()`에 전달
- `SessionLocal`로 세션 생성
- `get_db()`로 요청마다 세션을 열고 닫도록 구성

현재 구성(요약):
```python
DB_URL = "mysql+pymysql://user:password@host:port/database?charset=utf8"
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

## 9) 모델 구조
현재 모델은 `DetectionResult` 하나이며, 테이블 이름은 `detection_results` 입니다.

필드:
- `id` (정수, PK)
- `image_name` (문자열)
- `label` (문자열)
- `confidence` (실수)
- `bbox` (JSON)
- `created_at` (Datetime, 기본값: 현재 시간)

정의 위치: `app/model.py`

## 10) 앱 실행
프로젝트 루트에서 실행:
```
uvicorn app.main:app --reload
```

정상 실행 시:
- http://127.0.0.1:8000 에서 서버 동작

## 11) 테이블 생성
현재 `app/main.py`의 `startup` 이벤트에서 `Base.metadata.create_all()`을 호출합니다.
즉, 서버 시작 시 테이블이 자동 생성됩니다.

```
@app.on_event("startup")
def create_tables() -> None:
    Base.metadata.create_all(bind=engine)
```

## 12) API 상세

### 12-1) POST /save-od
탐지 결과를 저장합니다.

요청 예시 (PowerShell):
```
irm "http://127.0.0.1:8000/save-od" -Method Post -ContentType "application/json" -Body '{"image_name":"test.jpg","label":"cat","conf":0.98,"bbox":[10,20,100,200]}'
```

요청 바디 필드:
- `image_name`: 이미지 파일명
- `label`: 분류 라벨
- `conf`: 신뢰도
- `bbox`: 바운딩 박스 정보(JSON 배열 등)

응답 예시:
```json
{"status":"success","id":1}
```

## 13) 자주 발생하는 오류/해결

### 13-1) `Import "sqlalchemy.orm" could not be resolved`
- venv에 `sqlalchemy`가 없거나 IDE가 venv를 못 잡는 경우
- 해결: `pip install sqlalchemy` 후 인터프리터를 venv로 설정

### 13-2) `FileNotFoundError: secrets.json`
- 프로젝트 루트에 `secrets.json`이 없는 경우
- 해결: `practice/secrets.json` 생성

### 13-3) `OperationalError: Table ... doesn't exist`
- 테이블 생성 전에 insert 요청한 경우
- 해결: 서버 재시작(자동 생성) 또는 `Base.metadata.create_all()` 실행

### 13-4) `CREATE command denied`
- DB 사용자 권한 부족
- 해결: CREATE 권한 부여 또는 root 계정 사용

## 14) Workbench에서 데이터 확인
1. Workbench 접속
2. 왼쪽 하단 `Schemas` 탭 클릭
3. DB 선택 → Tables 펼치기
4. `detection_results` 우클릭 → `Select Rows - Limit 1000`

## 15) 향후 확장 아이디어
- Pydantic 스키마 분리 (`schemas.py`)
- CRUD 모듈 분리
- 조회/삭제/리스트 API 추가
- 인증/권한 부여

