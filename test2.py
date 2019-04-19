from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api, reqparse
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from functools import wraps
import os
import uuid
import jwt
import datetime

app = Flask(__name__)
api = Api(app)


app.config['SECRET_KEY'] = 'ad8f2b9a-e3e3-11e8-b959-13d598a90366'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///candidate.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enrolement_no = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    address = db.Column(db.String(80))
    degree_name = db.Column(db.String(80))
    admission_status = db.Column(db.Boolean)


class crud_candidate(Resource):
    def post(self):
        '''create new candidate'''
        parser = reqparse.RequestParser()
        parser.add_argument('enrolement_no', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('address', required=True)
        parser.add_argument('degree_name', required=True)

        args = parser.parse_args()

        new_candidate = Candidate(enrolement_no=str(uuid.uuid4()), name=args['name'],
        address=args['address'], degree_name=args['degree_name'],
        admission_status=False)

        db.session.add(new_candidate)
        db.session.commit()

        return {'message':'New candidate created!'}

    def get(self):
        try:    
            parser = reqparse.RequestParser()
            parser.add_argument('enrolement_no')
            args = parser.parse_args() 
            candidate = Candidate.query.filter_by(enrolement_no=args['enrolement_no']).first()

            if not candidate:
                return {'message': 'No candidate found!'}

            candidate_data = {}
            candidate_data['enrolement_no'] = candidate.enrolement_no
            candidate_data['name'] = candidate.name
            candidate_data['address'] = candidate.address
            candidate_data['admission_status'] = candidate.admission_status
            candidate_data['degree_name'] = candidate.degree_name

            return {'candidate': candidate_data}
        except Exception as err:
            return {'Error': err}

    def put(self):
        '''To update the candidate'''
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('enrolement_no')
            args = parser.parse_args() 
            candidate = Candidate.query.filter_by(enrolement_no=args['enrolement_no']).first()

            if not candidate:
                return {'message': 'candidate not found'}

            parser.add_argument('name', required=True)
            parser.add_argument('address', required=True)
            parser.add_argument('admission_status')
            parser.add_argument('degree_name', required=True)

            args2 = parser.parse_args()

            candidate.name = args2['name']
            candidate.address = args2['address']
            candidate.admission_status = args2['admission_status']
            candidate.degree_name = args2['degree_name']
            db.session.commit()

            return {'message': 'The candidate has been updated!'}
        except Exception as err:
            return {'Error': err}

    def delete(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('enrolement_no')
            args = parser.parse_args() 
            candidate = Candidate.query.filter_by(enrolement_no=args['enrolement_no']).first()

            if not candidate:
                return {'message': 'No cadidate found!'}
            db.session.delete(candidate)
            db.session.commit()
            return {'message': 'The candidate has been deleted!'}
        except Exception as err:
            return {'Error': err}

class Candidate_list(Resource):
    def get(self):
        try:
            candidates = Candidate.query.all()
            #return "asd"
            if candidates:
                output = []
                for candidate in candidates:
                    candidate_data = {}
                    candidate_data['enrolement_no'] = candidate.enrolement_no
                    candidate_data['name'] = candidate.name
                    candidate_data['address'] = candidate.address
                    candidate_data['admission_status'] = candidate.admission_status
                    candidate_data['degree_name'] = candidate.degree_name
                    output.append(candidate_data)
                return {'candidates': output}
            else:
                return {'No candidate found'}
        except Exception as err:
            return {'Error': err}

api.add_resource(crud_candidate,'/candidate')
api.add_resource(Candidate_list, '/candidate_list')


if __name__ == '__main__':
    app.run(debug=True)
