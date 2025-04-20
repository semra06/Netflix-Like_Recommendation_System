from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
from database import engine, get_db, SessionLocal
from recommender import MovieRecommender
from pydantic import BaseModel

# Veritabanı tablolarını oluştur
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Netflix Benzeri Öneri Sistemi")

# Pydantic modelleri
class MovieBase(BaseModel):
    title: str
    genre: str
    release_year: int
    rating: float
    description: str

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    id: int
    cluster_id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    cluster_id: int

    class Config:
        from_attributes = True

# Öneri sistemi örneği
recommender = MovieRecommender()

# API başlatıldığında öneri sistemini eğit
@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    recommender.fit(db)
    db.close()

@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=user.password  # Gerçek uygulamada şifre hash'lenmelidir
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/movies/", response_model=Movie)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    db_movie = models.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@app.post("/users/{user_id}/rate/{movie_id}")
def rate_movie(user_id: int, movie_id: int, rating: float, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    
    if not user or not movie:
        raise HTTPException(status_code=404, detail="User or movie not found")
    
    # Kullanıcı-film ilişkisini güncelle
    user.watched_movies.append(movie)
    db.commit()
    
    # Öneri sistemini güncelle
    recommender.fit(db)
    
    return {"message": "Rating added successfully"}

@app.get("/users/{user_id}/recommendations", response_model=List[Movie])
def get_recommendations(user_id: int, db: Session = Depends(get_db)):
    try:
        recommended_movies = recommender.recommend_movies(db, user_id)
        if not recommended_movies:
            raise HTTPException(status_code=404, detail="No recommendations found for this user")
        return recommended_movies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 