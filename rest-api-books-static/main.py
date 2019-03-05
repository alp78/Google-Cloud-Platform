import logging
import json
from flask import Flask, jsonify, request, Response, render_template

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_SORT_KEYS'] = False

books = [
    {
        'isbn': '9780816612833',
        'title': 'Visions of Excess',
        'author': 'Georges Bataille',
        'quote': 'The eye, at the summit of the skull, opening on the incandescent sun in order to contemplate it in a sinister solitude, is not a product of the understanding, but is instead an immediate existence.'
    },
    {
        'isbn': '9780520229235',
        'title': 'Duino Elegies',
        'author': 'Rainer Maria Rilke',
        'quote': 'Every angel is terrible.'
    }
]

oldIsbn = ""

def validBookObject(bookObject):
    if ("isbn" in bookObject and "title" in bookObject and "author" in bookObject and "quote" in bookObject):
        return True
    else:
        return False

'''
def valid_put_request_data(request_data):
    if ("title" in request_data and "author" in request_data and "quote" in request_data):
        return True
    else:
        return False
'''

# GET the list of books
# https://restapibooks.appspot.com/books


@app.route('/books')
def books_list():
    return jsonify({'books': books})

# GET one book with isbn
# https://restapibooks.appspot.com/books/9780816612833
@app.route('/books/<isbn>')
def get_book_by_isbn(isbn):
    return_value = {}
    for book in books:
        if book["isbn"] == isbn:
            return_value = {
                'isbn': book["isbn"],
                'author': book["author"],
                'title': book["title"],
                'quote': book["quote"]
                }
    return jsonify(return_value)


'''
# for testing POST in local with Postman
@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if(validBookObject(request_data)):
        books.insert(0, request_data)
        return "True"
    else:
        return "False"
'''

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
        books.insert(0, new_book)
        # Response constructor
        # response = Response("", 201, mimetype='application/json')
        # response.headers['Location'] = "/books/" + str(new_book['title'])
        return render_template(
            'inserted.html',
            isbn=new_book['isbn'],
            title=new_book['title'],
            author=new_book['author'],
            quote=new_book['quote']
        )
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
    old_book = {}

    for book in books:
        if book["isbn"] == isbn:
            global oldIsbn
            oldIsbn = isbn
            old_book = {
                'isbn': oldIsbn,
                'author': book["author"],
                'title': book["title"],
                'quote': book["quote"]
                }
    return render_template(
        'change.html',
        isbn=old_book['isbn'],
        title=old_book['title'],
        author=old_book['author'],
        quote=old_book['quote']
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
    # request_data = request.get_json()
    if(not validBookObject(changed_book)):
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object",
            "help": "{'title': '1', 'author': '2', 'quote': '3'}"            
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response
    
    for book in books:
        if oldIsbn == book["isbn"]:
            book["isbn"] = changed_book["isbn"]
            book["author"] = changed_book["author"]
            book["title"] = changed_book["title"]
            book["quote"] = changed_book["quote"]

    # response = Response("Book changed!", status=204)
    return render_template(
        'changed.html',
        isbn=changed_book['isbn'],
        title=changed_book['title'],
        author=changed_book['author'],
        quote=changed_book['quote']
    )

'''    
    new_book = {
        "isbn": isbn,
        "title": request_data['title'],
        "author": request_data['author'],
        "quote": request_data['quote']       
    }

    i = 0
    for book in books:
        currentIsbn = book["isbn"]
        if currentIsbn == isbn:
            books[i] = changed_book
        i += 1
    response = Response("", status=204)
    return response
'''
    # return jsonify(request.get_json())


# Delete a book from collection
@app.route('/delete/<isbn>')
def delete_book(isbn):
    i=0
    for book in books:
        if book["isbn"] == isbn:
            books.pop(i)
            deletionCompletedMsg = {
                'success':'Book with ISBN {0} was deleted from collection.'.format(isbn)
            }
            response = Response(json.dumps(deletionCompletedMsg), status=200, mimetype='application/json')
            return response
        i+=1
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
# app.run(port=5000)
