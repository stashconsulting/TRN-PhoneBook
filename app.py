import uuid
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

data = { 
    str(uuid.uuid1()): {
    "name": "Javier",
    "last_name":"Ortiz",
    "phone_number": 8093013934,
    "company_name": "Stash"
    } 
}

class PartialPhoneRecord(Resource):

    def get(self, search_value):
        for dict_id in data:
            values = data[dict_id]
            if (
                search_value in values['name'] 
                or search_value in values['last_name']
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

def create_new_record(element_data):
    new_record_id = str(uuid.uuid1())
    data[new_record_id] = element_data
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
api.add_resource(PartialPhoneRecord, "/PartialPhoneRecord")

if __name__ == '__main__':
    app.run(debug=True)
