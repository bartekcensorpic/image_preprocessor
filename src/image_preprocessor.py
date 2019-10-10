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

    #todo save original picture name with folder it is in, so we can upload only new images and skip the ones that already are on the bucket
    for image in images_in_category:
        image_path = str(image)

        str_id = str(current_id).zfill(zero_fill_id)
        current_id += 1

        image_new_name = f"img_{current_category_name}_{str_id}.jpg"
        binarized_label = encoder.transform([current_category_name])

        #save image file name, its category in 1hot encoding and its category name
        df.loc[len(df)] = [image_new_name, binarized_label.flatten().tolist(), current_category_name]
        new_image_path = os.path.join(output_image_folder_path, image_new_name)
        img = Image.open(image_path).resize(resized_image_shape)

        # todo normalize picture here

        try:
            img.save(new_image_path)
        except OSError:
            img.convert('RGB').save(new_image_path)

        # shutil.copy(image_path, new_image_path)
    #reutrning current_id instead
    print(f"Processed category {current_category_name}, {len(df)} in total")
    return df, current_id



def process_all_images(input_path: str, output_path: str, resized_image_shape: Tuple):
    output_images_path = os.path.join(output_path, "images")
    csv_file_path = os.path.join(output_path, "metadata.csv")

    prepare_folders(output_path, output_images_path)
    prepare_csv(csv_file_path)

    df = pd.read_csv(csv_file_path)
    current_id = 1
    categories_names = list(os.listdir(input_path))

    encoder = LabelBinarizer()
    encoder.fit(categories_names)
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
