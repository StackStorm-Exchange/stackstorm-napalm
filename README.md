# NAPALM

[NAPALM](https://github.com/napalm-automation) is a Python library to simplify and abstract some of the programmatic communication with network devices, making multi-vendor network automation a little easier. This pack introduces new capabilities that allow a StackStorm user to leverage NAPALM within StackStorm in the form of sensors, actions, and more.

This pack leverages the NAPALM library to allow ST2 to perform multivendor network automation

## Actions

- **napalm_loadconfig.yaml**: loads a config (either replace or merge) to a network device

## Sensors

- **napalm_bgpsensor**: retrives operational information about the BGP process running on a device

## Requirements

All Python dependencies are included in requirements.txt. This is primarily comprised of the various Python libraries that make up the NAPALM project.

## Configuration

1. Edit config.schema.yaml and look at the options. This is where you'll need to tell StackStorm about the network devices you wish to monitor with the various sensors.

## Notes

This pack is actively being developed.
