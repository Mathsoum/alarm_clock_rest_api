import time
import json
from flask_restful import reqparse, Resource

alarm_list = []


class Clock(Resource):
    def get(self):
        return {'clock': time.strftime("%H:%M")}


alarm_parser = reqparse.RequestParser()
alarm_parser.add_argument('time')
alarm_parser.add_argument('days')
alarm_parser.add_argument('active')


class AlarmApi(Resource):
    def get(self):
        return {'alarm_list': [alarm.json_dict() for alarm in alarm_list]}

    def post(self):
        args = alarm_parser.parse_args()
        new_alarm = Alarm(args['time'], args['days'], args['active'])
        alarm_list.append(new_alarm)
        return new_alarm.json_dict()


class Alarm:
    def __init__(self, _time=None, _days=None, _active=None):
        if alarm_list:
            self.id = max(alarm_list, key=lambda alarm: alarm.id).id + 1
        else:
            self.id = 0

        if _time is None:
            self.time = "00:00"
        else:
            self.time = _time

        self.days = {
            "Monday":    False,
            "Tuesday":   False,
            "Wednesday": False,
            "Thursday":  False,
            "Friday":    False,
            "Saturday":  False,
            "Sunday":    False,
        }

        if _days is not None:
            json_days = json.loads(_days)
            for key in json_days:
                if key in self.days:
                    self.days[key] = json_days[key]

        if _active is None:
            self.active = False
        else:
            self.active = bool(_active)

    def json_dict(self):
        return {
            'id':     self.id,
            'time':   self.time,
            'days':   self.days,
            'active': self.active
        }
