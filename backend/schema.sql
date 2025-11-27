CREATE DATABASE IF NOT EXISTS moviesir 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

USE moviesir;

-- =====================================================
-- 1. 영화 기본 정보 테이블
-- =====================================================

CREATE TABLE IF NOT EXISTS movies (
    id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    title_en VARCHAR(255),
    poster_path TEXT,
    overview TEXT,
    release_date DATE,
    runtime INT,
    vote_average DECIMAL(3,1),
    vote_count INT,
    popularity DECIMAL(8,3),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_runtime (runtime),
    INDEX idx_vote_average (vote_average),
    INDEX idx_popularity (popularity),
    INDEX idx_release_date (release_date)
) ENGINE=InnoDB;

-- =====================================================
-- 2. 장르 마스터 테이블
-- =====================================================

CREATE TABLE IF NOT EXISTS genres (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    name_kr VARCHAR(100)
) ENGINE=InnoDB;

-- =====================================================
-- 3. 영화-장르 연결 테이블
-- =====================================================

CREATE TABLE IF NOT EXISTS movie_genres (
    movie_id INT NOT NULL,
    genre_id INT NOT NULL,
    PRIMARY KEY (movie_id, genre_id),
    
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genres(id) ON DELETE CASCADE,
    
    INDEX idx_genre_id (genre_id)
) ENGINE=InnoDB;

-- =====================================================
-- 4. OTT 제공자 마스터 테이블
-- =====================================================

CREATE TABLE IF NOT EXISTS ott_providers (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    logo_path TEXT
) ENGINE=InnoDB;

-- =====================================================
-- 5. 영화-OTT 연결 테이블
-- =====================================================

CREATE TABLE IF NOT EXISTS movie_providers (
    movie_id INT NOT NULL,
    provider_id INT NOT NULL,
    region VARCHAR(2) DEFAULT 'KR',
    PRIMARY KEY (movie_id, provider_id),
    
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE,
    FOREIGN KEY (provider_id) REFERENCES ott_providers(id) ON DELETE CASCADE,
    
    INDEX idx_provider_id (provider_id)
) ENGINE=InnoDB;

-- =====================================================
-- 초기 데이터 삽입
-- =====================================================

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

INSERT INTO ott_providers (id, name) VALUES
(8, 'Netflix'),
(337, 'Disney Plus'),
(356, 'Tving'),
(97, 'Watcha'),
(350, 'Wavve')
ON DUPLICATE KEY UPDATE name=VALUES(name);