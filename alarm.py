import time
import json
from flask_restful import reqparse, abort, Resource

alarm_list = []


class Clock(Resource):
    def get(self):
        return {'clock': time.strftime("%H:%M")}


alarm_parser = reqparse.RequestParser()
alarm_parser.add_argument('time')
alarm_parser.add_argument('days')
alarm_parser.add_argument('active')


class AlarmListApi(Resource):
    def get(self):
        return {'alarm_list': [alarm.json_dict() for alarm in alarm_list]}

    def post(self):
        args = alarm_parser.parse_args()
        new_alarm = Alarm(args['time'], args['days'], args['active'])
        alarm_list.append(new_alarm)
        return new_alarm.json_dict()


def abort_if_alarm_doesnt_exists(alarm_id):
    if alarm_id not in [alarm.id for alarm in alarm_list]:
        abort(404, message="Alarm {} does not exists".format(alarm_id))


def get_alarm_from_list(alarm_id):
    result = [alarm for alarm in alarm_list if alarm.id == alarm_id]
    if result:
        return result[0]
    else:
        return None


class AlarmApi(Resource):
    def get(self, alarm_id):
        abort_if_alarm_doesnt_exists(alarm_id)
        return [alarm for alarm in alarm_list if alarm.id == alarm_id][0].json_dict()

    def delete(self, alarm_id):
        global alarm_list
        abort_if_alarm_doesnt_exists(alarm_id)
        get_alarm_from_list(alarm_id).active = False  # Deactivates the alarm
        alarm_list = [alarm for alarm in alarm_list if alarm.id != alarm_id]
        return '', 204

    def put(self, alarm_id):
        # TODO Change 'time', 'days' or 'active' regarding what parameters were given
        pass


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
            self.__active = False
        else:
            self.__active = bool(_active)

    @property
    def active(self):
        return self.__active

    @active.setter
    def active(self, value):
        prev = self.__active
        self.__active = value

        if not prev and self.__active:  # Rising edge detection to avoid multiple cron interactions
            self.register_alarm()
        elif prev and not self.__active:  # Falling edge detection to avoid multiple cron interactions
            self.unregister_alarm()

    def register_alarm(self):
        # TODO Register alarm as a cron script
        pass

    def unregister_alarm(self):
        # TODO Unregister alarm as a cron script
        pass

    def json_dict(self):
        return {
            'id':     self.id,
            'time':   self.time,
            'days':   self.days,
            'active': self.__active
        }
