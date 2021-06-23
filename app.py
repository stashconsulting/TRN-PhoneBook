from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# Name, LastName, Number, and Company.
data = [
    {"id": 890, "name": "javier", "lastname": "ortiz", "number": 8093013934, "company": "stash"},
]

def delete_record_by_id(element_id):
    for index, record in enumerate(data):
            if element_id == record['id']:
                del data[index]
                break


def create_new_record(element_data):
    data.append(element_data)
    return element_data

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
        delete_record_by_id(element_id)


api.add_resource(PhoneRecords, '/phonerecords')
api.add_resource(PhoneRecord, '/phonerecord/<int:element_id>')

if __name__ == '__main__':
    app.run(debug=True)
