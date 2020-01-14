""" Retrieve the list of rooms"""

import psycopg2

from synapsepurge import config


def get_rooms(config: config.Config):
    db_values = config._values[config._database_section]
    my_connection = psycopg2.connect(user=db_values[config._database_username], dbname=db_values[config._database_host],
                                     password=db_values[config._database_password],
                                     port=db_values[config._database_port])

    my_cursor = my_connection.cursor()

    my_cursor.execute("SEKECT room_id from rooms")

    result = my_cursor.fetchall()
    my_cursor.close()
    my_connection.close()
    return result
