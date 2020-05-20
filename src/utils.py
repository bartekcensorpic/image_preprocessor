import shutil
import csv
import sys
import os

def prepare_folders(output_path, output_images_path) -> None:
    """
    Checks for availability of the folders. If output folders already exists it will ask user to delete it. If users says 'no', the program stops.

    :param output_path: Root path to the output
    :param output_images_path: Assumes that output_images_path is a nested folder of output_path. Crude but works for now (16/10/2019)
    :return: None
    """
    if os.path.exists(output_path):
        yes = '-Y'
        no = '-N'

        output = None
        while output not in {yes, no}:
            message = f"Directory {output_path} will be deleted, are you sure? '-Y' yes, '-N' no"
            print(message)
            output = input()

        if output == yes:
            shutil.rmtree(output_path)
        else:
            sys.exit(f'Exiting to not delete the path content: {output_path}')

    os.makedirs(output_path)
    os.makedirs(output_images_path)


def prepare_csv(csv_file_path:str)-> None:
    """
    Initialised a CSV file with columns: 'image_name', 'category_id', 'category_name', 'orignal_file_name'

    :param csv_file_path:
    :return: None
    """

    image_id = 'image_name'
    category_id = 'category_id'
    category_name = 'category_name'
    original_name = 'orignal_file_name'
    columns = [image_id, category_id, category_name,original_name]

    with open(csv_file_path,'w+') as write_file:
        writer = csv.writer(write_file)
        writer.writerow(columns)

    write_file.close()
