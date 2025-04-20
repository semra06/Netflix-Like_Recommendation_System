from sqlalchemy.orm import Session
from models import User, Movie
from database import SessionLocal

def create_sample_data():
    db = SessionLocal()
    
    # Örnek filmler
    movies = [
        Movie(
            title="Inception",
            genre="Science Fiction",
            release_year=2010,
            rating=8.8,
            description="A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O."
        ),
        Movie(
            title="The Dark Knight",
            genre="Action",
            release_year=2008,
            rating=9.0,
            description="When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice."
        ),
        Movie(
            title="Pulp Fiction",
            genre="Crime",
            release_year=1994,
            rating=8.9,
            description="The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption."
        ),
        Movie(
            title="The Shawshank Redemption",
            genre="Drama",
            release_year=1994,
            rating=9.3,
            description="Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."
        ),
        Movie(
            title="Forrest Gump",
            genre="Drama",
            release_year=1994,
            rating=8.8,
            description="The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with an IQ of 75, whose only desire is to be reunited with his childhood sweetheart."
        ),
        Movie(
            title="The Matrix",
            genre="Science Fiction",
            release_year=1999,
            rating=8.7,
            description="A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers."
        ),
        Movie(
            title="Fight Club",
            genre="Drama",
            release_year=1999,
            rating=8.8,
            description="An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into something much, much more."
        ),
        Movie(
            title="The Godfather",
            genre="Crime",
            release_year=1972,
            rating=9.2,
            description="The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son."
        ),
        Movie(
            title="Interstellar",
            genre="Science Fiction",
            release_year=2014,
            rating=8.6,
            description="A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival."
        ),
        Movie(
            title="The Lord of the Rings: The Fellowship of the Ring",
            genre="Fantasy",
            release_year=2001,
            rating=8.8,
            description="A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron."
        )
    ]
    
    # Örnek kullanıcılar
    users = [
        User(
            username="john_doe",
            email="john@example.com",
            hashed_password="password123"
        ),
        User(
            username="jane_smith",
            email="jane@example.com",
            hashed_password="password123"
        ),
        User(
            username="mike_wilson",
            email="mike@example.com",
            hashed_password="password123"
        ),
        User(
            username="sarah_jones",
            email="sarah@example.com",
            hashed_password="password123"
        ),
        User(
            username="david_brown",
            email="david@example.com",
            hashed_password="password123"
        )
    ]
    
    # Veritabanına ekle
    for movie in movies:
        db.add(movie)
    
    for user in users:
        db.add(user)
    
    db.commit()
    
    # Kullanıcı-film ilişkilerini oluştur
    # John Doe'nun izlediği filmler
    users[0].watched_movies.extend([movies[0], movies[1], movies[2]])
    # Jane Smith'in izlediği filmler
    users[1].watched_movies.extend([movies[3], movies[4], movies[5]])
    # Mike Wilson'ın izlediği filmler
    users[2].watched_movies.extend([movies[6], movies[7], movies[8]])
    # Sarah Jones'un izlediği filmler
    users[3].watched_movies.extend([movies[0], movies[3], movies[6]])
    # David Brown'un izlediği filmler
    users[4].watched_movies.extend([movies[1], movies[4], movies[7]])
    
    db.commit()
    db.close()

if __name__ == "__main__":
    create_sample_data()
    print("Sample data has been created successfully!") 