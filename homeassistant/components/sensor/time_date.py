"""
homeassistant.components.sensor.time_date
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Date and Time service.

Configuration:

To use the Date and Time sensor you will need to add something like the
following to your config/configuration.yaml

sensor:
  platform: time_date
  monitored_variables:
    - type: 'time'
    - type: 'date'
    - type: 'date_time'
    - type: 'time_date'

VARIABLES:

monitored_variables
*Required
An array specifying the variables to monitor.

These are the variables for the monitored_variables array:

type
*Required
The variable you wish to display, see the configuration example above for a
list of all available variables


"""
import logging

import homeassistant.util.dt as dt_util
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)
SENSOR_TYPES = {
    'time': 'Time',
    'date': 'Date',
    'date_time': 'Date & Time',
    'time_date': 'Time & Date'
}


def setup_platform(hass, config, add_devices, discovery_info=None):
    """ Get the Time and Date sensor. """

    if hass.config.time_zone is None:
        _LOGGER.error("Timezone is not set in Home Assistant config")
        return False

    dev = []
    for variable in config['monitored_variables']:
        if variable['type'] not in SENSOR_TYPES:
            _LOGGER.error('Sensor type: "%s" does not exist', variable['type'])
        else:
            dev.append(TimeDateSensor(variable['type']))

    add_devices(dev)


# pylint: disable=too-few-public-methods
class TimeDateSensor(Entity):
    """ Implements a Time and Date sensor. """

    def __init__(self, sensor_type):
        self._name = SENSOR_TYPES[sensor_type]
        self.type = sensor_type
        self._state = None
        self.update()

    @property
    def name(self):
        """ Returns the name of the device. """
        return self._name

    @property
    def state(self):
        """ Returns the state of the device. """
        return self._state

    def update(self):
        """ Gets the latest data and updates the states. """

        time_date = dt_util.now()
        time = dt_util.datetime_to_short_time_str(time_date)
        date = dt_util.datetime_to_short_date_str(time_date)

        if self.type == 'time':
            self._state = time
        elif self.type == 'date':
            self._state = date
        elif self.type == 'date_time':
            self._state = date + ', ' + time
        elif self.type == 'time_date':
            self._state = time + ', ' + date