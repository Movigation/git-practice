# git-practice

## 폴더 구조

```markdown
.
├── README.md
├── backend
└── frontend
```

---

## 브랜치 구조

```markdown
main
dev
fe-dev
be-dev
```

---

## 📌 fe-dev / be-dev에서 main merge가 필요한 상황

1. PM이 공용 파일을 수정했을 때 (README, 폴더 구조, .gitignore 등)
2. 프로젝트 전체에 영향 있는 설정이 변경됐을 때
3. main에 내가 꼭 받아야 하는 코드가 생겼을 때

그 외엔 merge main 안 해도 됩니다!

```bash
git pull
git merge main
```

---

## 1. Git 레포지토리 클론

```bash
git clone https://github.com/Movi-T/git-practice.git
cd git-practice
```

---

## 프론트엔드

### 1. 루트로 이동

```bash
cd git-practice
```

### 2. fe-dev로 이동

```nginx
git checkout fe-dev
git pull
```

---

### 3. feature 브랜치 만들기

```bash
git checkout -b feature/fe-작업명       예) feature/fe-login
```

---

### 4. PUSH (최초 1회는 -u 필요)

```bash
git push -u origin feature/fe-작업명

```

---

## 백엔드

### 1. 루트로 이동

```bash
cd git-practice
```

### 2. fe-dev로 이동

```nginx
git checkout be-dev
git pull
```

---

### 3. feature 브랜치 만들기

```bash
git checkout -b feature/be-작업명       예) feature/be-search-api
```

---

### 4. PUSH (최초 1회는 -u 필요)

```bash
git push -u origin feature/be-작업명

```

---
