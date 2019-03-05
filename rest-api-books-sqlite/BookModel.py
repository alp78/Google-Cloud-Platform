from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from settings import app

db = SQLAlchemy(app)

class Book(db.Model):
    __tablename__='books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    author = db.Column(db.String(80))
    isbn = db.Column(db.String(80), nullable=False)
    quote = db.Column(db.String(80))

    # to return json format when querying
    def json(self):
        return {'title': self.title, 'author': self.author, 'isbn': self.isbn, 'quote': self.quote}

    def add_book(_title, _author, _isbn, _quote):
        new_book = Book(title=_title, author=_author, isbn=_isbn, quote=_quote)
        db.session.add(new_book)
        db.session.commit()

    def get_all_books():
        return [Book.json(book) for book in Book.query.all()]

    def get_book(_isbn):
        return Book.json(Book.query.filter_by(isbn=_isbn).first())

    def delete_book(_isbn):
        is_successful = Book.query.filter_by(isbn=_isbn).delete()
        db.session.commit()
        return bool(is_successful)

    def update_book_quote(_isbn, _quote):
        book_to_update = Book.query.filter_by(isbn=_isbn).first()
        book_to_update.quote = _quote
        db.session.commit()

    def replace_book(_oldIsbn, _isbn, _title, _author, _quote):
        book_to_replace = Book.query.filter_by(isbn=_oldIsbn).first()
        book_to_replace.isbn = _isbn
        book_to_replace.title = _title
        book_to_replace.author = _author
        book_to_replace.quote = _quote
        db.session.commit()

    # format of the query returns (from Terminal)
    def __repr__(self):
        book_object = {
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'quote': self.quote
        }
        return json.dumps(book_object)