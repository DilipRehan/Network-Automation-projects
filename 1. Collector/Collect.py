from ncclient import manager #manager object to connec to the device
from xml.dom import minidom #minidom to pretty print the xml output
import yaml #yaml to read the user credentials from a yaml file


with open ("credintials.yaml", "r") as file: #
    data = yaml.safe_load(file) #Load the yaml file




with manager.connect(**data["my_device"]) as m: #Connect to the device using the credentials from the yaml file
    result = m.get(filter=("subtree", filter)).xml
    print(minidom.parseString(result).toprettyxml()) #Pretty print the xml output
   


