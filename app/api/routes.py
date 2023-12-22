from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, Book_schema, Books_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'naw'}

@api.route('/Books', methods = ['POST'])
@token_required
def create_Book(current_user_token):
    isbn = request.json['isbn']
    author = request.json['author']
    title = request.json['title']
    book_length = request.json['book_length']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    book = Book(isbn, author, title, book_length, user_token = user_token )
    db.session.add(book)
    db.session.commit()

    response = Book_schema.dump(book)
    return jsonify(response)

@api.route('/Books', methods = ['GET'])
@token_required
def get_Book(current_user_token):
    a_user = current_user_token.token
    Books = Book.query.filter_by(user_token = a_user).all()
    response = Books_schema.dump(Books)
    return jsonify(response)

@api.route('/Books/<id>', methods = ['GET'])
@token_required
def get_Book_two(current_user_token, id):
    fan = current_user_token.token
    if fan == current_user_token.token:
        book = Book.query.get(id)
        response = Book_schema.dump(book)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

# UPDATE endpoint
@api.route('/Book/<id>', methods = ['POST','PUT'])
@token_required
def update_Book(current_user_token,id):
    book = Book.query.get(id) 
    book.make = request.json['isbn']
    book.model = request.json['author']
    book.year = request.json['title']
    book.condition = request.json['book_length']
    book.user_token = current_user_token.token

    db.session.commit()
    response = Book_schema.dump(book)
    return jsonify(response)


# DELETE car ENDPOINT
@api.route('/Books/<id>', methods = ['DELETE'])
@token_required
def delete_Book(current_user_token, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = Book_schema.dump(book)
    return jsonify(response)