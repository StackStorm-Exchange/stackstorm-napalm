# Change Log

## 1.1.0

- Update napalm dependency to > 3.4 to support Python 3.6+ only
- Fix issue #71

## 1.0.1

- Fix `LLDPNeighborIncrease` trigger in LLDP sensor

## 1.0.0

* Drop Python 2.7 support

## 0.5.0

- Convert mistral workflows to orquesta

## 0.4.1

- Restrict napalm dependency to < 3.0 to preserve Python 2.7 support

## 0.4.0

- Driver reunification - switched to just "napalm" import, removed device-specific and napalm-base

## 0.3.0

- Removed `napalm-ibm` as it is no longer maintained, and pins to an older version of paramiko that breaks other drivers.

## 0.2.16

- Added "nxos_ssh" to supported Napalm drivers for legacy nx-os systems without NX-API support. (inline transfer only)

## 0.2.15

- Version bump to fix tagging issues, no code changes

## 0.2.14

- Support `key_file` for SSH key authentication

## 0.2.13

- Support `secret` parameter for IOS devices that need password to enter enable mode

## 0.2.11

- Added "config_text" parameter to loadconfig action to be able to specify a command to set to device as text

## 0.2.8

- Removes unnecessary exception handling in each action. Was suppressing useful information about the problem
- Catch KeyError when referencing certain config items and provide useful message - clear indicator that config needs provided/reloaded

## 0.2.7

- Added "port" parameter to configuration (sensor now able to set port, actions use this as secondary)

## 0.2.5

- Added missing "credentials" section to `config.schema.yaml`
