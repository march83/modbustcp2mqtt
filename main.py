"""Module does some description
"""
import time
from datetime import datetime, timedelta
from pyModbusTCP.client import ModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
import paho.mqtt.client as mqtt

# and i need a comment now?
def decode_unpack(data_m0, meter0_map):
    map_x = {}
    for reg in meter0_map:
        if reg.get('used', False) != False:
            key = reg.get('name',0)
            if reg.get('type') == "UINT16":
                value = data_m0.decode_16bit_uint()
            elif reg.get('type') == "UINT32":
                value = data_m0.decode_32bit_uint()
            elif reg.get('type') == "SINT16":
                value = data_m0.decode_16bit_int()                
            elif reg.get('type') == "PRINT":
                print(data_m0.decode_string(size=2))                
            else:
                value = -99
                data_m0.skip_bytes(2)
            # map_x.append({"key": key, "value": value})
            map_x[key] = value
        else:
            data_m0.skip_bytes(2)
    return map_x


meter0map = [
    {"reg": 40070, "name": "na",                                    "type": "UINT16",   "used": False},
    {"reg": 40071, "name": "na",                                    "type": "UINT16",   "used": False},
    {"reg": 40072, "name": "ac_total_current",                      "type": "UINT16",   "used": True},
    {"reg": 40073, "name": "ac_current_phase_a",                    "type": "UINT16",   "used": True},
    {"reg": 40074, "name": "ac_current_phase_b",                    "type": "UINT16",   "used": False},
    {"reg": 40075, "name": "ac_current_phase_c",                    "type": "UINT16",   "used": False},
    {"reg": 40076, "name": "ac_current_scalefactor",                "type": "SINT16",   "used": True},
    {"reg": 40077, "name": "ac_voltage_phase_ab",                   "type": "UINT16",   "used": True},
    {"reg": 40078, "name": "ac_voltage_phase_bc",                   "type": "UINT16",   "used": False},
    {"reg": 40079, "name": "ac_voltage_phase_ca",                   "type": "UINT16",   "used": False},
    {"reg": 40080, "name": "ac_voltage_phase_a",                    "type": "UINT16",   "used": True},
    {"reg": 40081, "name": "ac_voltage_phase_b",                    "type": "UINT16",   "used": False},
    {"reg": 40082, "name": "ac_voltage_phase_c",                    "type": "UINT16",   "used": False},
    {"reg": 40083, "name": "ac_voltage_phase_scalefactor",          "type": "SINT16",   "used": True},
    {"reg": 40084, "name": "ac_power_output",                       "type": "SINT16",   "used": True},
    {"reg": 40085, "name": "ac_power_scalefactor",                  "type": "SINT16",   "used": True},
    {"reg": 40086, "name": "freq",                                  "type": "UINT16",   "used": True},
    {"reg": 40087, "name": "freq_scalefactor",                      "type": "SINT16",   "used": True},
    {"reg": 40088, "name": "ac_va",                                 "type": "SINT16",   "used": True},
    {"reg": 40089, "name": "ac_va_scalefactor",                     "type": "SINT16",   "used": True},
    {"reg": 40090, "name": "ac_var",                                "type": "SINT16",   "used": True},
    {"reg": 40091, "name": "ac_var_scalefactor",                    "type": "SINT16",   "used": True},
    {"reg": 40092, "name": "ac_pf",                                 "type": "SINT16",   "used": True},
    {"reg": 40093, "name": "ac_pf_scalefactor",                     "type": "SINT16",   "used": True},
    {"reg": 40094, "name": "lifetime",                              "type": "UINT32",   "used": True},
    # {"reg": 40095, "name": "na",                            "type": "na", "used": False},
    {"reg": 40096, "name": "lifetime_scale_factor",                 "type": "UINT16",   "used": True},
    {"reg": 40097, "name": "dc_current",                            "type": "UINT16",   "used": True},
    {"reg": 40098, "name": "dc_current_scalefactor",                "type": "SINT16",   "used": True},
    {"reg": 40099, "name": "dc_voltage",                            "type": "UINT16",   "used": True},
    {"reg": 40100, "name": "dc_voltage_scalefactor",                "type": "SINT16",   "used": True},
    {"reg": 40101, "name": "dc_power",                              "type": "SINT16",   "used": True},
    {"reg": 40102, "name": "dc_power_scalefactor",                  "type": "SINT16",   "used": True},
    {"reg": 40103, "name": "na",                                    "type": "UINT16",   "used": False},
    {"reg": 40104, "name": "temp_sink",                             "type": "SINT16",   "used": True},
    {"reg": 40105, "name": "na",                                    "type": "UINT16",   "used": False},
    {"reg": 40106, "name": "na",                                    "type": "UINT16",   "used": False},
    {"reg": 40107, "name": "temp_sink_scalefactor",                 "type": "SINT16",   "used": True},
    {"reg": 40108, "name": "status",                                "type": "UINT16",   "used": True},        
]

