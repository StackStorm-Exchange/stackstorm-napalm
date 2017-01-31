# NAPALM

[NAPALM](https://github.com/napalm-automation) is a Python library to simplify and abstract some of the programmatic communication with network devices, making multi-vendor network automation a little easier. This pack introduces new capabilities that allow a StackStorm user to leverage NAPALM within StackStorm in the form of sensors, actions, and more.

This pack leverages the NAPALM library to allow ST2 to perform multivendor network automation

## Actions

- **napalm_loadconfig.yaml**: loads a config (either replace or merge) to a network device

## Rules

The pack defines rules for handing syslog events or monitoring events. Logstash is a good source for handling syslog events and extracting the required parameters.

- **bgp_neighbour_down**: Webhook trigger to run a workflow when a bgp neighbour goes down.
- **bgp_prefix_trigger**: Webhook trigger to run a workflow when a bgp neighbour exceeds its prefix limit.
- **interface_flap**: Webhook trigger to run a workflow when an interface goes down.

## Requirements

All Python dependencies are included in requirements.txt. This is primarily comprised of the various Python libraries that make up the NAPALM project.

## Configuration

1. Edit config.schema.yaml and look at the options. This is where you'll need to tell StackStorm about the network devices you wish use.

## Notes

This pack is actively being developed.
