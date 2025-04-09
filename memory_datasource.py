from reminder_data import Reminder


class MemoryDataSource:
    def __init__(self):
        self.reminders = dict()

    def add_reminder(self, reminder_id, chat_id, message, time):
        reminder_obj = Reminder(chat_id, message, time)
        self.reminders[reminder_id] = reminder_obj
        return reminder_obj
