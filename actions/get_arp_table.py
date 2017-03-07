from lib.action import NapalmBaseAction


class NapalmGetARPTable(NapalmBaseAction):
    """Get ARP Table from a network device via NAPALM
    """

    def run(self, htmlout=False, **std_kwargs):

        try:

            with self.get_driver(**std_kwargs) as device:
                result = {'raw': device.get_arp_table()}
                if htmlout:
                    result['html'] = self.html_out(result['raw'])

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, result)
