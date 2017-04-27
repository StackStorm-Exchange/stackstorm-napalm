from lib.action import NapalmBaseAction


class NapalmGetLLDPNeighbors(NapalmBaseAction):
    """Get LLDP neighbors from a network device via NAPALM
    """

    def run(self, interface, **std_kwargs):

        try:
            with self.get_driver(**std_kwargs) as device:

                if not interface:
                    lldp_neighbors = {'raw': device.get_lldp_neighbors()}
                else:
                    lldp_neighbors = {'raw': device.get_lldp_neighbors_detail(interface)}

                if self.htmlout:
                    lldp_neighbors['html'] = self.html_out(lldp_neighbors['raw'])

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, lldp_neighbors)
