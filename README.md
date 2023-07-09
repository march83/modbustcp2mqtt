# modbustcp2mqtt
Polls Modbus TCP and maps data fields to MQTT

Current design allows for SE inverters with a SunSpec modbus map and an export meter (IE meter 0 and meter 1) and delivers to a local network MQTT broker.

## To Do

### Features

**Detach from SE modbus maps and calculations** Currently only works for SolarEdge Sunspec maps. Need to remove these hardcoded maps from main and allow use of any Sunspec model and device by adding more maps with their calculations. With this, need to allow for many devices with many configs to be entered

**Custom MQTT mapping** Currently using a logical mapping design that is tied to the modbus map. Should allow for a custom mapping to be used to allow simulation of different MQTT sources of data (IE, I want to be able to simulate Bolivar or MPower Ignition SCADA based sites)

**Ability to push to AWS IoT brokers** Currently only pushing to local MQTT brokers. Need to push to AWS IoT to be able to use this with cloud services.

### Improvements

**Linting** Initial commit is chicken scratch scripting. Needs to be linted and structured properly

**Better error handling** Currently using a big try except with no nuance. Need to understand why we're failing and whether to continue trying forever or not.