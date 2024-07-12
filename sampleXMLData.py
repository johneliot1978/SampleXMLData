# Description: command line python script to query an xml file and pull a random sample of some number of a particular element and it's children from the xml tree and write the samples out to subset xml file
import sys
import xml.etree.ElementTree as ET
import random
import xml.dom.minidom

def prettify(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = ET.fromstring(rough_string)
    return xml.dom.minidom.parseString(ET.tostring(reparsed)).toprettyxml(indent="    ")

def find_elements_by_path(root, element_path):
    """Find elements in XML tree based on the specified element_path."""
    elements = root.findall(element_path)
    return elements

def create_sample_xml(input_file, output_file, element_path, num_elements):
    try:
        # Parse the input XML file
        tree = ET.parse(input_file)
        root = tree.getroot()

        # Find all elements based on the specified element_path
        elements = find_elements_by_path(root, element_path)

        # Ensure we have enough elements based on the specified number
        if len(elements) < num_elements:
            print(f"Error: Input XML file does not contain enough '{element_path}' elements ({num_elements}).")
            return
        
        # Choose random elements based on the specified number
        random_elements = random.sample(elements, num_elements)

        # Create a new XML structure for the sampled elements
        sampled_root = ET.Element(element_path.split('/')[-1] + 's')  # Pluralize element name for the root
        for elem in random_elements:
            sampled_root.append(elem)

        # Write the sampled data to the output file with indentation
        with open(output_file, 'wb') as f:
            f.write(prettify(sampled_root).encode('utf-8'))

        print(f"Successfully created {output_file} with {num_elements} randomly sampled '{element_path}' elements.")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <input_xml> <element_path> <num_elements>")
        print("Example: python script.py input.xml user 5")
        print("Note: Don't include your root element in your path above, exclude it.")
        print("For example if the XML tree is /users/user/id, and you want to get samples")
        print("of id, use would specify /user/id or sampes of user would be just user, ")
        print("as we exclude specifing the root element.")
    else:
        input_xml = sys.argv[1]
        element_path = sys.argv[2]
        num_elements = int(sys.argv[3])  # Convert the third argument to an integer
        
        # Generate the output file name dynamically
        base_name = input_xml.rsplit('.', 1)[0]  # Remove file extension
        output_xml = f"{base_name}-{element_path.replace('/', '_')}-{num_elements}-sample.xml"
        
        create_sample_xml(input_xml, output_xml, element_path, num_elements)
