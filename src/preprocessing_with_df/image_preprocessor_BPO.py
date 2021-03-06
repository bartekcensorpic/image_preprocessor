from PIL import Image
from pathlib import Path
import os
from src.utils import *
import pandas as pd
from typing import List, Tuple
from sklearn.preprocessing import LabelBinarizer
import matplotlib.pyplot as plt
import pickle
import numpy as np
from src.transformations import *
import traceback


def process_image(
    df: pd.DataFrame,
    current_id: int,
    encoder: LabelBinarizer,
    current_category_name: str,
    images_in_category: List,
    output_image_folder_path: str,
    resized_image_shape:Tuple,
    transformations:List[TransformationsEnum],
    zero_fill_id=16,
):
    """
    Saves current folder images (as a category) to a new folder, with changed name and its data saved to a dataframe

    :param transformations: List of transformations
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

        image_new_name = f"img_{current_category_name}_{str_id}.png"
        binarized_label = encoder.transform([current_category_name])

        #save image file name, its category in 1hot encoding and its category name
        df.loc[len(df)] = [image_new_name, binarized_label.flatten().tolist(), current_category_name, orignal_name]
        new_image_path = os.path.join(output_image_folder_path, image_new_name)
        img = Image.open(image_path).convert('RGB').resize(resized_image_shape)

        #apply transformations
        if TransformationsEnum('hog') in transformations:
            img = to_hog(img)
            # because something fucky happens when you try apply HOG and rescale its intensity and then try to save it using pillow :(
            plt.imsave(new_image_path, img)
            continue

        if TransformationsEnum('grayscale') in transformations:
            img = to_gray_scale(img)

        if TransformationsEnum('edge_enh') in transformations:
            img = edge_enhacement(img)

        if TransformationsEnum('tv_den') in transformations:
            img = denoise_tv(img)

        img.save(new_image_path)


    #reutrning current_id instead
    print(f"Processed category {current_category_name}, {len(df)} in total")
    return df, current_id



def process_all_images(input_csv_file_path: str, output_path: str, resized_image_shape: Tuple,transformations:List[TransformationsEnum]):
    """
    Reads the folders, names categories with their names and returns CSV file with metadata

    :param csv_file_path: path to folders with pictures
    :param output_path: path where output will be returned
    :param resized_image_shape: shape of images to be returned
    :return:
    """

    #TODO use transformation list

    output_image_folder_path = os.path.join(output_path, "images")
    prepare_folders(output_path, output_image_folder_path)
    csv_file_path = os.path.join(output_path, "metadata.csv")

    input_df = pd.read_csv(input_csv_file_path)
    new_df = pd.DataFrame(columns=list(input_df.columns))


    new_df['image_name'] = ""
    img_name_format = "img_{}.png"
    n_rows = len(input_df)

    for index, row in input_df.iterrows():

        str_id = str(index).zfill(16)
        new_image_name = img_name_format.format(str_id)
        new_image_path = os.path.join(output_image_folder_path, new_image_name)



        image_path = row['url']
        try:
            img = Image.open(image_path).convert('RGB').resize(resized_image_shape)
            img.save(new_image_path)
            row['image_name'] = new_image_name
            new_df = new_df.append(row, ignore_index=True)
        except:
            print(traceback.print_exc())
            print(f"Error with image {image_path}, skipping")
            continue

        if index % 20 ==0:
            print(np.round(((index+1)/n_rows)*100,decimals=3),'%', new_image_name)
            print('new_df length:', len(new_df))



    new_df = new_df.loc[(new_df['image_name'] != '') & (new_df['tags'] != '')]

    new_df.to_csv(csv_file_path, index=False, quotechar='"', encoding='ascii')
    print('done (without removing duplicates)')



    # #################### remove classes with less than 5 instances
    # df = pd.read_csv(csv_file_path)
    #
    # print('removing classes with less than 5 instances')
    # unique_vals = list(df.drop_duplicates('tags')['tags'])#.apply(lambda x: x[1:-1].replace('\'','').split(',')))
    #
    # print('length:',len(df))
    # dataset_clean = False
    # while (not dataset_clean):
    #     dataset_clean = True
    #     for index,val in enumerate(unique_vals):
    #         frame = df[df['tags'] == val]
    #
    #         n_img = len(frame)
    #         print(index, n_img , '\t\t', val)
    #         if n_img < 5:
    #             dataset_clean = False
    #             print('=====')
    #             print(frame)
    #             df = df[~df['url'].isin(frame['url'])]
    #             print('length:',len(df))
    #             print('########')
    #             print('_____________________')
    #
    # print('length:',len(df))
    #
    #
    #
    #
    # df.to_csv(csv_file_path, index=False, quotechar='"', encoding='ascii')
    # print('removing duplicates done!')


