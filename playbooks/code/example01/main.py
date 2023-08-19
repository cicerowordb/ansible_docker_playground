""" TenisPolar is a cipher from Pedro Bandeira's books
    In the books, a club of teenagers use a substitution
    cipher replacing letters of `tenis` by letters of
    `polar` and vice-versa. This is not a serious cipher
    in computational meaning, but a good way to practice.
    This code uses Flask to offer to the clients an 
    endpoint to access the service.

    python3 -m pip install flask==2.2.2
    flask --debug --app playbooks/code/example01/main run --host 0.0.0.0 --port 5000
    curl http://localhost:5000/cipher?text=My+text+to+cipher
    curl http://localhost:5000/cipher?text=My+poxp+po+caphor
"""

from flask import Flask
from flask import request

app = Flask(__name__)

FIRST_WORD = 'tenisTENIS'
SECOND_WORD = 'polarPOLAR'

@app.route('/')
def hello():
    """ default route with basic usage """
    return '/cipher?text=example+of+text+to+cipher', 200

@app.route('/cipher')
def cipher(text=None):
    """ function to cipher text """
    if 'text' in request.args:
        text = request.args.get('text')
        for letter in FIRST_WORD:
            text = text.replace(letter, f'=__{letter}__=')
        for index, letter in enumerate(SECOND_WORD):
            text = text.replace(SECOND_WORD[index], FIRST_WORD[index])
        for index, letter in enumerate(FIRST_WORD):
            text = text.replace(f'=__{letter}__=', SECOND_WORD[index])
        return text, 200
    return 'no text received', 400
