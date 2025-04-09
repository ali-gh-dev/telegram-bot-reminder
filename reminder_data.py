import datetime


class Reminder:
    def __init__(self, chat_id, message, time):
        self.chat_id = chat_id
        self.message = message
        self.time = datetime.datetime.strptime(time, "%d/%m/%Y %H:%M")
        self.creation_datetime = datetime.datetime.today()
        self.fired = False

    def __repr__(self):
        return f"\n✍️  {self.message}\n\n⏰  {self.time.strftime('%d/%m/%Y %H:%M')}\n"

    def fire(self):
        self.fired = True

    def should_be_fired(self):
        return (self.fired is False) and (datetime.datetime.today() >= self.time)

# example
# reminder_1 = Reminder("going to work", "13/10/2025 07:30")
# reminder_2 = Reminder("sending email to Hamed", "14/10/2025 16:00")
