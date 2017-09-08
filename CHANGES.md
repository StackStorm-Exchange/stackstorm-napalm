# Change Log

## 0.2.8

- Removes unnecessary exception handling in each action. Was suppressing useful information about the problem
- Catch KeyError when referencing certain config items and provide useful message - clear indicator that config needs provided/reloaded

## 0.2.7

- Added "port" parameter to configuration (sensor now able to set port, actions use this as secondary)

## 0.2.5

- Added missing "credentials" section to `config.schema.yaml`
