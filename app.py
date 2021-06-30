import uuid
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

data = { 
    str(uuid.uuid1()): 
    "name": "Javier",
    "last_name": "Ortiz",
    "full_name": "Javier Ortiz",
    "phone_number": 8093013934,
    "company_name": "Stash",
    } 
}

phone_records_post_parser = reqparse.RequestParser()
phone_records_post_parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
phone_records_post_parser.add_argument('last_name', type=str, required=True, help="Last name cannot be blank!")
phone_records_post_parser.add_argument('phone_number', type=int, required=True, help="Phone number is requierd!")
phone_records_post_parser.add_argument('company_name', type=str, required=True, help="Please especify Company name !")


class PartialPhoneRecord(Resource):

    def get(self, search_value):
        for dict_id in data:
            values = data[dict_id]
            if (
                search_value in values['full_name']
                or search_value in values['phone_number']
                or search_value in values['company_name']
            ):
                return values


def delete_record_by_id(element_id):
    for dict_id in data:
        if element_id == dict_id:
            del data[dict_id]
            break
    return {'deleted': 'ok'}

def create_new_record(args):
    args = phone_records_post_parser.parse_args()

    for dict_id in data:
        duplicated_information = data[dict_id]
        if (args['phone_number'] == duplicated_information['phone_number']):
            return {
                'error': f'duplicated number. it already exist under {duplicated_information["full_name"]}'
                }

    new_record_id = str(uuid.uuid1())
    args['full_name'] = f"{args['name']} {args['last_name']}"
    data[new_record_id] = args
    return data[new_record_id]

class PhoneRecords(Resource):

    def get(self):
        return data

    def post(self):
        request_body = request.get_json()
        return create_new_record(request_body)


class PhoneRecord(Resource):
    def get(self, element_id):
        for record in data:
            if element_id == record['id']:
                return data

    def put(self, element_id):
        delete_record_by_id(element_id)
        request_body = request.get_json()
        return create_new_record(request_body)

    def delete(self, element_id):
        return delete_record_by_id(element_id)


api.add_resource(PhoneRecords, '/phonerecords')
api.add_resource(PhoneRecord, '/phonerecord/<string:element_id>')
api.add_resource(PartialPhoneRecord, "/partialphonerecord")

if __name__ == '__main__':
    app.debug = True
    app.run(host = "0.0.0.0", port = 8080)
