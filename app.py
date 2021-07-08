from os import name
from typing import List

from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Column, String
from sqlalchemy.sql.functions import user
from sqlalchemy.types import Integer, BigInteger

app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Ivanka0818@localhost:3306/test"
engine = SQLAlchemy(app)


class User(engine.Model):
    __tablename__ = "users"

    user_id = Column(Integer(), primary_key =True)
    name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    full_name = Column(String(50), nullable=False)
    phone_number = Column(BigInteger(),primary_key=True)
    company_name = Column(String(50), nullable=False)
    
phone_records_post_parser = reqparse.RequestParser()
phone_records_post_parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
phone_records_post_parser.add_argument('last_name', type=str, required=True, help="Last name cannot be blank!")
phone_records_post_parser.add_argument('phone_number', type=int, required=True, help="Phone number is requierd!")
phone_records_post_parser.add_argument('company_name', type=str, required=True, help="Please especify Company name !")

 
class PartialPhoneRecord(Resource):

    def get(self, search_value):
        
        search = "%{}%".format(search_value)
        datalike = User.query.filter(User.full_name.like(search)).all()
        if not datalike: 
            datalike = User.query.filter(User.phone_number.like(search)).all()
        if not datalike: 
            datalike = User.query.filter(User.company_name.like(search)).all()
        dataphonerecords = []
        
        for idinformation in datalike:
            print(vars(idinformation))
            phoneidinformation = (vars(idinformation))
            del phoneidinformation['_sa_instance_state']
            dataphonerecords.append(phoneidinformation)
        return dataphonerecords


def delete_record_by_id(element_id):

    User.query.filter(User.user_id==element_id).delete()
    engine.session.commit()
    return {'deleted': 'ok'}


def create_new_record():
    args = phone_records_post_parser.parse_args()
    
    args['full_name'] = f"{args['name']} {args['last_name']}"
    new_phone_record = User(
        name=args["name"],
        last_name=args["last_name"],
        full_name=args["full_name"],
        phone_number=args["phone_number"], 
        company_name=args["company_name"]
    )

    # TODO: Save records
    engine.session.add(new_phone_record)
    return engine.session.commit()


class PhoneRecords(Resource):

    def get(self):

        dataphonerecords = []
        
        results = engine.session.query(User).all()
        for idinformation in results:
            print(vars(idinformation))
            phoneidinformation = (vars(idinformation))
            del phoneidinformation['_sa_instance_state']
            dataphonerecords.append(phoneidinformation)
        return dataphonerecords
        

    def post(self):
        return create_new_record()

class PhoneRecord(Resource):
    
    def put(self, element_id):
        # TODO: Modify by id
        args = phone_records_post_parser.parse_args() # Informacion nueva
        user = User.query.filter(User.user_id==element_id).first()
        # Registro de la tabla
        user.name = args['name']
        user.last_name = args['last_name']
        user.phone_number = args['phone_number']
        user.company_name = args['company_name']
        engine.session.commit()
    
        return

    def delete(self, element_id):
        return delete_record_by_id(element_id)


api.add_resource(PhoneRecords, '/phonerecords')
api.add_resource(PhoneRecord, '/phonerecord/<string:element_id>')
api.add_resource(PartialPhoneRecord, '/partialphonerecord/<string:search_value>')

if __name__ == '__main__':
    app.debug = True
    app.run(host = "0.0.0.0", port = 8080)
   