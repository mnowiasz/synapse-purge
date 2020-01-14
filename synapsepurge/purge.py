""" The main file """

from synapsepurge import config
from synapsepurge import roomlist

def purge():
    my_config = config.Config()
    my_config.read_config()
    roomlist.get_rooms(my_config)
    print(roomlist)

if __name__ == '__main__':
    purge()
