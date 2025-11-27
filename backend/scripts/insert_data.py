#!/usr/bin/env python3
"""
TMDB 크롤링 데이터를 MySQL 데이터베이스에 삽입하는 스크립트

사용법:
    python insert_data.py [JSON 파일 경로]
    
예시:
    python insert_data.py ../data/trend_final_complete.json
    python insert_data.py ../data/2019_data.json
"""

import json
import sys
import mysql.connector
from mysql.connector import Error
from pathlib import Path
from datetime import datetime

# DB 연결 정보 (실제 사용 시 .env에서 로드 권장)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'dev_user',  # 본인의 MySQL 사용자명
    'password': 'dev_password',  # 본인의 MySQL 비밀번호
    'database': 'moviesir'
}

def connect_db():
    """MySQL 데이터베이스 연결"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print(f"MySQL 연결 성공: {DB_CONFIG['database']}")
        return conn
    except Error as e:
        print(f"MySQL 연결 실패: {e}")
        sys.exit(1)

def load_json_file(file_path):
    """JSON 파일 로드"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"JSON 파일 로드 성공: {len(data)}개 영화")
        return data
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {file_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"JSON 파싱 실패: {e}")
        sys.exit(1)

def insert_movie(cursor, movie):
    """movies 테이블에 영화 데이터 삽입"""
    try:
        sql = """
            INSERT INTO movies 
            (id, title, title_en, poster_path, overview, release_date, 
             runtime, vote_average, vote_count, popularity)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                title = VALUES(title),
                title_en = VALUES(title_en),
                poster_path = VALUES(poster_path),
                overview = VALUES(overview),
                release_date = VALUES(release_date),
                runtime = VALUES(runtime),
                vote_average = VALUES(vote_average),
                vote_count = VALUES(vote_count),
                popularity = VALUES(popularity),
                updated_at = CURRENT_TIMESTAMP
        """
        
        values = (
            movie.get('id'),
            movie.get('title'),
            movie.get('original_title'),  # title_en으로 사용
            movie.get('poster_path'),
            movie.get('overview'),
            movie.get('release_date'),
            movie.get('runtime'),
            movie.get('vote_average'),
            movie.get('vote_count', 0),
            movie.get('popularity')
        )
        
        cursor.execute(sql, values)
        return True
    except Error as e:
        print(f"  영화 삽입 실패 (ID: {movie.get('id')}): {e}")
        return False

def insert_genres(cursor, movie):
    """movie_genres 테이블에 장르 데이터 삽입"""
    movie_id = movie.get('id')
    genres = movie.get('genres', [])
    
    if not genres:
        return 0
    
    success_count = 0
    for genre in genres:
        try:
            # genres 테이블에 장르가 있는지 확인 (이미 schema.sql에서 삽입됨)
            # movie_genres에 연결 데이터 삽입
            sql = """
                INSERT IGNORE INTO movie_genres (movie_id, genre_id)
                VALUES (%s, %s)
            """
            cursor.execute(sql, (movie_id, genre.get('id')))
            success_count += 1
        except Error as e:
            print(f"  장르 삽입 실패 (영화: {movie_id}, 장르: {genre.get('id')}): {e}")
    
    return success_count

def insert_providers(cursor, movie):
    """movie_providers 테이블에 OTT 데이터 삽입"""
    movie_id = movie.get('id')
    providers = movie.get('providers', [])
    
    if not providers:
        return 0
    
    success_count = 0
    for provider in providers:
        try:
            provider_id = provider.get('provider_id')
            provider_name = provider.get('provider_name')
            
            if not provider_id:
                continue
            
            # ott_providers 테이블에 provider 추가 (없으면)
            sql_provider = """
                INSERT IGNORE INTO ott_providers (id, name)
                VALUES (%s, %s)
            """
            cursor.execute(sql_provider, (provider_id, provider_name))
            
            # movie_providers에 연결 데이터 삽입
            sql_movie_provider = """
                INSERT IGNORE INTO movie_providers (movie_id, provider_id, region)
                VALUES (%s, %s, 'KR')
            """
            cursor.execute(sql_movie_provider, (movie_id, provider_id))
            success_count += 1
        except Error as e:
            print(f"  OTT 삽입 실패 (영화: {movie_id}, OTT: {provider.get('provider_name')}): {e}")
    
    return success_count

