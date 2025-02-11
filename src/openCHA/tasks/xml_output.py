from tasks.task import BaseTask
from typing import Any, List

import xml.etree.ElementTree as ET
import json

class XmlOutput(BaseTask):
    """
    **Description:**
            This task converts an array of JSON objects, provided as a string, into a structured XML format.
            When the user requests to enclose the output in XML tags, this task is executed to transform 
            the JSON data into the specified XML format and return it as a string.
    """

    name: str = "xml_output"
    chat_name: str = "XmlOutput"
    description: str = (
        "When a request for enclosing output in XML format is received, call this task."
        "This task transforms an array of JSON objects (in string format) into a structured XML format."
        "Each JSON object is enclosed in <Record> tags, with each key-value pair wrapped in <Item> tags within the record."
    )
    dependencies: List[str] = []
    inputs: List[str] = ["Array of JSON objects in string format"]
    outputs: List[str] = ["XML formatted string"]

    output_type: bool = False
    # False if planner should continue. True if after this task the planning should be
    # on pause or stop. examples are when you have a task that asks user to provide more information
    return_direct: bool = False


    def json_to_xml(self, json_str: str) -> str:
        
        # Parse the JSON string into a Python object
        data = json.loads(json_str)
        
        # Create the root XML element
        root = ET.Element("Output")

        # Iterate over each record in the JSON array
        for record in data:
            record_elem = ET.SubElement(root, "Record")
            
            # Add each item as a separate XML element within the record
            for key, value in record.items():
                item_elem = ET.SubElement(record_elem, "Item")
                item_elem.text = str(value)

        # Convert the XML tree to a string
        xml_str = ET.tostring(root, encoding='unicode')
        
        return xml_str


    def _execute(
        self,
        inputs: List[Any],
    ) -> str:
        
        json_str = inputs[0].strip()

        # Convert JSON to XML format
        xml_output = self.json_to_xml(json_str)

        return xml_output

