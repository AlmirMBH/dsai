import xml.etree.ElementTree as ET

# Parse the XML file
tree = ET.parse("person.xml")
root = tree.getroot()

# Access the child element
name = root.find("name").text
print(name)



tree = ET.parse("messages.xml")
root = tree.getroot()

print("\nLocations")
for location in root.find("Locations"):
    location_id = location.get("id")
    room = location.get("room")
    print(location_id, room)

print("\nMessages")
for message in root.find("Messages"):
    message_id = message.get("id")
    room = message.get("roomId")
    message = message.text.strip()
    print(message_id, room, message)
