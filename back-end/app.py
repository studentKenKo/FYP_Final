from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import psycopg2
import spacy
import time
from spacy.lang.en.stop_words import STOP_WORDS

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='postgres',
                            user='postgres',
                            password='imdb123')
    return conn

@app.route("/movies")
def GetMovies():
    # db
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM movies LIMIT 30;')
    movies = cur.fetchall()
    cur.close()
    conn.close()
    print('GetMovies')
    return {
        'result': movies
    }


@app.route('/movie/<sentence>', methods=['GET'])
def querBySentence(sentence):
    # print("type(sentence) : ", type(sentence))
    persons = []
    dates = []
    tokens = []
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            persons.append(ent.text)
        if ent.label_ == "DATE":
            dates.append(ent.text)
        print(ent.text, ent.label_)
        print('persons', persons)
        print('dates', dates)

    stop_words = spacy.lang.en.stop_words.STOP_WORDS
    doc = [word for word in doc if word not in stop_words and word and len(word) > 2]
    for token in doc:
        tokens.append(token.text)
    print(tokens)

    # db
    conn = get_db_connection()
    cur = conn.cursor()
    if len(persons) > 0 and len(dates) > 0:
        cur.execute(
            "SELECT * FROM movies where actors like '%{}%' AND releasedate like '%{}%'".format(persons[0], dates[0]))
        movies = cur.fetchall()
    elif len(persons) > 0:
        cur.execute("SELECT * FROM movies where actors like '%{}%'".format(persons[0]))
        movies = cur.fetchall()
    elif len(dates) > 0:
        cur.execute("SELECT * FROM movies where releasedate like '%{}%'".format(dates[0]))
        movies = cur.fetchall()
    else:
        movies = []
    cur.close()
    conn.close()

    return {
        "person": persons,
        "date": dates,
        "token": tokens,
        "result": movies
    }

