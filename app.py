from flask import Flask
from flask_restful import Api
from alarm import AlarmApi, AlarmListApi, Clock

app = Flask(__name__)
api = Api(app)


api.add_resource(Clock, '/clock')
api.add_resource(AlarmListApi, '/alarms')
api.add_resource(AlarmApi, '/alarm/<int:alarm_id>')

if __name__ == '__main__':
    app.run(debug=True)