def insert_movies_batch(conn, movies):
    """영화 데이터 일괄 삽입"""
    cursor = conn.cursor()
    
    stats = {
        'total': len(movies),
        'movies_success': 0,
        'movies_failed': 0,
        'genres_inserted': 0,
        'providers_inserted': 0
    }
    
    print(f"\n데이터 삽입 시작 (총 {stats['total']}개 영화)")
    print("=" * 60)
    
    for idx, movie in enumerate(movies, 1):
        movie_id = movie.get('id')
        title = movie.get('title', 'Unknown')
        
        # 진행률 표시 (100개마다)
        if idx % 100 == 0:
            print(f"진행중... {idx}/{stats['total']} ({idx/stats['total']*100:.1f}%)")
        
        try:
            # 1. 영화 기본 정보 삽입
            if insert_movie(cursor, movie):
                stats['movies_success'] += 1
            else:
                stats['movies_failed'] += 1
                continue
            
            # 2. 장르 삽입
            genre_count = insert_genres(cursor, movie)
            stats['genres_inserted'] += genre_count
            
            # 3. OTT 제공자 삽입
            provider_count = insert_providers(cursor, movie)
            stats['providers_inserted'] += provider_count
            
            # 매 100개마다 커밋
            if idx % 100 == 0:
                conn.commit()
        
        except Exception as e:
            print(f"  영화 처리 실패 (ID: {movie_id}, 제목: {title}): {e}")
            stats['movies_failed'] += 1
    
    # 최종 커밋
    conn.commit()
    cursor.close()
    
    return stats

def print_statistics(stats):
    """통계 출력"""
    print("\n" + "=" * 60)
    print("데이터 삽입 완료!")
    print("=" * 60)
    print(f"총 영화 수:        {stats['total']}개")
    print(f"성공:             {stats['movies_success']}개")
    print(f"실패:             {stats['movies_failed']}개")
    print(f"장르 연결:         {stats['genres_inserted']}개")
    print(f"OTT 연결:          {stats['providers_inserted']}개")
    print(f"성공률:           {stats['movies_success']/stats['total']*100:.1f}%")
    print("=" * 60)

def verify_data(conn):
    """삽입된 데이터 검증"""
    cursor = conn.cursor()
    
    print("\n데이터 검증 중...")
    print("-" * 60)
    
    # 영화 수 확인
    cursor.execute("SELECT COUNT(*) FROM movies")
    movie_count = cursor.fetchone()[0]
    print(f"총 영화 수: {movie_count}개")
    
    # 장르 연결 수 확인
    cursor.execute("SELECT COUNT(*) FROM movie_genres")
    genre_count = cursor.fetchone()[0]
    print(f"장르 연결 수: {genre_count}개")
    
    # OTT 연결 수 확인
    cursor.execute("SELECT COUNT(*) FROM movie_providers")
    provider_count = cursor.fetchone()[0]
    print(f"OTT 연결 수: {provider_count}개")
    
    # 런타임 있는 영화 수
    cursor.execute("SELECT COUNT(*) FROM movies WHERE runtime IS NOT NULL AND runtime > 0")
    runtime_count = cursor.fetchone()[0]
    print(f"런타임 정보 있는 영화: {runtime_count}개 ({runtime_count/movie_count*100:.1f}%)")
    
    # 샘플 영화 5개 출력
    print("\n샘플 영화 (최근 5개):")
    cursor.execute("""
        SELECT id, title, runtime, vote_average, popularity 
        FROM movies 
        ORDER BY created_at DESC 
        LIMIT 5
    """)
    
    for movie in cursor.fetchall():
        print(f"  - ID: {movie[0]}, 제목: {movie[1]}, 런타임: {movie[2]}분, 평점: {movie[3]}")
    
    cursor.close()
    print("-" * 60)

def main():
    """메인 함수"""
    print("=" * 60)
    print("TMDB 영화 데이터 삽입 스크립트")
    print("=" * 60)
    
    # 파일 경로 확인
    if len(sys.argv) < 2:
        print("\n사용법: python insert_data.py [JSON 파일 경로]")
        print("예시: python insert_data.py ../data/trend_final_complete.json")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    # JSON 파일 로드
    movies = load_json_file(file_path)
    
    # DB 연결
    conn = connect_db()
    
    try:
        # 데이터 삽입
        stats = insert_movies_batch(conn, movies)
        
        # 통계 출력
        print_statistics(stats)
        
        # 검증
        verify_data(conn)
        
    finally:
        conn.close()
        print("\nMySQL 연결 종료")

if __name__ == "__main__":
    main()
