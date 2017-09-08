from lib.action import NapalmBaseAction


class NapalmGetNetworkInstances(NapalmBaseAction):
    """Get VRF/Routing instances from a network device via NAPALM
    """

    def run(self, name, **std_kwargs):

        with self.get_driver(**std_kwargs) as device:

            if not name:
                network_instances = {'raw': device.get_network_instances()}
            else:
                network_instances = {'raw': device.get_network_instances(name)}

            if self.htmlout:
                network_instances['html'] = self.html_out(network_instances['raw'])

        return (True, network_instances)
