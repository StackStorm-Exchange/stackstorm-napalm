from lib.action import NapalmBaseAction


class NapalmGetLLDPNeighbours(NapalmBaseAction):
    """Get LLDP neighbours from a network device via NAPALM
    """

    def run(self, interface, **std_kwargs):

        try:
            with self.get_driver(**std_kwargs) as device:

                if not interface:
                    lldp_neighbours = {'raw': device.get_lldp_neighbors()}
                else:
                    lldp_neighbours = {'raw': device.get_lldp_neighbors_detail(interface)}

                if self.htmlout:
                    lldp_neighbours['html'] = self.html_out(lldp_neighbours['raw'])

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, lldp_neighbours)
