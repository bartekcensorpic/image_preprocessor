import xml.etree.ElementTree as ET


def convert_annotation(xml_file_path, classes):

    in_file = open(xml_file_path)
    tree=ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('filename'):
        image_name = obj.text

    tags = set()


    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls not in classes:
            continue
        tags.add(cls)

    if len(tags) == 0:
        tags.add('nonNude')

    return image_name, tags


