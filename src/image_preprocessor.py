from PIL import Image
from pathlib import Path
import os
from utils import *
import pandas as pd
from typing import List, Tuple
from sklearn.preprocessing import LabelBinarizer
import pickle
import numpy as np


def process_image(
    df: pd.DataFrame,
    current_id: int,
    encoder: LabelBinarizer,
    current_category_name: str,
    images_in_category: List,
    output_image_folder_path: str,
    resized_image_shape:Tuple,
    zero_fill_id=16,
):
    """
    Saves current folder images (as a category) to a new folder, with changed name and its data saved to a dataframe

    :param df: previous dataframe
    :param current_id: current file index
    :param encoder: encoder used to categorise picture label
    :param current_category_name: name of current category
    :param images_in_category: list of names of picture files
    :param output_image_folder_path: folder where the pictures will be saved to
    :param resized_image_shape: desired shape of the output images
    :param zero_fill_id: number of leading zeros in the file name
    :return: DataFrame with current category data, current file index
    """

    #todo save original picture name with folder it is in, so we can upload only new images and skip the ones that already are on the bucket
    for image in images_in_category:

        orignal_name  = os.path.join(current_category_name,os.path.split(image)[1])
        image_path = str(image)

        str_id = str(current_id).zfill(zero_fill_id)
        current_id += 1

        image_new_name = f"img_{current_category_name}_{str_id}.jpg"
        binarized_label = encoder.transform([current_category_name])

        #save image file name, its category in 1hot encoding and its category name
        df.loc[len(df)] = [image_new_name, binarized_label.flatten().tolist(), current_category_name, orignal_name]
        new_image_path = os.path.join(output_image_folder_path, image_new_name)
        img = Image.open(image_path).resize(resized_image_shape)

        # todo normalize picture here if you want.
        # todo Keras training model (for 16/10/2019) normalizes (divides by 255) and applies trasformation to the images.

        try:
            img.save(new_image_path)
        except OSError:
            img.convert('RGB').save(new_image_path)

    #reutrning current_id instead
    print(f"Processed category {current_category_name}, {len(df)} in total")
    return df, current_id



def process_all_images(input_path: str, output_path: str, resized_image_shape: Tuple):
    """
    Reads the folders, names categories with their names and returns CSV file with metadata

    :param input_path: path to folders with pictures
    :param output_path: path where output will be returned
    :param resized_image_shape: shape of images to be returned
    :return:
    """

    output_images_path = os.path.join(output_path, "images")
    csv_file_path = os.path.join(output_path, "metadata.csv")

    prepare_folders(output_path, output_images_path)
    prepare_csv(csv_file_path)

    df = pd.read_csv(csv_file_path)
    current_id = 1 #has to check the current id in the folder or be set to 1 if none
    categories_names = list(os.listdir(input_path))

    encoder = LabelBinarizer()
    encoder.fit(categories_names)

    #Todo so far it is useless :( delete one day
    #save encoder to file so we can use it in algorithm
    pickle_output = open(os.path.join(output_path,'classes_encoder.pkl'), 'wb')
    pickle.dump(encoder, pickle_output)

    for folder_name in os.listdir(input_path):
        current_category_name = folder_name
        category_path = os.path.join(input_path, folder_name)
        images_in_category = list(Path(category_path).glob("*.jpg"))
        df, current_id = process_image(
            df, current_id, encoder, current_category_name, images_in_category,output_images_path, resized_image_shape
        )

        df.to_csv(csv_file_path, index=False, quotechar='"', encoding='ascii')

    print("done, processed", len(df), "images")
