from ncclient import manager #manager object to connec to the device
from xml.dom import minidom #minidom to pretty print the xml output
import yaml #yaml to read the user credentials from a yaml file

with open ("credintials/credintials.yaml", "r") as file: #
    data = yaml.safe_load(file) #Load the yaml file

with open("subtree_xml/event_information.xml", "r") as file_xml:
    filter = file_xml.read() #Read the filter xml file

    print("Select the option from below")
    print("1. Get Event subscription configurations")

    while True: 
        try: 
            chose = int(input("Enter your choice:"))
            if 1 <= chose <= 1: # Check if the choice is valid

                with manager.connect(**data["my_device"]) as m: #Connect to the device using the credentials from the yaml file
                    result = m.get(filter=("subtree", filter)).xml
                    print(minidom.parseString(result).toprettyxml()) #Pretty print the xml output
                break

            else: 
                print("Please enter a number between 1 and 2")
        except ValueError: 
            print("Invalid input. Please enter a number between 1 and 2")
    

   

