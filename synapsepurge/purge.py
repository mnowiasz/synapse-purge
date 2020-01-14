""" The main file """

from synapsepurge import config
from synapsepurge import roomlist

def purge():
    my_config = config.Config()
    error = my_config.read_config()
    if error:
        print(error)
        exit(1)

    rooms = roomlist.get_rooms(my_config)
    for room in rooms:
        print(room[0])

if __name__ == '__main__':
    purge()
