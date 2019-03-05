
import logging
import json
from flask import Flask, jsonify, request, Response, render_template
from BookModel import Book
from settings import *

# app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_SORT_KEYS'] = False

oldIsbn = ""

def validBookObject(bookObject):
    if ("isbn" in bookObject and "title" in bookObject and "author" in bookObject and "quote" in bookObject):
        return True
    else:
        return False

# GET the list of books
# https://restapibooks.appspot.com/books
@app.route('/books')
def books_list():
    return jsonify({'books': Book.get_all_books()})

# GET one book with isbn
# https://restapibooks.appspot.com/books/9780816612833
@app.route('/books/<isbn>')
def get_book_by_isbn(isbn):
    return_value = Book.get_book(isbn)
    return jsonify(return_value)

# POST 1/2: form to create a new book -> redirects to add_book() link
# https://restapibooks.appspot.com/books/insertbook
@app.route('/insertbook')
def insert_book():
    return render_template('insert.html')

# POST 2/2: processes the data in form and inserts the new book
# https://restapibooks.appspot.com/books/newbook
@app.route('/newbook', methods=['POST'])
def add_book():
    new_book = {
        "isbn": request.form['isbn'],
        "title": request.form['title'],
        "author": request.form['author'],
        "quote": request.form['quote']
    }
    if (validBookObject(new_book)):
        # books.insert(0, new_book)
        Book.add_book(
            new_book['title'], new_book['author'], new_book['isbn'], new_book['quote']
        )
        # Response constructor
        bookInsertedMsg = "New book successfully inserted as follow: {0}".format(new_book)
        response = Response(json.dumps(bookInsertedMsg), status=200, mimetype='application/json')
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object",
            "help": "{'isbn': 1, title': '2', 'author': '3', 'quote': '4'}"
        }
        response = Response(invalidBookObjectErrorMsg,
                            status=400, mimetype='application/json')
        return response

# PUT (fake) 1/2: form to modify a book in the collection
# http://127.0.0.1:5000/changebook/9780816612833
# https://restapibooks.appspot.com/changebook/9780816612833
@app.route('/changebook/<isbn>')
def change_book(isbn):
    old_book = Book.query.filter_by(isbn=isbn).first()
    global oldIsbn
    oldIsbn = old_book.isbn
    return render_template(
        'change.html',
        isbn=oldIsbn,
        title=old_book.title,
        author=old_book.author,
        quote=old_book.quote
    )

# https://restapibooks.appspot.com/replacebook
# http://127.0.0.1:5000/replacebook
@app.route('/replacebook', methods=['POST'])
def replace_book():
    changed_book = {
        "isbn": request.form['isbn'],
        "title": request.form['title'],
        "author": request.form['author'],
        "quote": request.form['quote']
    }
    if(not validBookObject(changed_book)):
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object",
            "help": "{'title': '1', 'author': '2', 'quote': '3'}"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response

    Book.replace_book(oldIsbn, changed_book["isbn"], changed_book["title"], changed_book["author"], changed_book["quote"])
    response = Response("Book changed!", status=204)
    replacementCompletedMsg = {
        'success':'Book replaced successfully:{0}'.format(changed_book)
    }
    response = Response(json.dumps(replacementCompletedMsg), status=200, mimetype='application/json')
    return response

# Delete a book from collection
@app.route('/delete/<isbn>')
def delete_book(isbn):
    if(Book.delete_book(isbn)):
        deletionCompletedMsg = {
            'success':'Book with ISBN {0} was deleted from collection.'.format(isbn)
        }
        response = Response(json.dumps(deletionCompletedMsg), status=200, mimetype='application/json')
        return response
    invalidBookObjectErrorMsg = {
        'error': 'Book with this ISBN was not found.'
    }
    response = Response(json.dumps(invalidBookObjectErrorMsg), status=404, mimetype='application/json')
    return response

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

# for testing the app in localhost
app.run(port=5000)