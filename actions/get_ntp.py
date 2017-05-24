from lib.action import NapalmBaseAction


class NapalmGetNTP(NapalmBaseAction):
    """Get NTP details from a network device via NAPALM
    """

    def run(self, query_type, **std_kwargs):

        try:

            query_type = query_type.lower()

            with self.get_driver(**std_kwargs) as device:

                if type == "stats":
                    ntp_result = {'raw': device.get_ntp_stats()}
                elif type == "servers":
                    ntp_result = {'raw': device.get_ntp_servers()}
                elif type == "peers":
                    ntp_result = {'raw': device.get_ntp_peers()}
                if self.htmlout:
                    ntp_result['html'] = self.html_out(ntp_result['raw'])

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, ntp_result)
