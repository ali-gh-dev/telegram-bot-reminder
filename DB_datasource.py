import psycopg2
import logging
from reminder_data import Reminder

# logging
logger = logging.getLogger()

SELECT_ALL_REMINDERS_QUERY = """SELECT * FROM reminders """

INSERT_REMINDER_QUERY = """INSERT INTO reminders(chat_id, reminder_message, reminder_time, creation_datetime)
                           VALUES(%s, %s, %s, %s)
                           RETURNING reminder_id, chat_id, reminder_message, reminder_time, fired, creation_datetime"""

FIRE_REMINDER_QUERY = """UPDATE reminders
                         SET fired = true
                         WHERE reminder_id = %s"""

CREATE_TABLE_QUERY = """
                CREATE TABLE IF NOT EXISTS reminders (
                    reminder_id serial PRIMARY KEY,
                    chat_id bigint NOT NULL,
                    reminder_message VARCHAR(300) NOT NULL,
                    reminder_time TIMESTAMP NOT NULL,
                    fired BOOLEAN NOT NULL DEFAULT FALSE,
                    creation_datetime TIMESTAMP NOT NULL
                )
            """


class DataSource:
    def __init__(self, database_url):
        self.database_url = database_url

    def get_connection(self):
        return psycopg2.connect(self.database_url, sslmode='allow')

    @staticmethod
    def close_connection(conn):
        if conn is not None:
            conn.close()

    def create_tables(self):
        commands = (
            CREATE_TABLE_QUERY,
        )

        conn = None
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            for command in commands:
                cur.execute(command)
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(error)
            raise error
        finally:
            self.close_connection(conn)

    def get_all_reminders(self):
        conn = None
        reminders = list()
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(SELECT_ALL_REMINDERS_QUERY)
            for row in cur.fetchall():
                reminders.append(Reminder(row))
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(error)
            raise error
        finally:
            self.close_connection(conn)
            return reminders

    def create_reminder(self, chat_id, reminder_message, reminder_time, creation_datetime):
        conn = None
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(INSERT_REMINDER_QUERY, (chat_id, reminder_message, reminder_time, creation_datetime))
            row = cur.fetchone()
            cur.close()
            conn.commit()
            return Reminder(row)
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(error)
            raise error
        finally:
            self.close_connection(conn)

    def fire_reminder(self, reminder_id):
        conn = None
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(FIRE_REMINDER_QUERY, (reminder_id,))
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(error)
            raise error
        finally:
            self.close_connection(conn)
