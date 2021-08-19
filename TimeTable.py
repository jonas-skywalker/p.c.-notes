import datetime


TIMETABLE = {
    0: {range(20 * 60 + 0, 21 * 60 + 20): "Experimentalphysik1"},
    1: {},
    2: {},
    3: {},
    4: {},
    5: {},
    6: {}
}


class TimeTable:
    def __init__(self):
        self.timetable = TIMETABLE

    def get_course(self):
        now = datetime.datetime.now()
        minute = now.hour * 60 + now.minute
        for key, val in self.timetable[now.weekday()].items():
            if minute in key:
                return val
            else:
                return ""
