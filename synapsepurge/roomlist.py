""" Retrieve the list of rooms"""

import psycopg2

from synapsepurge import config


def get_rooms(the_config: config.Config):
    db_values = the_config.values[config.POSTGRESQL_SECTION]
    my_connection = psycopg2.connect(user=db_values[config.POSTGRESQL_USERNAME],
                                     dbname=db_values[config.POSTGRESQL_DATABASE],
                                     password=db_values[config.POSTGRESQL_PASSWORD],
                                     host=db_values[config.POSTGRESQL_HOST],
                                     port=db_values[config.POSTGRESQL_PORT])

    my_cursor = my_connection.cursor()

    my_cursor.execute("SELECT room_id from rooms")

    result = my_cursor.fetchall()
    my_cursor.close()
    my_connection.close()
    return result
