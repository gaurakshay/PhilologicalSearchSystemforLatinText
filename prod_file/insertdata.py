#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Program to insert fetched data into database."""
import sqlite3 as db
import codecs
import json
import fnmatch
import os

tuples = []

def create_tuples_from_file(filename):
    global tuples
    with codecs.open(filename, 'r', encoding='utf-8') as file:
        data = json.loads(file.read())
        date_ = data['dates']
        book = data['books']
        language = data['language']
        author_name = data['author_name']
        title = data['title']
        for book in data['books']:
            bookname = book['bookname']
            for chapter in book['chapters']:
                chaptername = chapter['chapter']
                for verse in chapter['verses']:
                    verseid = verse['verse']
                    passage = verse['passage']
                    link = verse['link']
                    tuple = (title, bookname, language, author_name
                             , date_, chaptername, verseid, passage, link)
                    tuples.append(tuple)


def insert_data():
    conn = db.connect('latinworks.db')
    with conn:
        cur = conn.cursor()
        cur.executescript("""
                          DROP TABLE IF EXISTS latinworks;
                          CREATE TABLE latinworks(
                              title text,
                              book text,
                              language text,
                              author text,
                              dates text,
                              chapter text,
                              verse text,
                              passage text,
                              link text);
                          """)
        cur.executemany("""INSERT INTO latinworks
                        VALUES(?,?,?,?,?,?,?,?,?)
                        """, tuples)
        conn.commit()
        cur.execute('SELECT COUNT(*) FROM latinworks')
        return cur.fetchone()[0]


def create_tuples():
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, '*.txt'):
            create_tuples_from_file(file)
    return len(tuples)


def test_insert_date():
    tuples_count = create_tuples()
    rows_count = insert_data()
    assert tuples_count == rows_count
    print
    print ('Total rows inserted = ' + str(len(tuples)))
