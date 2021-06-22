from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# Name, LastName, Number, and Company.
data = [
    {"id": 890, "name": "javier", "lastname": "ortiz", "number": 8093013934, "company": "stash"},
]

class PhoneRecords(Resource):

    def get(self):
        return data

    def post(self):
        request_body = request.get_json()
        data.append(request_body)
        return request_body


class PhoneRecord(Resource):
    def get(self): ...

    def put(self): ...

    def delete(self, element_id):
        for index, record in enumerate(data):
            if element_id == record['id']:
                del data[index]
                break


api.add_resource(PhoneRecords, '/phonerecords')
api.add_resource(PhoneRecord, '/phonerecord/<int:element_id>')

if __name__ == '__main__':
    app.run(debug=True)
