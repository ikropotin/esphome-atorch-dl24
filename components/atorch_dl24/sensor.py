import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import ble_client, sensor
from esphome.const import (
    CONF_CAPACITY,
    CONF_CURRENT,
    CONF_ENERGY,
    CONF_ID,
    CONF_POWER,
    CONF_TEMPERATURE,
    CONF_VOLTAGE,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_EMPTY,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_VOLTAGE,
    ICON_COUNTER,
    ICON_EMPTY,
    ICON_TIMER,
    STATE_CLASS_MEASUREMENT,
    UNIT_AMPERE,
    UNIT_CELSIUS,
    UNIT_EMPTY,
    UNIT_SECOND,
    UNIT_VOLT,
    UNIT_WATT,
    UNIT_WATT_HOURS,
)

CODEOWNERS = ["@syssi"]

CONF_DIM_BACKLIGHT = "dim_backlight"
CONF_RUNNING = "running"
UNIT_AMPERE_HOURS = "Ah"
ICON_CAPACITY = "mdi:battery-medium"
ICON_RUNNING = "mdi:power"

SENSORS = [
    CONF_VOLTAGE,
    CONF_CURRENT,
    CONF_POWER,
    CONF_CAPACITY,
    CONF_ENERGY,
    CONF_TEMPERATURE,
    CONF_DIM_BACKLIGHT,
    CONF_RUNNING,
]

atorch_dl24_ns = cg.esphome_ns.namespace("atorch_dl24")
AtorchDL24 = atorch_dl24_ns.class_("AtorchDL24", ble_client.BLEClientNode, cg.Component)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(AtorchDL24),
        cv.Optional(CONF_VOLTAGE): sensor.sensor_schema(
            UNIT_VOLT, ICON_EMPTY, 1, DEVICE_CLASS_VOLTAGE, STATE_CLASS_MEASUREMENT
        ),
        cv.Optional(CONF_CURRENT): sensor.sensor_schema(
            UNIT_AMPERE,
            ICON_EMPTY,
            3,
            DEVICE_CLASS_CURRENT,
            STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_POWER): sensor.sensor_schema(
            UNIT_WATT, ICON_EMPTY, 4, DEVICE_CLASS_POWER, STATE_CLASS_MEASUREMENT
        ),
        cv.Optional(CONF_CAPACITY): sensor.sensor_schema(
            UNIT_AMPERE_HOURS,
            ICON_CAPACITY,
            4,
            DEVICE_CLASS_ENERGY,
            STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_ENERGY): sensor.sensor_schema(
            UNIT_WATT_HOURS,
            ICON_COUNTER,
            0,
            DEVICE_CLASS_ENERGY,
            STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_TEMPERATURE): sensor.sensor_schema(
            UNIT_CELSIUS,
            ICON_EMPTY,
            0,
            DEVICE_CLASS_TEMPERATURE,
            STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_DIM_BACKLIGHT): sensor.sensor_schema(
            UNIT_SECOND,
            ICON_TIMER,
            0,
            DEVICE_CLASS_EMPTY,
            STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_RUNNING): sensor.sensor_schema(
            UNIT_EMPTY,
            ICON_RUNNING,
            0,
            DEVICE_CLASS_EMPTY,
            STATE_CLASS_MEASUREMENT,
        ),
    }
).extend(ble_client.BLE_CLIENT_SCHEMA)


def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    yield cg.register_component(var, config)
    yield ble_client.register_ble_node(var, config)

    for key in SENSORS:
        if key in config:
            conf = config[key]
            sens = yield sensor.new_sensor(conf)
            cg.add(getattr(var, f"set_{key}_sensor")(sens))
