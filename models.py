from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Kullanıcı ve film arasındaki ilişki tablosu
user_movie_association = Table(
    'user_movie_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('rating', Float)
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    cluster_id = Column(Integer)  # K-means küme ID'si

    # İlişkiler
    watched_movies = relationship("Movie", secondary=user_movie_association, back_populates="watched_by")

class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    genre = Column(String)
    release_year = Column(Integer)
    rating = Column(Float)
    description = Column(String)
    cluster_id = Column(Integer)  # K-means küme ID'si

    # İlişkiler
    watched_by = relationship("User", secondary=user_movie_association, back_populates="watched_movies") 