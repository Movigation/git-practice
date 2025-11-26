-- 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS moviesir 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

USE moviesir;

-- 영화의 핵심 메타데이터 저장
-- TMDB API에서 수집한 데이터 구조 기반

CREATE TABLE IF NOT EXISTS movies (
    id INT PRIMARY KEY COMMENT 'TMDB 영화 고유 ID',
    title VARCHAR(255) NOT NULL COMMENT '영화 제목',
    title_en VARCHAR(255) COMMENT '영화 영문 제목',
    poster_path TEXT COMMENT '포스터 이미지 경로 (/path/to/poster.jpg)',
    overview TEXT COMMENT '영화 줄거리/시놉시스',
    release_date DATE COMMENT '개봉일',
    
    -- 핵심 기능 1: 런타임 필터
    runtime INT COMMENT '상영 시간 (분 단위)',
    
    -- 핵심 기능 4: 평점/인기 정렬
    vote_average DECIMAL(3,1) COMMENT 'TMDB 평점 (0.0 ~ 10.0)',
    vote_count INT COMMENT '평점 참여자 수',
    popularity DECIMAL(8,3) COMMENT 'TMDB 인기 지수',
    
    -- 메타 정보
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '데이터 생성 시각',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '데이터 수정 시각',
    
    -- 인덱스: 필터링 및 정렬 성능 최적화
    INDEX idx_runtime (runtime),
    INDEX idx_vote_average (vote_average),
    INDEX idx_popularity (popularity),
    INDEX idx_release_date (release_date)
    
) ENGINE=InnoDB COMMENT='영화 메인 테이블';

-- =====================================================
-- 2. 장르 마스터 테이블 (genres)
-- =====================================================
-- TMDB 표준 장르 목록 저장

CREATE TABLE IF NOT EXISTS genres (
    id INT PRIMARY KEY COMMENT 'TMDB 장르 고유 ID',
    name VARCHAR(100) NOT NULL COMMENT '장르 영문명 (Action, Drama 등)',
    name_kr VARCHAR(100) COMMENT '장르 한글명 (액션, 드라마 등)'
) ENGINE=InnoDB COMMENT='장르 마스터 테이블';

-- =====================================================
-- 3. 영화-장르 연결 테이블 (movie_genres)
-- =====================================================
-- 핵심 기능 2: 장르 기반 필터
-- 다대다(N:N) 관계: 한 영화는 여러 장르, 한 장르는 여러 영화

CREATE TABLE IF NOT EXISTS movie_genres (
    movie_id INT NOT NULL COMMENT '영화 ID (FK)',
    genre_id INT NOT NULL COMMENT '장르 ID (FK)',
    
    PRIMARY KEY (movie_id, genre_id),
    
    FOREIGN KEY (movie_id) 
        REFERENCES movies(id) 
        ON DELETE CASCADE
        COMMENT '영화 삭제 시 연결 데이터도 삭제',
    
    FOREIGN KEY (genre_id) 
        REFERENCES genres(id) 
        ON DELETE CASCADE
        COMMENT '장르 삭제 시 연결 데이터도 삭제',
    
    -- 인덱스: 장르별 영화 검색 최적화
    INDEX idx_genre_id (genre_id)
    
) ENGINE=InnoDB COMMENT='영화-장르 매핑 테이블 (N:N)';

-- =====================================================
-- 4. OTT 제공자 마스터 테이블 (ott_providers)
-- =====================================================
-- Netflix, Disney+, Tving 등 OTT 서비스 정보

CREATE TABLE IF NOT EXISTS ott_providers (
    id INT PRIMARY KEY COMMENT 'TMDB provider 고유 ID',
    name VARCHAR(100) NOT NULL COMMENT 'OTT 서비스명 (Netflix, Disney+ 등)',
    logo_path TEXT COMMENT 'OTT 로고 이미지 경로'
) ENGINE=InnoDB COMMENT='OTT 제공자 마스터 테이블';

-- =====================================================
-- 5. 영화-OTT 연결 테이블 (movie_providers)
-- =====================================================
-- 핵심 기능 3: OTT 필터
-- 다대다(N:N) 관계: 한 영화는 여러 OTT, 한 OTT는 여러 영화

