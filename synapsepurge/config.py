""" Configparser """

import configparser
from pathlib import Path

_config_directories = (Path.home(), Path.cwd())
_config_filename = "purge.conf"


class Config(object):
    _synapse_section = "synapse"
    _synapse_username = "username"
    _synapse_password = "password"
    _synapse_url = "url"
    _synapse_config_mandatory = (_synapse_username, _synapse_password, _synapse_url)

    _postgresql_section = "postgresql"
    _postgresql_username = "username"
    _postgresql_password = "password"
    _postgresql_database = "database"
    _postgresql_host = "host"
    _postgresql_port = "port"
    _postgresql_port_default = 5432

    _postgresql_config_mandatory = (_postgresql_username, _postgresql_password, _postgresql_database, _postgresql_host)

    _purge_section = "purge"
    _purge_keep_days = "keep_days"
    _purge_keep_days_default = 120
    _purge_delete_local_events = "delete_local_events"
    _purge_delete_local_events_default = False
    _purge_max_jobs = "max_jobs"
    _purge_max_jobs_default = 5

    def __init__(self):
        self._parser = None
        self._values = {}
        self._defaults = {
            self._postgresql_section: {
                self._postgresql_port: 5432
            },
            self._purge_section: {
                self._purge_keep_days: 120,
                self._purge_delete_local_events: False,
                self._purge_max_jobs: 5
            }
        }

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
            configfile = (Path(path) / _config_filename).resolve()
            if configfile.is_file():
                break
        else:
            configfile = None

        if not configfile:
            return "Unable to find a configfile"

        self._parser = configparser.ConfigParser()
        self._parser.read(configfile)

        # First the mandatory settings
        error = self._read_mandatory(self._synapse_section, self._synapse_config_mandatory)
        if error:
            return error

        error = self._read_mandatory(self._postgresql_section, self._postgresql_config_mandatory)
        if error:
            return error

        # Now the optional settings
        self._values[self._purge_section] = {}

        # Do not bother with catching ValueError - this exception is rather self-explanatory

        self._values[self._postgresql_section][self._postgresql_port] = \
            int(self._parser.get(self._postgresql_section, self._postgresql_port, fallback=self._postgresql_port_default))
        self._values[self._purge_section][self._purge_keep_days] = \
            int(self._parser.get(self._purge_section, self._purge_keep_days, fallback=self._purge_keep_days_default))
        self._values[self._purge_section][self._purge_delete_local_events] = \
            bool(self._parser.get(self._purge_section, self._purge_delete_local_events,
                                  fallback=self._purge_delete_local_events_default))
        self._values[self._purge_section][self._purge_max_jobs] = \
            int(self._parser.get(self._purge_section, self._purge_max_jobs, fallback=self._purge_max_jobs_default))

        return None
