# NAPALM

[NAPALM](https://github.com/napalm-automation) is a Python library to simplify
and abstract some of the programmatic communication with network devices,
making multi-vendor network automation a little easier. This pack introduces
new capabilities that allow a StackStorm user to leverage NAPALM within
StackStorm in the form of sensors, actions, and more.

This pack leverages the NAPALM library to allow ST2 to perform multivendor
network automation

## Requirements

All Python dependencies are included in requirements.txt. This is primarily
comprised of the various Python libraries that make up the NAPALM project.

## Configuration

1. Look at config.schema.yaml. The napalm.yaml.example file as a base to start
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

Actions in the NAPALM pack largely mirror the NAPALM library methods. Documented
[here](https://napalm.readthedocs.io/en/latest/base.html)

- **loadconfig.yaml**: loads a config (either replace or merge) to a network device

## Rules and Triggers

The pack defines rules for handing syslog events or monitoring events. Logstash
is a good source for handling syslog events and extracting the required
parameters. There is an example logstash configuration in the examples
directory.

- **configured_device_chain**: Webhook trigger to run a remote backup action chain when a configuration change is detected on a device.
- **bgp_prefix_exceeded_chain**: Webhook trigger to run an action chain when a bgp neighbour exceeds its prefix limit.

## Datastore

Action chains in this pack require certain datastore values to be set.

Common datastore key value pairs for all the action chains and workflows.

```sh
# Where to send notifications when an action chain fails.
st2 key set napalm_actionerror_mailto "stackstorm_errors@example.com"

# What email should be the sender of failure notifications
st2 key set napalm_actionerror_mailfrom "stackstorm@example.com"
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

For BGP related action chains the following commands will create the datastore key value pairs needed.

```sh
# Where to send output from BGP actions.
st2 key set napalm_bgpsyslog_mailto "bgpnotify@example.com"

# What email should be the sender of BGP related notifications
st2 key set napalm_bgpsyslog_mailfrom "stackstorm@example.com"
```


## Notes

This pack is actively being developed.
