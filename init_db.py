import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv()

def create_database():
    # PostgreSQL bağlantı bilgileri
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    
    try:
        # Veritabanını oluştur
        cur.execute("CREATE DATABASE netflix_recommender")
        print("Veritabanı başarıyla oluşturuldu!")
    except psycopg2.Error as e:
        print(f"Hata oluştu: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    create_database() 