from flask import Flask
from flask_restful import Api
from alarm import AlarmApi, Clock

app = Flask(__name__)
api = Api(app)


api.add_resource(Clock, '/clock')
api.add_resource(AlarmApi, '/alarm')

if __name__ == '__main__':
    app.run(debug=True)
