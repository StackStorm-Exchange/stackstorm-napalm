from datetime import datetime

from napalm import get_network_driver

from st2reactor.sensor.base import PollingSensor

BGP_PEER_INCREASE = 'napalm.BgpPeerIncrease'
BGP_PEER_DECREASE = 'napalm.BgpPeerDecrease'


class NapalmBGPSensor(PollingSensor):

    def __init__(self, sensor_service, config=None, poll_interval=5):
        super(NapalmBGPSensor, self).__init__(sensor_service=sensor_service,
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
                username=device['username'],
                password=device['password'],
                optional_args={
                    'port': str(device['port'])
                })
            for device in self._devices
        }

    def poll(self):

        for hostname, device_obj in self.devices.items():

            try:
                last_bgp_peers = self.device_state[hostname]["last_bgp_peers"]
            except KeyError:

                # Get current BGP peers (instead of setting to 0 and
                # triggering every time sensor starts initially)
                try:
                    self.device_state[hostname] = {
                        "last_bgp_peers": self.get_number_of_peers(device_obj)
                    }
                    continue
                # Any connection-related exception raised here is
                # driver-specific, so we have to catch "Exception"
                except Exception as e:
                    self._logger.debug("Caught exception on connect: %s" % e)
                    continue

            try:
                this_bgp_peers = self.get_number_of_peers(device_obj)
            # Any connection-related exception raised here is
            # driver-specific, so we have to catch "Exception"
            except Exception as e:
                self._logger.debug("Caught exception on get peers: %s" % e)
                continue

            if this_bgp_peers > last_bgp_peers:
                self._logger.info(
                    "Peer count went UP to %s" % str(this_bgp_peers)
                )
                self._bgp_peer_trigger(BGP_PEER_INCREASE, hostname,
                                       last_bgp_peers, this_bgp_peers)

            elif this_bgp_peers < last_bgp_peers:
                self._logger.info(
                    "BGP neighbors went DOWN to %s" % str(this_bgp_peers)
                )

                self._bgp_peer_trigger(BGP_PEER_DECREASE, hostname,
                                       last_bgp_peers, this_bgp_peers)

            elif this_bgp_peers == last_bgp_peers:
                self._logger.info(
                    "BGP neighbors STAYED at %s" % str(this_bgp_peers)
                )

            # Save this state for the next poll
            self.device_state[hostname]["last_bgp_peers"] = this_bgp_peers

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

    def get_number_of_peers(self, device_obj):

        vrfs = {}

        # Retrieve full BGP peer info at the VRF level
        try:
            with device_obj:
                vrfs = device_obj.get_bgp_neighbors()
        except Exception:  # TODO(mierdin): convert to ConnectionException
            raise

        this_bgp_peers = 0

        for vrf_id, vrf_details in vrfs.items():

            for peer_id, peer_details in vrf_details['peers'].items():

                # TODO(mierdin): This isn't always the fastest method when
                # peers go down. Try to improve on this.
                if peer_details['is_up']:
                    this_bgp_peers += 1

        return this_bgp_peers

    def _bgp_peer_trigger(self, trigger, hostname, oldpeers, newpeers):
        trigger = 'napalm.BgpPeerDecrease'
        payload = {
            'device': hostname,
            'oldpeers': int(oldpeers),
            'newpeers': int(newpeers),
            'timestamp': str(datetime.now()),
        }
        self._logger.debug("DISPATCHING TRIGGER %s" % trigger)
        self._sensor_service.dispatch(trigger=trigger, payload=payload)
