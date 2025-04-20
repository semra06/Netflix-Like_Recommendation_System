from sklearn.cluster import KMeans
import pandas as pd
from sqlalchemy.orm import Session
from models import User, Movie
import numpy as np

class MovieRecommender:
    def __init__(self, n_clusters=5):
        self.n_clusters = n_clusters
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.user_features = None
        self.movie_features = None

    def prepare_features(self, db: Session):
        # Kullanıcı özelliklerini hazırla
        users = db.query(User).all()
        user_data = []
        for user in users:
            user_data.append({
                'user_id': user.id,
                'cluster_id': user.cluster_id,
                'avg_rating': np.mean([movie.rating for movie in user.watched_movies]) if user.watched_movies else 0
            })
        self.user_features = pd.DataFrame(user_data)

        # Film özelliklerini hazırla
        movies = db.query(Movie).all()
        movie_data = []
        for movie in movies:
            movie_data.append({
                'movie_id': movie.id,
                'cluster_id': movie.cluster_id,
                'rating': movie.rating,
                'release_year': movie.release_year
            })
        self.movie_features = pd.DataFrame(movie_data)

    def fit(self, db: Session):
        self.prepare_features(db)
        
        # Kullanıcıları kümelere ayır
        user_clusters = self.kmeans.fit_predict(self.user_features[['avg_rating']])
        for i, user in enumerate(db.query(User).all()):
            user.cluster_id = int(user_clusters[i])
        
        # Filmleri kümelere ayır
        movie_clusters = self.kmeans.fit_predict(self.movie_features[['rating', 'release_year']])
        for i, movie in enumerate(db.query(Movie).all()):
            movie.cluster_id = int(movie_clusters[i])
        
        db.commit()

    def recommend_movies(self, db: Session, user_id: int, n_recommendations: int = 5):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return []

        # Kullanıcının kümesindeki filmleri bul
        cluster_movies = db.query(Movie).filter(Movie.cluster_id == user.cluster_id).all()
        
        # Kullanıcının izlemediği filmleri filtrele
        unwatched_movies = [movie for movie in cluster_movies if movie not in user.watched_movies]
        
        # Filmleri rating'e göre sırala
        recommended_movies = sorted(unwatched_movies, key=lambda x: x.rating, reverse=True)
        
        return recommended_movies[:n_recommendations] 