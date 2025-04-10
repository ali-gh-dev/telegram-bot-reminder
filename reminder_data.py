import datetime


class Reminder:
    def __init__(self, row):
        self.reminder_id = row[0]
        self.chat_id = row[1]
        self.reminder_message = row[2]
        self.reminder_time = row[3]
        self.fired = row[4]
        # self.creation_datetime = datetime.datetime.today()

    def __repr__(self):
        return f"\n✍️  {self.reminder_message}\n\n⏰  {self.reminder_time.strftime('%d/%m/%Y %H:%M')}\n"

    def should_be_fired(self):
        return (self.fired is False) and (datetime.datetime.today() >= self.reminder_time)
