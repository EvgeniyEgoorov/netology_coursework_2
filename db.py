from sqlalchemy import exc
import sqlalchemy.exc
from auth import db_auth

try:
    db = f'postgresql://postgres:{db_auth}@localhost:5432/postgres'
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()
except exc.SQLAlchemyError:
    print('Ошибка при работе с базой!')
    pass


def db():
    try:
        connection.execute("""
        CREATE TABLE if not exists Users (
        id INTEGER PRIMARY KEY
        );
        
        CREATE TABLE if not exists Candidates (
        id INTEGER PRIMARY KEY,
        name VARCHAR(40),
        surname VARCHAR(40)
        );
        
        CREATE TABLE if not exists User_to_Candidates (
        user_id INTEGER REFERENCES Users(id),
        candidates_id INTEGER REFERENCES Candidates(id),
        constraint pk PRIMARY KEY (user_id, candidates_id)
        );
        
        CREATE TABLE if not exists Photos (
        candidate_id INTEGER REFERENCES Candidates(id),
        photo_link VARCHAR(300)
        );
        """)
    except NameError:
        print('Ошибка при работе с базой!')
        pass


def user_db(user_id):
    insert_query = """
    INSERT INTO Users(id) 
    VALUES (%s) ON CONFLICT DO NOTHING
    """
    try:
        connection.execute(insert_query, user_id)
    except NameError:
        pass


def candidate_db(candidate_id, first_name, last_name):
    insert_query = """
    INSERT INTO Candidates(id, name, surname)
    VALUES (%s,%s,%s) ON CONFLICT DO NOTHING
    """
    candidate_data = (candidate_id, first_name, last_name)
    try:
        connection.execute(insert_query, candidate_data)
    except NameError:
        pass


def user_to_candidates(user_id, candidate_id):
    insert_query = """
    INSERT INTO User_to_Candidates(user_id, candidates_id) 
    VALUES (%s,%s)
    """
    relation_data = (user_id, candidate_id)
    try:
        connection.execute(insert_query, relation_data)
    except NameError:
        pass


def photos_db(candidate_id, link):
    insert_query = """
    INSERT INTO Photos(candidate_id, photo_link) 
    VALUES (%s,%s)
    """
    photos_data = (candidate_id, link)
    try:
        connection.execute(insert_query, photos_data)
    except NameError:
        pass

# def del_db():
#     connection.execute("""
#     DROP TABLE Users, Candidates, Photos, User_to_Candidates CASCADE;
#     """)
#
#
# del_db()
