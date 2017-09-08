from lib.action import NapalmBaseAction


class NapalmGetBGPNeighborDetail(NapalmBaseAction):

    def run(self, neighbor, **std_kwargs):

        with self.get_driver(**std_kwargs) as device:
            result = {'raw': device.get_bgp_neighbors_detail(neighbor)}

            if self.htmlout:
                result['html'] = self.html_out(result['raw'])

        return (True, result)
