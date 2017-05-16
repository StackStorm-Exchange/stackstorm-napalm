from datetime import datetime

from napalm import get_network_driver

from st2reactor.sensor.base import PollingSensor

NEIGHBOR_INCREASE = 'napalm.NeighborIncrease'
NEIGHBOR_DECREASE = 'napalm.NeighborDecrease'


class NapalmLLDPSensor(PollingSensor):

    def __init__(self, sensor_service, config=None, poll_interval=5):
        super(NapalmLLDPSensor, self).__init__(sensor_service=sensor_service,
                                               config=config,
                                               poll_interval=poll_interval)
        self._logger = self.sensor_service.get_logger(
            name=self.__class__.__name__
        )

        # self._poll_interval = 30

    def setup(self):
        # Need to get initial BGP RIB, neighbor table, etc. Put into "self".
        # Then, write some logic within "poll" that checks again, and
        # detects diffs
        # Detects:
        # - Diffs in BGP RIB (need to give a threshold like 100s or 1000s or
        #   routes different)
        #   (may want to not only store the previous result, but also the
        #    previous 10 or so and do a stddev calc)

        # Stores number of BGP neighbors
        # self.bgp_neighbors = 0

        # Stores RIB information in-between calls
        # self.bgp_rib = {}

        # Dictionary for tracking per-device known state
        # Top-level keys are the management IPs sent to NAPALM, and
        # information on each is contained below that
        self.device_state = {}

        napalm_config = self._config

        # Assign sane defaults for configuration
        # default_opts = {
        #     "opt1": "val1"
        # }
        # for opt_name, opt_val in default_opts.items():

        #     try:

        #         # key exists but is set to nothing
        #         if not napalm_config[opt_name]:
        #             napalm_config[opt_name] == default_opts

        #     except KeyError:

        #         # key doesn't exist
        #         napalm_config[opt_name] == default_opts

        # Assign options to instance
        self._devices = napalm_config['devices']

        # Generate dictionary of device objects per configuration
        # IP Address(key): Device Object(value)
        self.devices = {
            str(device['hostname']): get_network_driver(device['driver'])(
                hostname=str(device['hostname']),
                username="interop",
                password="netauto42",
                optional_args={
                    'port': "22"
                })
            for device in self._devices
        }

    def poll(self):

        for hostname, device_obj in self.devices.items():

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
                    "Peer count went UP to %s" % str(this_lldp_neighbors)
                )
                self._lldp_peer_trigger(NEIGHBOR_INCREASE, hostname,
                                       last_lldp_neighbors, this_lldp_neighbors)

            elif this_lldp_neighbors < last_lldp_neighbors:
                self._logger.info(
                    "LLDP neighbors went DOWN to %s" % str(this_lldp_neighbors)
                )

                self._lldp_peer_trigger(NEIGHBOR_DECREASE, hostname,
                                       last_lldp_neighbors, this_lldp_neighbors)

            elif this_lldp_neighbors == last_lldp_neighbors:
                self._logger.info(
                    "LLDP neighbors STAYED at %s" % str(this_lldp_neighbors)
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
        # trigger = 'napalm.BgpPeerDecrease'
        payload = {
            'device': hostname,
            'oldpeers': int(oldpeers),
            'newpeers': int(newpeers),
            'timestamp': str(datetime.now()),
        }
        self._logger.debug("DISPATCHING TRIGGER %s" % trigger)
        self._sensor_service.dispatch(trigger=trigger, payload=payload)
