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

## 1. Git 레포지토리 클론

```bash
git clone https://github.com/Movi-T/git-practice.git
cd git-practice
```

---

## FE

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

### 4. PUSH

```bash
git push -u origin feature/fe-작업명

```

---

## BE

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

### 4. PUSH

```bash
git push -u origin feature/be-작업명

```

---
