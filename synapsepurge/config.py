""" Configparser """

import configparser
from pathlib import Path

_config_directories = (Path.home(), Path.cwd())
_CONFIG_FILENAME = "purge.conf"

SYNAPSE_SECTION = "synapse"
SYNAPSE_USERNAME = "username"
SYNAPSE_PASSWORD = "password"
SYNAPSE_URL = "url"
SYNAPSE_DEVICE_NAME = "device_name"
_SYNAPSE_DEVICE_NAME_DEFAULT = "python/synapse-purge"
_synapse_config_mandatory = (SYNAPSE_USERNAME, SYNAPSE_PASSWORD, SYNAPSE_URL)

POSTGRESQL_SECTION = "postgresql"
POSTGRESQL_USERNAME = "username"
POSTGRESQL_PASSWORD = "password"
POSTGRESQL_DATABASE = "database"
POSTGRESQL_HOST = "host"
POSTGRESQL_PORT = "port"
_POSTGRESQL_PORT_DEFAULT = 5432

_postgresql_config_mandatory = (POSTGRESQL_USERNAME, POSTGRESQL_PASSWORD, POSTGRESQL_DATABASE, POSTGRESQL_HOST)

PURGE_SECTION = "purge"
PURGE_KEEP_DAYS = "keep_days"
PURGE_KEEP_DAYS_DEFAULT = 120
PURGE_DELETE_LOCAL_EVENTS = "delete_local_events"
_PURGE_DELETE_LOCAL_EVENTS_DEFAULT = False
PURGE_MAX_JOBS = "max_jobs"
_PURGE_MAX_JOBS_DEFAULT = 5
PURGE_WAIT_SECONDS = "wait_seconds"
_PURGE_WAIT_SECONDS_DEFAULT = 1


class Config(object):

    def __init__(self):
        self._parser = None
        self._values = {}

    def _read_mandatory(self, section: str, settings: list) -> str:
        """

        :param section: The config's section
        :type section: str
        :param settings: the list of mandatory configuration items
        :type settings: list
        :return: an error string if something went wrong, if not, None
        :rtype: str
        """

        self._values[section] = {}

        try:
            for value in settings:
                self._values[section][value] = self._parser[section][value]
                if self._values[section][value] is None or len(self._values[section][value]) == 0:
                    return "Empty value for " + value
        except KeyError as key_error:
            return key_error.args[0] + " not set!"

        return None

    def read_config(self) -> str:
        """
        Parse a configfile

        :return: Error (if there's something wrong with the configfile or NONE if everything is OK)
        :rtype: str
        """

        # Find a configfile
        for path in _config_directories:
            configfile = (Path(path) / _CONFIG_FILENAME).resolve()
            if configfile.is_file():
                break
        else:
            configfile = None

        if not configfile:
            return "Unable to find a configfile"

        self._parser = configparser.ConfigParser()
        self._parser.read(configfile)

        # First the mandatory settings
        error = self._read_mandatory(SYNAPSE_SECTION, _synapse_config_mandatory)
        if error:
            return error

        error = self._read_mandatory(POSTGRESQL_SECTION, _postgresql_config_mandatory)
        if error:
            return error

        # Now the optional settings
        self._values[PURGE_SECTION] = {}

        # Do not bother with catching ValueError - this exception is rather self-explanatory

        self._values[SYNAPSE_SECTION][SYNAPSE_DEVICE_NAME] = self._parser.get(SYNAPSE_SECTION, SYNAPSE_DEVICE_NAME,
                                                                              fallback=_SYNAPSE_DEVICE_NAME_DEFAULT)

        self._values[POSTGRESQL_SECTION][POSTGRESQL_PORT] = int(
            self._parser.get(POSTGRESQL_SECTION, POSTGRESQL_PORT, fallback=_POSTGRESQL_PORT_DEFAULT))

        self._values[PURGE_SECTION][PURGE_KEEP_DAYS] = int(
            self._parser.get(PURGE_SECTION, PURGE_KEEP_DAYS, fallback=PURGE_KEEP_DAYS_DEFAULT))
        self._values[PURGE_SECTION][PURGE_DELETE_LOCAL_EVENTS] = bool(
            self._parser.get(PURGE_SECTION, PURGE_DELETE_LOCAL_EVENTS, fallback=_PURGE_DELETE_LOCAL_EVENTS_DEFAULT))
        self._values[PURGE_SECTION][PURGE_MAX_JOBS] = int(
            self._parser.get(PURGE_SECTION, PURGE_MAX_JOBS, fallback=_PURGE_MAX_JOBS_DEFAULT))
        self._values[PURGE_SECTION][PURGE_WAIT_SECONDS] = int(
            self._parser.get(PURGE_SECTION, PURGE_WAIT_SECONDS, fallback=_PURGE_WAIT_SECONDS_DEFAULT))

        return None

    @property
    def values(self):
        return self._values
