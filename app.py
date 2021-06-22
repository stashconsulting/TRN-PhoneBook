from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# Name, LastName, Number, and Company.
data = [
    {'name': 'javier', 'lastname': 'ortiz', 'number': 8093013934, 'company': 'stash'},
]

class PhoneRecords(Resource):
    def get(self):
        return data

api.add_resource(PhoneRecords, '/phonerecords')

if __name__ == '__main__':
    app.run(debug=True)
