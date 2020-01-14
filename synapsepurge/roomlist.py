""" Retrieve the list of rooms"""

import psycopg2

from synapsepurge import config


def get_rooms(config: config.Config):
    db_values = config._values[config._postgresql_section]
    my_connection = psycopg2.connect(user=db_values[config._postgresql_username],
                                     dbname=db_values[config._postgresql_database],
                                     password=db_values[config._postgresql_password],
                                     host=db_values[config._postgresql_host],
                                     port=db_values[config._postgresql_port])

    my_cursor = my_connection.cursor()

    my_cursor.execute("SELECT room_id from rooms")

    result = my_cursor.fetchall()
    my_cursor.close()
    my_connection.close()
    return result
