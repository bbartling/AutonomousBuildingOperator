import os
import sys
import asyncio
import rdflib
from rdflib import RDF, Namespace, Graph, URIRef, Literal
from bacpypes3.debugging import bacpypes_debugging, ModuleLogger
from bacpypes3.argparse import SimpleArgumentParser
from bacpypes3.pdu import Address
from bacpypes3.primitivedata import ObjectIdentifier
from bacpypes3.basetypes import PropertyIdentifier
from bacpypes3.apdu import AbortReason, AbortPDU, ErrorRejectAbortNack
from bacpypes3.app import Application
from bacpypes3.vendor import get_vendor_info

# Define namespaces
BACNET = Namespace("http://data.ashrae.org/bacnet/2020#")
BRICK = Namespace("https://brickschema.org/schema/Brick#")
BLDG = Namespace("http://example.com/mybuilding#")

# Point type mappings for VAV boxes
vav_point_type_mappings = {
    "Zone Air Temperature Sensor": ["ZN-T", BRICK.Temperature_Sensor],
    "Zone Temperature Setpoint": ["ZN-SP", BRICK.Temperature_Setpoint],
    "Supply Air Temperature Sensor": ["DA-T", BRICK.Temperature_Sensor],
    "Heating Coil Valve Command": ["HTG-O", BRICK.Valve_Command],
    "Air Damper Command": ["DPR-O", BRICK.Damper_Command],
    "Air Flow Sensor": ["SA-F", BRICK.Air_Flow_Sensor],
    "Supply Air Flow Setpoint": ["SAFLOW-SP", BRICK.Air_Flow_Setpoint],
    "Occupancy Sensor": ["OCC-S", BRICK.Occupancy_Sensor],
    "Occupancy Command": ["OCC-CMD", BRICK.Occupancy_Command],
}

# Point type mappings for AHUs
ahu_point_type_mappings = {
    "Return Fan Status": ["RF-STAT", BRICK.Fan_Status],
    "Supply Fan Status": ["SF-STAT", BRICK.Fan_Status],
    "Supply Fan Speed": ["SF-SPD", BRICK.Fan_Speed],
    "Duct Static Pressure": ["DSP", BRICK.Static_Pressure_Sensor],
    "Duct Static Pressure Setpoint": ["DSP-SP", BRICK.Static_Pressure_Setpoint],
    "Return Air Temperature": ["RAT", BRICK.Temperature_Sensor],
    "Mixing Air Temperature": ["MAT", BRICK.Temperature_Sensor],
    "Leaving Air Temperature": ["LAT", BRICK.Temperature_Sensor],
    "Leaving Air Temperature Setpoint": ["LAT-SP", BRICK.Temperature_Setpoint],
    "Mixing Air Damper Command": ["MAD-CMD", BRICK.Damper_Command],
}

# Point type mappings for Central Plants (Boilers, Chillers)
central_plant_point_type_mappings = {
    "Outdoor Air Temperature": ["OAT", BRICK.Temperature_Sensor],
    "Pump Status": ["PUMP-STAT", BRICK.Pump_Status],
    "Pump Speed": ["PUMP-SPD", BRICK.Pump_Speed],
    "Primary Inlet Temperature": ["PI-T", BRICK.Temperature_Sensor],
    "Primary Outlet Temperature": ["PO-T", BRICK.Temperature_Sensor],
    "Secondary Inlet Temperature": ["SI-T", BRICK.Temperature_Sensor],
    "Secondary Outlet Temperature": ["SO-T", BRICK.Temperature_Sensor],
    "Plant Leaving Temperature Setpoint": ["PLT-SP", BRICK.Temperature_Setpoint],
    "Differential Pressure Setpoint": ["DP-SP", BRICK.Pressure_Setpoint],
}

def prompt_for_hvac_system():
    building_name = input("Enter the building name: ")
    hvac_system_type = input("Enter the HVAC system type (VAV AHU, CAV AHU, Central Plant): ")
    return building_name, hvac_system_type

def prompt_for_vav_type():
    vav_type = input("Does the VAV have hot water reheat? (Y/N): ")
    return vav_type.upper() == 'Y'

def prompt_for_ahu_type():
    has_dx_cooling = input("Does the AHU have DX cooling? (Y/N): ")
    has_gas_burner = input("Does the AHU have a gas burner? (Y/N): ")
    return has_dx_cooling.upper() == 'Y', has_gas_burner.upper() == 'Y'

def read_rdf_file(file_path):
    g = rdflib.Graph()
    g.parse(file_path, format="turtle")
    return g

def extract_device_configurations(graph):
    devices = {}
    for s, p, o in graph:
        if p == BACNET.contains:
            device_id = str(s).split("//")[1]
            devices[device_id] = devices.get(device_id, {})
            point_uri = rdflib.URIRef(o)
            devices[device_id][str(point_uri)] = {
                str(p): str(o) for s, p, o in graph.triples((point_uri, None, None))
            }
    return devices

def prompt_for_mappings(point_name):
    print(f"Enter the Brick class for the BACnet point '{point_name}': ")
    print("Available options: Temperature_Sensor, Temperature_Setpoint, Valve_Command, Damper_Command, Air_Flow_Sensor, Air_Flow_Setpoint, Occupancy_Sensor, Fan_Status, Fan_Speed, Static_Pressure_Sensor, Static_Pressure_Setpoint, Pump_Status, Pump_Speed, Pressure_Setpoint, Occupancy_Command")
    brick_class = input("Brick class: ")
    return f"BRICK.{brick_class}"

