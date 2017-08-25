from datetime import datetime

from napalm import get_network_driver

from st2reactor.sensor.base import PollingSensor

NEIGHBOR_INCREASE = 'napalm.LLDPNeighborIncrease'
NEIGHBOR_DECREASE = 'napalm.LLDPNeighborDecrease'


class NapalmLLDPSensor(PollingSensor):

    def __init__(self, sensor_service, config=None, poll_interval=5):
        super(NapalmLLDPSensor, self).__init__(sensor_service=sensor_service,
                                               config=config,
                                               poll_interval=poll_interval)
        self._logger = self.sensor_service.get_logger(
            name=self.__class__.__name__
        )

    def setup(self):
        # Dictionary for tracking per-device known state
        # Top-level keys are the management IPs sent to NAPALM, and
        # information on each is contained below that
        self.device_state = {}

        # Generate dictionary of device objects per configuration
        # IP Address(key): Device Object(value)
        self.devices = self._get_devices()

    def _get_devices(self):
        """Generate a dictionary of devices

        This used to be a fancy dictionary comprehension, but the way that most
        NAPALM drivers handle optional_args, this was difficult to maintain.
        We're doing it this way now so that optional_args is only provided when
        we are explicitly setting "port". Otherwise, we don't want to pass in
        "optional_args", so NAPALM can use its default value for port.
        """

        devices = {}
        for device in self._config['devices']:
            port = self._get_port(device)
            if port:
                devices[device['hostname']] = get_network_driver(device['driver'])(
                    hostname=device['hostname'],
                    username=self._get_creds(device['hostname'])['username'],
                    password=self._get_creds(device['hostname'])['password'],
                    optional_args={
                        'port': self._get_port(device)
                    }
                )
            else:
                devices[device['hostname']] = get_network_driver(device['driver'])(
                    hostname=device['hostname'],
                    username=self._get_creds(device['hostname'])['username'],
                    password=self._get_creds(device['hostname'])['password']
                )
        return devices

    def _get_port(self, device):
        port = device.get('port')
        if port:
            return str(port)
        else:
            return None

    def _get_creds(self, hostname):
        for device in self._config['devices']:
            if device['hostname'] == hostname:
                return self._config['credentials'][device['credentials']]

    def poll(self):

        for hostname, device_obj in self.devices.items():

            # Skip if device not online
            try:
                device_obj.open()
            except Exception:
                # Currently, we just skip the device. if we can't reach it.
                # In the future it may be worth doing something with
                # the neighbor count after a few misses, as in this state,
                # the sensor will continue to report that a device has the
                # same number of neighbors even if the device is inaccessible
                self._logger.warn(
                    "Failed to open connection to %s. Skipping this device for now." % hostname
                )
                continue

            try:
                last_lldp_neighbors = self.device_state[hostname]["last_lldp_neighbors"]
            except KeyError:
                self.device_state[hostname] = {
                    "last_lldp_neighbors": self.get_number_of_neighbors(device_obj)
                }
                continue

            this_lldp_neighbors = self.get_number_of_neighbors(device_obj)

            if this_lldp_neighbors > last_lldp_neighbors:
                self._logger.info(
                    "Device %s peer count went UP to %s" % (hostname, str(this_lldp_neighbors))
                )
                self._lldp_peer_trigger(NEIGHBOR_INCREASE, hostname,
                                        last_lldp_neighbors, this_lldp_neighbors)

            elif this_lldp_neighbors < last_lldp_neighbors:
                self._logger.info(
                    "Device %s LLDP nbrs went DOWN to %s" % (hostname, str(this_lldp_neighbors))
                )

                self._lldp_peer_trigger(NEIGHBOR_DECREASE, hostname,
                                        last_lldp_neighbors, this_lldp_neighbors)

            else:
                self._logger.debug(
                    "Device %s LLDP nbrs STAYED at %s" % (hostname, str(this_lldp_neighbors))
                )

            # Save this state for the next poll
            self.device_state[hostname]["last_lldp_neighbors"] = this_lldp_neighbors

    def cleanup(self):
        # This is called when the st2 system goes down. You can perform
        # cleanup operations like closing the connections to external
        # system here.
        pass

    def add_trigger(self, trigger):
        # This method is called when trigger is created
        pass

    def update_trigger(self, trigger):
        # This method is called when trigger is updated
        pass

    def remove_trigger(self, trigger):
        # This method is called when trigger is deleted
        pass

    def get_number_of_neighbors(self, device_obj):

        # Retrieve LLDP info
        try:
            with device_obj:
                neighbor_info = device_obj.get_lldp_neighbors()
        except Exception:  # TODO(mierdin): convert to ConnectionException
            raise

        this_lldp_neighbors = 0

        for interface, neighbors in neighbor_info.items():
            this_lldp_neighbors += len(neighbors)

        return this_lldp_neighbors

    def _lldp_peer_trigger(self, trigger, hostname, oldpeers, newpeers):
        payload = {
            'device': hostname,
            'oldpeers': int(oldpeers),
            'newpeers': int(newpeers),
            'timestamp': str(datetime.now()),
        }
        self._sensor_service.dispatch(trigger=trigger, payload=payload)
