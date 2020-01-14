""" The main file """

from synapsepurge import config


def main():
    my_config = config.Config()
    print(my_config.read_config())

    print(my_config._values[my_config._database_section][my_config._database_port])
    print(my_config._values)


if __name__ == '__main__':
    main()