def process_and_save_rdf(devices, output_file_path, device_type, room_numbers):
    g = Graph()
    g.bind("brick", BRICK)
    g.bind("bldg", BLDG)
    g.bind("bacnet", BACNET)
    system_uri = BLDG[SYSTEM_NAME]
    g.add((system_uri, RDF.type, URIRef(device_type)))
    
    for device_id, points in devices.items():
        device_uri = BLDG[f"Device_{device_id}"]
        g.add((device_uri, RDF.type, URIRef(device_type)))
        g.add((system_uri, BRICK.feeds, device_uri))
        
        for room_number in room_numbers:
            room_uri = BLDG[f"Room-{room_number}"]
            g.add((room_uri, RDF.type, BRICK.Room))
            g.add((device_uri, BRICK.serves, room_uri))
        
        for point_uri, details in points.items():
            point_name = details.get(f"{BACNET}object-name", "")
            brick_class = prompt_for_mappings(point_name)
            if brick_class and point_name in point_type_mappings:
                new_point_uri = BLDG[f"{point_name}_{device_id}"]
                g.add((new_point_uri, RDF.type, URIRef(brick_class)))
                for prop, value in details.items():
                    g.add((new_point_uri, URIRef(prop), Literal(value)))
            else:
                print(f"Skipping unmapped point: {point_name}")
    
    g.serialize(destination=output_file_path, format="turtle")

async def main() -> None:
    app = None
    g = Graph()
    bacnet_graph = BACnetGraph(g)
    
    try:
        parser = SimpleArgumentParser()
        parser.add_argument(
            "device_identifier",
            type=int,
            help="device identifier",
        )
        parser.add_argument(
            "-o",
            "--output",
            help="output to a file",
        )
        parser.add_argument(
            "-f",
            "--format",
            help="output format",
            default="turtle",
        )
        parser.add_argument(
            "--building-name",
            help="name of the building",
            default="Building1"
        )
        parser.add_argument(
            "--system-name",
            help="name of the HVAC system",
            default="System1"
        )
        parser.add_argument(
            "--vav-box",
            help="name of the VAV box file",
            default="vav_10"
        )
        parser.add_argument(
            "--room-numbers",
            nargs='+',
            help="list of room numbers",
            default=["410", "411", "412"]
        )
        args = parser.parse_args()

        # Set global constants from arguments
        global BUILDING_NAME, SYSTEM_NAME, VAV_BOX
        BUILDING_NAME = args.building_name
        SYSTEM_NAME = args.system_name
        VAV_BOX = args.vav_box
        ROOM_NUMBERS = args.room_numbers

        # Get user inputs for the HVAC system type
        building_name, hvac_system_type = prompt_for_hvac_system()

        # Set the mappings and device type based on the HVAC system type
        if hvac_system_type == "VAV AHU":
            point_type_mappings = vav_point_type_mappings
            device_type = str(BRICK.Variable_Air_Volume_Box)
        elif hvac_system_type == "CAV AHU":
            point_type_mappings = ahu_point_type_mappings
            device_type = str(BRICK.Air_Handler_Unit)
        elif hvac_system_type == "Central Plant":
            point_type_mappings = central_plant_point_type_mappings
            device_type = str(BRICK.Central_Plant)
        else:
            print("Unsupported HVAC system type")
            sys.exit(1)

        # build an application
        app = Application.from_args(args)
        
        # look for the device
        i_ams = await app.who_is(args.device_identifier, args.device_identifier)
        if not i_ams:
            sys.stderr.write("device not found\n")
            sys.exit(1)
        
        i_am = i_ams[0]
        device_address: Address = i_am.pduSource
        device_identifier: ObjectIdentifier = i_am.iAmDeviceIdentifier
        vendor_info = get_vendor_info(i_am.vendorID)
        
        # create a device object in the graph and return it like a context
        device_graph = bacnet_graph.create_device(device_address, device_identifier)
        
        object_list = await object_identifiers(app, device_address, device_identifier)
        for object_identifier in object_list:
            object_proxy = device_graph.create_object(object_identifier)
            
            object_class = vendor_info.get_object_class(object_identifier[0])
            if object_class is None:
                continue
            
            property_list: Optional[List[PropertyIdentifier]] = None
            try:
                property_list = await app.read_property(
                    device_address, object_identifier, "property-list"
                )
                assert isinstance(property_list, list)
                
                setattr(
                    object_proxy,
                    "property-list",
                    property_list,
                )
            except ErrorRejectAbortNack as err:
                continue
            
            for property_name in (
                "object-name",
                "description",
                "present-value",
                "units",
            ):
                try:
                    property_identifier = PropertyIdentifier(property_name)
                    if property_list and property_identifier not in property_list:
                        continue
                    
                    property_class = object_class.get_property_type(property_identifier)
                    if property_class is None:
                        continue
                    
                    property_value = await app.read_property(
                        device_address, object_identifier, property_identifier
                    )
                    setattr(object_proxy, property_name, property_value)
                except ErrorRejectAbortNack as err:
                    continue

        # dump the graph
        rdf_file_path = f"./raw_graph_models/{VAV_BOX}"
        graph = read_rdf_file(rdf_file_path)
        device_configurations = extract_device_configurations(graph)
        output_file_path = args.output if args.output else f"./processed_graph_models/processed_{VAV_BOX}.ttl"
        process_and_save_rdf(device_configurations, output_file_path, device_type, ROOM_NUMBERS)
    
    finally:
        if app:
            app.close()

if __name__ == "__main__":
    asyncio.run(main())