CREATE TABLE IF NOT EXISTS movie_providers (
    movie_id INT NOT NULL COMMENT '영화 ID (FK)',
    provider_id INT NOT NULL COMMENT 'OTT 제공자 ID (FK)',
    region VARCHAR(2) DEFAULT 'KR' COMMENT '제공 지역 (한국 기준)',
    
    PRIMARY KEY (movie_id, provider_id),
    
    FOREIGN KEY (movie_id) 
        REFERENCES movies(id) 
        ON DELETE CASCADE
        COMMENT '영화 삭제 시 연결 데이터도 삭제',
    
    FOREIGN KEY (provider_id) 
        REFERENCES ott_providers(id) 
        ON DELETE CASCADE
        COMMENT 'OTT 제공자 삭제 시 연결 데이터도 삭제',
    
    -- 인덱스: OTT별 영화 검색 최적화
    INDEX idx_provider_id (provider_id)
    
) ENGINE=InnoDB COMMENT='영화-OTT 매핑 테이블 (N:N)';

-- =====================================================
-- 초기 데이터 삽입
-- =====================================================

-- 장르 초기 데이터 (TMDB 표준 장르)
INSERT INTO genres (id, name, name_kr) VALUES
(28, 'Action', '액션'),
(12, 'Adventure', '어드벤처'),
(16, 'Animation', '애니메이션'),
(35, 'Comedy', '코미디'),
(80, 'Crime', '범죄'),
(99, 'Documentary', '다큐멘터리'),
(18, 'Drama', '드라마'),
(10751, 'Family', '가족'),
(14, 'Fantasy', '판타지'),
(36, 'History', '역사'),
(27, 'Horror', '공포'),
(10402, 'Music', '음악'),
(9648, 'Mystery', '미스터리'),
(10749, 'Romance', '로맨스'),
(878, 'Science Fiction', 'SF'),
(10770, 'TV Movie', 'TV 영화'),
(53, 'Thriller', '스릴러'),
(10752, 'War', '전쟁'),
(37, 'Western', '서부')
ON DUPLICATE KEY UPDATE name=VALUES(name), name_kr=VALUES(name_kr);

-- 주요 OTT 제공자 초기 데이터
INSERT INTO ott_providers (id, name) VALUES
(8, 'Netflix'),
(337, 'Disney Plus'),
(356, 'Tving'),
(97, 'Watcha'),
(350, 'Wavve')
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- =====================================================
-- 유용한 쿼리 예시
-- =====================================================

-- 1. 런타임 기반 영화 검색 (120분 ±15분)
-- SELECT * FROM movies 
-- WHERE runtime BETWEEN 105 AND 135
-- ORDER BY vote_average DESC;

-- 2. 장르 기반 영화 검색 (액션 장르)
-- SELECT m.* FROM movies m
-- JOIN movie_genres mg ON m.id = mg.movie_id
-- WHERE mg.genre_id = 28
-- ORDER BY m.popularity DESC;

-- 3. OTT 기반 영화 검색 (Netflix에서 볼 수 있는 영화)
-- SELECT m.* FROM movies m
-- JOIN movie_providers mp ON m.id = mp.movie_id
-- WHERE mp.provider_id = 8;

-- 4. 복합 필터 (런타임 + 장르 + OTT + 평점순)
-- SELECT DISTINCT m.* FROM movies m
-- JOIN movie_genres mg ON m.id = mg.movie_id
-- JOIN movie_providers mp ON m.id = mp.movie_id
-- WHERE m.runtime BETWEEN 105 AND 135
--   AND mg.genre_id IN (28, 35)
--   AND mp.provider_id IN (8, 337)
-- ORDER BY m.vote_average DESC
-- LIMIT 20;

-- =====================================================
-- 테이블 정보 확인
-- =====================================================

-- SHOW TABLES;
-- DESCRIBE movies;
-- DESCRIBE genres;
-- DESCRIBE movie_genres;
-- DESCRIBE ott_providers;
-- DESCRIBE movie_providers;