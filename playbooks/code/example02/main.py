""" Module to update information in Redis server
    python3 -m pip install redis==4.6 flask==2.3 -t .
    python3 -m flask --no-debug --app main run --host 0.0.0.0 --port 5001 &
"""

import os
from datetime import datetime
import redis
from flask import Flask
from flask import request

REDIS_HOST = os.getenv('REDIS_HOST', '172.18.1.2')
REDIS_PASS = os.getenv('REDIS_PASS', 'OQBMK/5fkc3pHAJ+qkexIN1D')
REDIS_PORT = 6379

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASS,
    decode_responses=True
)

app = Flask(__name__)

def insert_new_book(name=None, author=None, borrowed_to=None, borrowed_on=None):
    """ Insert a new book in Redis server """
    book = {
        "name": name,
        "author": author,
        "borrowed_to": borrowed_to,
        "borrowed_on": borrowed_on
    }
    last_key = redis_client.incr('last_key', amount=1)
    redis_client.hset('BOOK'+str(last_key), mapping=book)


@app.route('/')
def hello():
    """ Default route with basic usage """
    default_message = [
        "<h1>Borrowed Books</h1>",
        "Usage: <br>",
        "/list - list all borrowed books <br>",
        "/add?name=Book+Name&author=Author+Name&borrowed_to=Friend+Name"
        "      - add a new book to the list <br>",
        "/del?code=BOOK# - delete a book from the list <br>",
        ""
    ]
    return '\n'.join(default_message), 200

@app.route('/list')
def list_books():
    """ List all books in Redis server with a 200 response or
        list a message of not found in ith 204 response.
    """
    scan_response = redis_client.scan(match='BOOK*')
    print('========================================')
    print(scan_response)
    print(redis_client.hgetall('BOOK2'))
    print('========================================')
    response_status = 0
    response_content = ''
    if scan_response[1] == []:
        response_status = 404
        response_content = 'No books found\n'
    else:
        for book in scan_response[1]:
            print(f'code: {book}')
            response_content += f'<h1>code: {book} </h1>\n'
            for key in ['name', 'author', 'borrowed_to', 'borrowed_on']:
                hget_response = redis_client.hget(book, key)
                print(f'{key}: {hget_response}')
                response_content += f'<b>{key}</b>: {hget_response} <br>\n'
            print('-----------------------')
            response_content += '<hr>\n'
        response_status = 200
    return response_content, response_status

@app.route('/add')
def add():
    """" Add a new book using insert_new_book function """
    response_status = 0
    response_content = ''
    if any(s in request.args for s in ('name', 'author', 'borrowed_to')):
        borrowed_on = datetime.now().strftime('%Y-%m-%d_%H-%M')
        print(borrowed_on)
        insert_new_book(
            name=request.args['name'],
            author=request.args['author'],
            borrowed_to=request.args['borrowed_to'],
            borrowed_on=borrowed_on
        )
        response_status = 200
        response_content = 'Inserted'
    else:
        response_status = 422
        response_content = 'Missing parameter'
    return response_content, response_status

@app.route('/del')
def delete(code=None):
    """  """
    response_status = 0
    response_content = ''
    if 'code' in request.args:
        code = request.args['code']
        found = False
        scan_response = redis_client.scan(match='BOOK*')
        for book in scan_response[1]:
            if code == book:
                found = True
                redis_client.delete(book)
                response_content += f'Deleted book <b>{book}</b>\n'
                response_status = 200
                print(f'Deleted book {book}')
        if not found:
            print(f'The book with code {code} was not found.')
            response_content += f'The book with code <b>{code}</b> was not found.\n'
            response_status = 404
    else:
        response_status = 422
        response_content = 'Missing parameter'
    return response_content, response_status