meter1map = [
    { 'reg': 40188, 'name': "m1_sunspec_id",                        'type': "UINT16", 'used': True },
    { 'reg': 40189, 'name': "m1_sunspec_len",                       'type': "UINT16", 'used': True },
    { 'reg': 40190, 'name': "m1_ac_current",                        'type': "SINT16", 'used': True },
    { 'reg': 40191, 'name': "m1_ac_current_phase_a",                'type': "SINT16", 'used': True },
    { 'reg': 40192, 'name': "na",                                   'type': "SINT16", 'used': False },
    { 'reg': 40193, 'name': "na",                                   'type': "SINT16", 'used': False },
    { 'reg': 40194, 'name': "m1_ac_current_scalefactor",            'type': "SINT16", 'used': True },
    { 'reg': 40195, 'name': "m1_ac_voltage_phase_ln",               'type': "SINT16", 'used': True },
    { 'reg': 40196, 'name': "m1_ac_voltage_phase_an",               'type': "SINT16", 'used': True },
    { 'reg': 40197, 'name': "na",                                   'type': "SINT16", 'used': False },
    { 'reg': 40198, 'name': "na",                                   'type': "SINT16", 'used': False },
    { 'reg': 40199, 'name': "m1_ac_voltage_phase_ll",               'type': "SINT16", 'used': True },
    { 'reg': 40200, 'name': "m1_ac_voltage_phase_ab",               'type': "SINT16", 'used': True },
    { 'reg': 40201, 'name': "na",                                   'type': "SINT16", 'used': False },
    { 'reg': 40202, 'name': "na",                                   'type': "SINT16", 'used': False },
    { 'reg': 40203, 'name': "m1_ac_voltage_scalefactor",            'type': "SINT16", 'used': True },
    { 'reg': 40204, 'name': "m1_ac_frequency",                      'type': "SINT16", 'used': True },
    { 'reg': 40205, 'name': "m1_ac_frequency_scalefactor",          'type': "SINT16", 'used': True },
    { 'reg': 40206, 'name': "m1_ac_power",                          'type': "SINT16", 'used': True },
    { 'reg': 40207, 'name': "na",                                   'type': "SINT16", 'used': False },
    { 'reg': 40208, 'name': "na",                                   'type': "SINT16", 'used': False },
    { 'reg': 40209, 'name': "na",                                   'type': "SINT16", 'used': False },
    { 'reg': 40210, 'name': "m1_ac_power_scalefactor",              'type': "SINT16", 'used': True },
    { 'reg': 40211, 'name': "m1_ac_apparent_power",                 'type': "SINT16", 'used': True },
    { 'reg': 40212, 'name': "na",                                   'type': "SINT16", 'used': False },
    { 'reg': 40213, 'name': "na",                                   'type': "SINT16", 'used': False },
    { 'reg': 40214, 'name': "na",                                   'type': "SINT16", 'used': False },
    { 'reg': 40215, 'name': "m1_ac_apparent_power_scalefactor",     'type': "SINT16", 'used': True },
    { 'reg': 40216, 'name': "m1_ac_reactive_power",                 'type': "SINT16", 'used': True },
    { 'reg': 40217, 'name': "na",                                   'type': "SINT16", 'used': False },
    { 'reg': 40218, 'name': "na",                                   'type': "SINT16", 'used': False },
    { 'reg': 40219, 'name': "na",                                   'type': "SINT16", 'used': False },
    { 'reg': 40220, 'name': "m1_ac_reactive_power_scalefactor",     'type': "SINT16", 'used': True },
    { 'reg': 40221, 'name': "m1_ac_pf",                             'type': "SINT16", 'used': True },
    { 'reg': 40222, 'name': "na",                                   'type': "SINT16", 'used': False },
    { 'reg': 40223, 'name': "na",                                   'type': "SINT16", 'used': False },
    { 'reg': 40224, 'name': "na",                                   'type': "SINT16", 'used': False },
    { 'reg': 40225, 'name': "m1_ac_pf_scalefactor",                 'type': "SINT16", 'used': True },
    { 'reg': 40226, 'name': "m1_ac_energy_exported",                'type': "UINT32", 'used': True },
    { 'reg': 40228, 'name': "na",                                   'type': "UINT32", 'used': False },
    { 'reg': 40230, 'name': "na",                                   'type': "UINT32", 'used': False },
    { 'reg': 40232, 'name': "na",                                   'type': "UINT32", 'used': False },
    { 'reg': 40234, 'name': "m1_ac_energy_imported",                'type': "UINT32", 'used': True },
    { 'reg': 40236, 'name': "na",                                   'type': "UINT32", 'used': False },
    { 'reg': 40238, 'name': "na",                                   'type': "UINT32", 'used': False },
    { 'reg': 40240, 'name': "na",                                   'type': "UINT32", 'used': False },
    { 'reg': 40242, 'name': "m1_ac_energy_scalefactor",             'type': "SINT16", 'used': True },
    { 'reg': 40243, 'name': "m1_ac_apparent_energy_exported",       'type': "UINT32", 'used': True },
    { 'reg': 40245, 'name': "na",                                   'type': "UINT32", 'used': False },
    { 'reg': 40247, 'name': "na",                                   'type': "UINT32", 'used': False },
    { 'reg': 40249, 'name': "na",                                   'type': "UINT32", 'used': False },
    { 'reg': 40251, 'name': "m1_ac_apparent_energy_imported",       'type': "UINT32", 'used': True },
    { 'reg': 40253, 'name': "na",                                   'type': "UINT32", 'used': False },
    { 'reg': 40255, 'name': "na",                                   'type': "UINT32", 'used': False },
    { 'reg': 40257, 'name': "na",                                   'type': "UINT32", 'used': False },
    { 'reg': 40259, 'name': "m1_ac_apparent_energy_scalefactor",    'type': "SINT16", 'used': True },
    { 'reg': 40260, 'name': "na",                                   'type': "UINT32", 'used': False },
    { 'reg': 40262, 'name': "na",                                   'type': "UINT32", 'used': False },
    { 'reg': 40264, 'name': "na",                                   'type': "UINT32", 'used': False },
    { 'reg': 40266, 'name': "na",                                   'type': "UINT32", 'used': False },
    { 'reg': 40268, 'name': "na",                                   'type': "UINT32", 'used': False },
    { 'reg': 40270, 'name': "na",                                   'type': "UINT32", 'used': False },
    { 'reg': 40272, 'name': "na",                                   'type': "UINT32", 'used': False },
    { 'reg': 40274, 'name': "na",                                   'type': "UINT32", 'used': False },
    { 'reg': 40276, 'name': "na",                                   'type': "UINT32", 'used': False },
    { 'reg': 40278, 'name': "na",                                   'type': "UINT32", 'used': False },
    { 'reg': 40280, 'name': "na",                                   'type': "UINT32", 'used': False },
    { 'reg': 40282, 'name': "na",                                   'type': "UINT32", 'used': False },
    { 'reg': 40284, 'name': "na",                                   'type': "UINT32", 'used': False },
    { 'reg': 40286, 'name': "na",                                   'type': "UINT32", 'used': False },
    { 'reg': 40288, 'name': "na",                                   'type': "UINT32", 'used': False },
    { 'reg': 40290, 'name': "na",                                   'type': "UINT32", 'used': False },
    { 'reg': 40292, 'name': "na",                                   'type': "SINT16", 'used': False }
]

