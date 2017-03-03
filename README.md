# NAPALM

[NAPALM](https://github.com/napalm-automation) is a Python library to simplify
and abstract some of the programmatic communication with network devices,
making multi-vendor network automation a little easier. This pack introduces
new capabilities that allow a StackStorm user to leverage NAPALM within
StackStorm in the form of sensors, actions, and more.

This pack leverages the NAPALM library to allow ST2 to perform multivendor
network automation

**This pack is actively being developed and should be considered BETA status for
the time being. Please open a github issue or pull request if you run into any
problems with this pack**

## Requirements

All Python dependencies are included in requirements.txt. This is primarily
comprised of the various Python libraries that make up the NAPALM project.

## Configuration

Look at config.schema.yaml. The napalm.yaml.example file as a base to start
the configuration which needs to be copied into your stackstorm configs
directory (/opt/stackstorm/configs/ by default on debian/ubuntu) as napalm.yaml.
This is where you'll need to tell StackStorm about the network devices
you wish use and the credentails for logging into the devices.

### Credentials configuration

Multiple credentials are supported as different hosts or groups of hosts might
have different logins. The credentials groups are not validated by the schema.

The following format is used to specify the credentials group. In the example
two groups are created *core* and *customer*. Each group has a username and
password.

When running actions on devices you can pass the name of the credentials group
defined here in the credentials parameter or leave it blank and it will be
picked up in the devices configuration (provided you configured the device).

```YAML
credentials:
  core:
    username: myuser
    password: mypassword
  customer:
    username: customeruser
    password: customerpw
```

### Devices configuration

The devices configuration is so that credentials and drivers for each device
don't have to be entered manually. This is useful for automated action chains
or mistral workflows where (most of the time) only the hostname is known
(for example from a syslog logsource field.)

```YAML
devices:
- hostname: router1.lon
  driver: junos
  credentials: core
- hostname: router2.par
  driver: junos
  credentials: customer
```

## Actions

Actions in the NAPALM pack largely mirror the NAPALM library methods documented
[here](https://napalm.readthedocs.io/en/latest/base.html).

- **cli**: Run a CLI command on a devices.
- **get_arp_table**:  Get the APR table from a device.
- **get_bgp_config**: Get BGP configuration from a device.
- **get_bgp_neighbors**: Get the BGP Neighbours from a device.
- **get_bgp_neighbors_detail**: Get a detailed BGP neighbour from a device.
- **get_config**: Get configuration from the device.
- **get_environment**: Get the environment sensor output from a device.
- **get_facts**: Get the various facts (Version, Serial Number, Vendor, Model, etc.) from a device.
- **get_firewall_policies**: Get firewall policies from a device.
- **get_interfaces**: Get interfaces from a device.
- **get_lldp_neighbors**: Get the LLDP Neighbours from a device.
- **get_log**: Get logs from devices.
- **get_mac_address_table**: Get the MAC Address table from a device.
- **get_network_instances**: Get details of network/routing instances/vrfs from a device.
- **get_ntp**: Gets NTP information from a network device.
- **get_optics**: Fetches the power usage on the various transceivers installed on the device (in dbm).
- **get_probes_config**: Get RPM (JunOS) or IP SLA (IOS-XR) probe configuration from a device.
- **get_probes_results**: Get RPM (JunOS) or IP SLA (IOS-XR) probe results from a device.
- **get_route_to**: Shows an IP route on a device.
- **get_snmp_information**: Get the SNMP information from a device using NAPALM.
- **loadconfig**: Loads (merge) a configuration to a device.
- **traceroute**: Run a traceroute from a device.

## Rules and Triggers

The pack defines rules for handing syslog events or monitoring events. Logstash
is a good source for handling syslog events and extracting the required
parameters. There is an example logstash and rsyslog configuration in the examples
directory.

It's important to note that the rules and triggers here rely on the host field
being set to the IP address of the host and the logsoure being set to the hostname
received from the box. The example rsyslog configuration example details more
on this.

- **configuration_change_workflow**: Webhook trigger to run a remote backup mistral workflow when a configuration change is detected on a device.
- **interface_down_chain**: Webhook trigger to run an action chain when an interface goes down.
- **bgp_prefix_exceeded_chain**: Webhook trigger to run an action chain when a bgp neighbour exceeds its prefix limit.

## Datastore

Action chains in this pack require certain datastore values to be set.

Common datastore key value pairs for all the action chains and workflows.

```sh
# Where to send notifications when an action chain fails.
st2 key set napalm_actionerror_mailto "stackstorm_errors@example.com"

# What email should be the sender of failure notifications
st2 key set napalm_actionerror_mailfrom "stackstorm@example.com"

# HTML header and footer files which get read in by some of the workflows to send nice emails.
st2 key set napalm_html_mail_header_file "/opt/stackstorm/packs/napalm/examples/html_header.html"
st2 key set napalm_html_mail_footer_file "/opt/stackstorm/packs/napalm/examples/html_footer.html"
```

For the remote backup action chain the following commands will create the datastore key value pairs needed.

```sh
# Command to run on the remote server to backup the device
st2 key set napalm_remotebackup_cmd "backup_cmd"

# Username used to connect to the remote server
st2 key set napalm_remotebackup_user "username"

# Hostname of the remote server.
st2 key set napalm_remotebackup_host "backup hostname"

# Where to send notifications of a successful backup.
st2 key set napalm_remotebackup_mailto "backupnotify@example.com"

# What email should be the sender of notifications
st2 key set napalm_remotebackup_mailfrom "stackstorm@example.com"
```
For Interface related action chains the following commands will create the datastore key value pairs needed.

```sh
# Where to send output from BGP actions.
st2 key set napalm_interface_down_mailto "interfaceevent@example.com"

# What email should be the sender of BGP related notifications
st2 key set napalm_interface_down_mailfrom "stackstorm@example.com"
```


For BGP related action chains the following commands will create the datastore key value pairs needed.

```sh
# Where to send output from BGP actions.
st2 key set napalm_bgpsyslog_mailto "bgpnotify@example.com"

# What email should be the sender of BGP related notifications
st2 key set napalm_bgpsyslog_mailfrom "stackstorm@example.com"
```

## Notes

### HTML Emails

Each action can output an HTML table version of the result, this allows you to
send emails in HTML format with the output nicely formatted.

The HTML header and footer files are used to format nice HTML emails and to
style the templates. Some examples have been provided in the examples directory
and should be copied into a location specified by the key value datastore set
above.

This pack is actively being developed.

### Raw output

Most actions put their output under the key raw and when the htmlout option is ticked (see above)
the output is in 'raw' and 'html'. the cli action also adds a 'raw_array' key to the result so
you can iterate through the lines as 'raw' contains lines with a newline ending.
