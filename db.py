import sqlalchemy
from auth import db_auth

db = f'postgresql://postgres:{db_auth}@localhost:5432/postgres'
engine = sqlalchemy.create_engine(db)
connection = engine.connect()


def db():
    connection.execute("""
    CREATE TABLE if not exists Users (
    id INTEGER PRIMARY KEY
    );
    
    CREATE TABLE if not exists Candidates (
    id INTEGER PRIMARY KEY
    );
    
    CREATE TABLE if not exists User_to_Candidates (
    user_id INTEGER REFERENCES Users(id),
    candidates_id INTEGER REFERENCES Candidates(id),
    constraint pk PRIMARY KEY (user_id, candidates_id)
    );
    
    CREATE TABLE if not exists Photos (
    id serial PRIMARY KEY,
    photo_link TEXT,
    candidate_id INTEGER REFERENCES Candidates(id)
    );
    """)


def user_db(user_id):
    connection.execute(f'INSERT INTO Users(id) VALUES ({user_id}) ON CONFLICT DO NOTHING')


def candidate_db(candidate_id):
    connection.execute(f"INSERT INTO Candidates(id) VALUES ({candidate_id}) ON CONFLICT DO NOTHING")


def user_to_candidates(user_id, candidate_id):
    connection.execute(f"INSERT INTO User_to_Candidates(candidates_id, user_id, ) VALUES ({candidate_id}, {user_id})")


def photos_db(candidate_id, link):
    connection.execute(f"INSERT INTO Photos(candidate_id, photo_link) VALUES ({candidate_id}, {link})")

# def del_db():
#     connection.execute("""
#     DROP TABLE Users, Candidates, Photos, User_to_Candidates CASCADE;
#     """)
#
# del_db()
