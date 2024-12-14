import xml.etree.ElementTree as ET

# Create the root element
root = ET.Element("person")

# Create a child element
child = ET.SubElement(root, "name")
child.text = "Almir"

# Create the tree and write to a file
tree = ET.ElementTree(root)
tree.write("person.xml")
