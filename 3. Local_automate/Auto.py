from ncclient import manager
from xml.dom import minidom
from xml.etree import ElementTree as ET
import yaml

# ---------------------------------------------------------
# Function to convert routing XML into human-readable text
# ---------------------------------------------------------
def human_readable_routing(xml_data):
    ns = {
        "rt": "urn:ietf:params:xml:ns:yang:ietf-routing",
        "v4": "urn:ietf:params:xml:ns:yang:ietf-ipv4-unicast-routing"
    }

    root = ET.fromstring(xml_data)
    output = []

    # Routing instance
    instance = root.find(".//rt:routing-instance", ns)
    if instance is None:
        return "No routing information found."

    name = instance.find("rt:name", ns).text
    output.append(f"Routing Instance: {name}")

    # Static routes
    for route in root.findall(".//v4:route", ns):
        dest = route.find("v4:destination-prefix", ns).text
        iface = route.find(".//v4:outgoing-interface", ns).text
        output.append(f"Static Route: {dest} → {iface}")

    return "\n".join(output) #Join the output list into a single string


# ---------------------------------------------------------
# Load credentials
# ---------------------------------------------------------
with open("credintials/credintials.yaml", "r") as file:
    data = yaml.safe_load(file)

# ---------------------------------------------------------
# Load XML filter
# ---------------------------------------------------------
with open("xml/event.xml", "r") as file_xml:
    filter_xml = file_xml.read()

# ---------------------------------------------------------
# Menu
# ---------------------------------------------------------
print("Select the option from below")
print("1. Get Event subscription configurations")
print("2. Get Routing (human readable)")

while True:
    try:
        choice = int(input("Enter your choice: "))

        if choice == 1:
            with manager.connect(**data["my_device"]) as m:
                result = m.get(filter=("subtree", filter_xml)).xml
                print(minidom.parseString(result).toprettyxml())
            break

        elif choice == 2:
            with manager.connect(**data["my_device"]) as m:
                result = m.get(filter=("subtree", filter_xml)).xml
                print("\n--- Human Readable Output ---")
                print(human_readable_routing(result))
            break

        else:
            print("Please enter a number between 1 and 2")

    except ValueError:
        print("Invalid input. Please enter a number between 1 and 2")