# define modbus client
mbHost = "192.168.1.226"
mbPort = 1502
mbM0Register = 40069 
mbM0Length = 39
mbM1Register = 40188
mbM1Length = 105
# mbClient = ModbusClient(host=mbHost, port=mbPort, debug=True, auto_open=True)
mbClient = ModbusClient(host=mbHost, port=mbPort, debug=False, auto_open=True)
mbPollRate = 5

# define mqtt connection
mqttBroker = "192.168.1.167"
mqttPort = 1883
mqttClient = mqtt.Client("modbus-to-mqtt")
mqttClient.connect(mqttBroker)


while True:
    nextTime = datetime.now() + timedelta(seconds=mbPollRate)
    # read modbus

    try:
        print("trying to read modbus")        
        readingM0 = mbClient.read_holding_registers(mbM0Register, mbM0Length)
        dataM0 = BinaryPayloadDecoder.fromRegisters(readingM0, byteorder=Endian.Big, wordorder=Endian.Big)
        mapM0 = decode_unpack(dataM0, meter0map)

        print("trying to read M1")
        readingM1 = mbClient.read_holding_registers(mbM1Register, mbM1Length)
        dataM1 = BinaryPayloadDecoder.fromRegisters(readingM1, byteorder=Endian.Big, wordorder=Endian.Big)
        mapM1 = decode_unpack(dataM1, meter1map)


        values_m0 = {}
        values_m0["ac_total_current"] = round(mapM0["ac_total_current"] * (10 ** mapM0["ac_current_scalefactor"]),2)
        values_m0["ac_current_phase_a"] = round(mapM0["ac_current_phase_a"] * (10 ** mapM0["ac_current_scalefactor"]),2)
        values_m0["ac_voltage_phase_ab"] = round(mapM0["ac_voltage_phase_ab"] * (10 ** mapM0["ac_voltage_phase_scalefactor"]),2)
        values_m0["ac_voltage_phase_a"] = round(mapM0["ac_voltage_phase_a"] * (10 ** mapM0["ac_voltage_phase_scalefactor"]),2)
        values_m0["ac_power_output"] = round(mapM0["ac_power_output"] * (10 ** mapM0["ac_power_scalefactor"]),2)
        values_m0["freq"] = round(mapM0["freq"] * (10 ** mapM0["freq_scalefactor"]),2)
        values_m0["ac_va"] = round(mapM0["ac_va"] * (10 ** mapM0["ac_va_scalefactor"]),2) 
        values_m0["ac_var"] = round(mapM0["ac_var"] * (10 ** mapM0["ac_var_scalefactor"]),2) 
        values_m0["ac_pf"] = round(mapM0["ac_pf"] * (10 ** mapM0["ac_pf_scalefactor"]),2)
        values_m0["lifetime"] = round(mapM0["lifetime"] * (10 ** mapM0["lifetime_scale_factor"]),2)
        values_m0["dc_current"] = round(mapM0["dc_current"] * (10 ** mapM0["dc_current_scalefactor"]),2)
        values_m0["dc_voltage"] = round(mapM0["dc_voltage"] * (10 ** mapM0["dc_voltage_scalefactor"]),2)
        values_m0["dc_power"] = round(mapM0["dc_power"] * (10 ** mapM0["dc_power_scalefactor"]),2)
        values_m0["temp_sink"] = round(mapM0["temp_sink"] * (10 ** mapM0["temp_sink_scalefactor"]),2) 
        values_m0["status"] = mapM0["temp_sink"]
        if values_m0['dc_power'] > 0:
            values_m0['computed_inverter_efficiency'] = round( values_m0['ac_power_output'] / values_m0['dc_power'] * 100 )
        else:
            values_m0['computed_inverter_efficiency'] = 0

    # write mqtt
        print("trying to write mqtt")
    # try:
        for key, value in values_m0.items():
            mqttClient.publish(topic=f"solaredge-mqtt/meter0/{key}", payload=value)
    # except:
    #     print("failed to write MQTT")





        values_m1 = {}
        values_m1["m1_ac_current"] = round(mapM1["m1_ac_current"] * (10 ** mapM1["m1_ac_current_scalefactor"]),2)
        values_m1["m1_ac_current_phase_a"] = round(mapM1["m1_ac_current_phase_a"] * (10 ** mapM1["m1_ac_current_scalefactor"]),2)
        values_m1["m1_ac_voltage_phase_ln"] = round(mapM1["m1_ac_voltage_phase_ln"] * (10 ** mapM1["m1_ac_voltage_scalefactor"]),2)
        values_m1["m1_ac_voltage_phase_an"] = round(mapM1["m1_ac_voltage_phase_an"] * (10 ** mapM1["m1_ac_voltage_scalefactor"]),2)
        values_m1["m1_ac_voltage_phase_ll"] = round(mapM1["m1_ac_voltage_phase_ll"] * (10 ** mapM1["m1_ac_voltage_scalefactor"]),2)
        values_m1["m1_ac_voltage_phase_ab"] = round(mapM1["m1_ac_voltage_phase_ll"] * (10 ** mapM1["m1_ac_voltage_scalefactor"]),2)    
        values_m1["m1_ac_power"] = round(mapM1["m1_ac_power"] * (10 ** mapM1["m1_ac_power_scalefactor"]),2)
        values_m1["m1_ac_frequency"] = round(mapM1["m1_ac_frequency"] * (10 ** mapM1["m1_ac_frequency_scalefactor"]),2)
        values_m1["m1_ac_apparent_power"] = round(mapM1["m1_ac_apparent_power"] * (10 ** mapM1["m1_ac_apparent_power_scalefactor"]),2) 
        values_m1["m1_ac_reactive_power"] = round(mapM1["m1_ac_reactive_power"] * (10 ** mapM1["m1_ac_reactive_power_scalefactor"]),2) 
        # values_m1["m1_ac_pf"] = round(mapM1["m1_ac_pf"] * (10 ** mapM1["m1_ac_pf_scalefactor"]),2)
        # values_m1["m1_ac_energy_exported"] = round(mapM1["m1_ac_energy_exported"] * (10 ** mapM1["m1_ac_energy_scalefactor"]),2)
        # values_m1["m1_ac_energy_imported"] = round(mapM1["m1_ac_energy_exported"] * (10 ** mapM1["m1_ac_energy_scalefactor"]),2)
        # values_m1["m1_ac_apparent_energy_exported"] = round(mapM1["m1_ac_apparent_energy_exported"] * (10 ** mapM1["m1_ac_apparent_energy_scalefactor"]),2)
        # values_m1["m1_ac_apparent_energy_imported"] = round(mapM1["m1_ac_apparent_energy_imported"] * (10 ** mapM1["m1_ac_apparent_energy_scalefactor"]),2)

        # write mqtt
        # try:
        for key, value in values_m1.items():
            mqttClient.publish(topic=f"solaredge-mqtt/meter1/{key}", payload=value)
    except:
        print("failed to write MQTT")

    sleepTime = nextTime - datetime.now()
    sleeptime = sleepTime if sleepTime > timedelta(seconds=0) else timedelta(seconds = 0)
    print(f"sleeping for {sleepTime}")
    time.sleep(round(sleepTime.seconds, 0))
