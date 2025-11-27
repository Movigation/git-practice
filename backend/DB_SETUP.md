# 무비서 데이터베이스 설정 가이드

## 백엔드 팀원용

---

## 1️⃣ MySQL 설치 및 설정

### MySQL 설치

**macOS (Homebrew):**

```bash
# Homebrew 없으면 먼저 설치
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# MySQL 설치
brew install mysql

# MySQL 시작
brew services start mysql

# 또는 일회성 실행
mysql.server start
```

**Windows (WSL2):**

```bash
sudo apt update
sudo apt install mysql-server -y
sudo service mysql start
```

### DB 및 사용자 생성

**macOS:**

```bash
# Mac은 기본적으로 비밀번호 없이 root 접속 가능
mysql -u root
```

**Windows (WSL2):**

```bash
sudo mysql -u root -p
```

**MySQL 프롬프트에서 실행:**

```sql
CREATE DATABASE moviesir CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'dev_user'@'localhost' IDENTIFIED BY 'dev_password';
GRANT ALL PRIVILEGES ON moviesir.* TO 'dev_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

---

## 2️⃣ 스키마 적용

```bash
cd backend
mysql -u dev_user -p moviesir < schema.sql
# 비밀번호: dev_password
```

**확인:**

```bash
mysql -u dev_user -p moviesir
```

```sql
SHOW TABLES;  -- 5개 테이블
SELECT COUNT(*) FROM genres;  -- 19개
SELECT * FROM ott_providers;  -- 5개
EXIT;
```

---

## 3️⃣ 데이터 삽입 (선택)

### 데이터 다운로드

**Google Drive:** [문수현님 공유 링크]

- `trend_final_complete.json` (4,000개)
- `2019_data.json` (13,000개)

→ `backend/data/` 폴더에 저장

### 삽입 실행

```bash
pip install mysql-connector-python

cd backend/scripts
python3 insert_data.py ../data/trend_final_complete.json
```

---

## 4️⃣ 기능 테스트

```sql
-- 넷플릭스 120분 액션 영화 추천
SELECT DISTINCT m.title, m.runtime, m.vote_average
FROM movies m
JOIN movie_genres mg ON m.id = mg.movie_id
JOIN movie_providers mp ON m.id = mp.movie_id
WHERE m.runtime BETWEEN 105 AND 135
  AND mg.genre_id = 28
  AND mp.provider_id = 8
ORDER BY m.vote_average DESC
LIMIT 5;
```

---

## 주요 ID

**장르:**

- 28 = 액션
- 35 = 코미디
- 18 = 드라마
- 전체: `SELECT * FROM genres;`

**OTT:**

- 8 = Netflix
- 337 = Disney Plus
- 356 = Tving
- 전체: `SELECT * FROM ott_providers;`

---

## 문제 해결

**MySQL 재시작:**

macOS:

```bash
brew services restart mysql
# 또는
mysql.server restart
```

**비밀번호 재설정:**

macOS:

```bash
mysql -u root
```

```sql
ALTER USER 'dev_user'@'localhost' IDENTIFIED BY 'dev_password';
FLUSH PRIVILEGES;
EXIT;
```

---
