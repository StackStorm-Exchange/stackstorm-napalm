from lib.action import NapalmBaseAction


class NapalmGetNetworkInstances(NapalmBaseAction):
    """Get VRF/Routing instances from a network device via NAPALM
    """

    def run(self, name, htmlout=False, **std_kwargs):

        try:
            with self.get_driver(**std_kwargs) as device:

                if not name:
                    network_instances = {'raw': device.get_network_instances()}
                else:
                    network_instances = {'raw': device.get_network_instances(name)}

                if htmlout:
                    network_instances['html'] = self.html_out(network_instances['raw'])

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, network_instances)
