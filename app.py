from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy import Column, String
from sqlalchemy.types import Integer, BigInteger
import os

MYSQLPASSWORD = os.environ.get("mysql_password")
MYSQLUSER = os.environ.get("mysql_user")
MYSQLHOST = os.environ.get("mysql_host")
MYSQLPORT = os.environ.get("mysql_port")
APIPORT = os.environ.get("api_port")

app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://"
    f"{MYSQLUSER}:{MYSQLPASSWORD}@{MYSQLHOST}:{MYSQLPORT}/test"
)
engine = SQLAlchemy(app) 
migrate = Migrate(app, engine) 

manager = Manager(app)
manager.add_command("engine", MigrateCommand)


def clean_variable(variable_to_clean):

    print(vars(variable_to_clean))
    variableid = (vars(variable_to_clean))
    del variableid['_sa_instance_state']
    return variableid


def dic_json_serializable(json_serializable_dic):

    dataphonerecords = []

    if isinstance(json_serializable_dic, list):

        for variable_to_clean in json_serializable_dic:
            dataphonerecords.append(clean_variable(variable_to_clean))

    else:
        print(vars(json_serializable_dic))
        clean_results = (clean_variable(json_serializable_dic))
        dataphonerecords = clean_results

    return dataphonerecords


class User(engine.Model):
    __tablename__ = "users"

    user_id = Column(Integer(), autoincrement=True, primary_key=True)
    name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    full_name = Column(String(50), nullable=False)
    phone_number = Column(BigInteger(), nullable=True)
    company_name = Column(String(50), nullable=False)
    company_deparment = Column(String(50), nullable=False)


phone_records_post_parser = reqparse.RequestParser()
phone_records_post_parser.add_argument(
    'name', type=str, required=True, help="Name cannot be blank!")
phone_records_post_parser.add_argument(
    'last_name', type=str, required=True, help="Last name cannot be blank!")
phone_records_post_parser.add_argument(
    'phone_number', type=int, required=True, help="Phone number is requierd!")
phone_records_post_parser.add_argument(
    'company_name', type=str, required=True,
    help="Please especify Company name !")


class PartialPhoneRecord(Resource):

    def get(self, search_value):

        search = "%{}%".format(search_value)
        datalike = User.query.filter(User.full_name.like(search)).all()
        if not datalike:
            datalike = User.query.filter(User.phone_number.like(search)).all()
        if not datalike:
            datalike = User.query.filter(User.company_name.like(search)).all()
        return dic_json_serializable(datalike)


def delete_record_by_id(element_id):

    User.query.filter(User.user_id == element_id).delete()
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
    engine.session.commit()
    engine.session.refresh(new_phone_record)
    print(new_phone_record.name)
    return dic_json_serializable(new_phone_record)


class PhoneRecords(Resource):

    def get(self):

        results = engine.session.query(User).all()
        return dic_json_serializable(results)

    def post(self):
        return create_new_record()


class PhoneRecord(Resource):

    def put(self, element_id):
        args = phone_records_post_parser.parse_args()
        user = User.query.filter(User.user_id == element_id).first()

        user.name = args['name']
        user.last_name = args['last_name']
        user.phone_number = args['phone_number']
        user.company_name = args['company_name']
        engine.session.commit()

        return args

    def delete(self, element_id):
        return delete_record_by_id(element_id)


api.add_resource(PhoneRecords, '/phonerecords')
api.add_resource(PhoneRecord, '/phonerecord/<string:element_id>')
api.add_resource(
    PartialPhoneRecord, '/partialphonerecord/<string:search_value>')


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=APIPORT)
    manager.run()
