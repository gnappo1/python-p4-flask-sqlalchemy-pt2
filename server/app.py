#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension

from models import db, Pet, Owner
import os
from dotenv import load_dotenv

load_dotenv()
# print(config['SECRET_KEY'])
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
toolbar = DebugToolbarExtension(app)

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def method_name():
    response = make_response(
        "<body><h1>Welcome to our Pets&Owners database!</h1></body>",
        200
    )
    return response

@app.route('/pets/<int:id>')
def find_pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()

    if pet:
        response_body = f'''
            <body><h1>Information for {pet.name}</h1>
            <h2>Pet Species is {pet.species}</h2>
            <h2>Pet Owner is {pet.owner.name}</h2></body>
        '''
        response = make_response(response_body, 200)
        return response
    
    response_body = f"<body><h1>Sorry but we could not find any pets with id #{id}</h1></body>"
    response = make_response(response_body, 404)
    return response

@app.route('/owners/<int:id>')
def find_owner_by_id(id):
    owner = Owner.query.filter(Owner.id == id).first()
    
    response_body= '<body>'
    
    if owner:
        response_body += f'''
            <h1>Information for {owner.name}</h1>
            <h3>Owner Id is {owner.id}</h3>
            <h3>Pets</h3>
            <ul>
        '''
        for pet in owner.pets:
            response_body += f'''
                <li>
                    <h3>Name: {pet.name}</h3>
                    <h4>Id: {pet.id}</h4>
                    <h4>Species: {pet.species}</h4>
                </li>
            '''
        response_body += f'''
            </ul></body>
        '''
        response = make_response(response_body, 200)
        return response
        
    response_body += f"<h1>Sorry but we could not find any owners with id #{id}</h1></body>"
    response = make_response(response_body, 404)
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
