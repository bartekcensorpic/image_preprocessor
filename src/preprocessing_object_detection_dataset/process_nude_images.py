import pandas as pd

from src.preprocessing_object_detection_dataset.annotations_reader import convert_annotation
from src.preprocessing_object_detection_dataset.utils import process_files_generator
import os
import re
import random

def group_aug_to_df(data, columns):

    df =  pd.DataFrame(columns=columns)
    for random_number, group in data:
        for row in group[1]:
                df.loc[len(df)] = row

    return df


def split_and_shufle(group_aug_dict, columns):
    data = [ (random.random(), group) for group in group_aug_dict.items() ]
    data.sort()
    n_lines = len(data)
    n_train = int(n_lines * 0.6)
    rest =  int(n_lines - n_train)
    n_test = int(rest /2)



    train_df = group_aug_to_df( data[:n_train],columns)
    test_df = group_aug_to_df( data[n_train:n_train+n_test],columns)
    valid_df = group_aug_to_df( data[n_train+n_test:],columns)

    return train_df, valid_df, test_df


def group_by_augmentations(df):
    pattern =  r'(?P<file_path>.*)(_aug_){1}\d+_\d+(\.jpg|\.png)' #we want to group them by their original name. because i wrote it, i know that the pattern is: '<file_path>_aug_<any number>_<any number>.jpg'
    regex =  re.compile(pattern)

    image_to_augmentation_dict = dict()
    for idx,row in df.iterrows():

        file_name = row['image_path']
        matches = regex.search(file_name)
        org_path = matches.group('file_path')

        if org_path not in image_to_augmentation_dict:
            image_to_augmentation_dict[org_path] = [row]
        else:
            image_to_augmentation_dict[org_path].append(row)

    return image_to_augmentation_dict

def find_annotations_nude_image(xml_file_path, nude_img_folder_path, classes):
    '''

    :param xml_file_path:
    :param nude_img_folder_path:
    :return: a row of dataset with all required informations
    '''

    image_name, tags_from_annotation = convert_annotation(xml_file_path,classes)

    image_path = os.path.join(nude_img_folder_path, image_name)

    if os.path.exists(image_path):
        return image_path, list(tags_from_annotation)
    else:
        return None


#columns = ['image_path','tags','boobsPecs','nipples','Vaginas','penis','nakedWoman','nakedMan', 'nonNude' ]

def extract_all_nude_images(columns, annots_folder_path, nude_img_folder_path)-> pd.DataFrame:
    classes =columns[2:]
    annots_gen = process_files_generator(find_annotations_nude_image,
                                         annots_folder_path,
                                         ['*.xml'],
                                         {'nude_img_folder_path': nude_img_folder_path, 'classes':classes},
                                         tqdm_description= 'extracting nudes'
                                         )


    df =  pd.DataFrame(columns=columns)

    for idx,(image_path, tags) in enumerate(annots_gen):

        row = {'image_path': image_path, 'tags':tags}

        for class_name in classes:
            if class_name in tags:
                row[class_name] = True
            else:
                row[class_name] = False
        df.loc[idx] =row



    return df

def process_nude_images(columns, annots_folder_path, nude_img_folder_path):

    nude_df = extract_all_nude_images(columns, annots_folder_path, nude_img_folder_path)

    group_aug_dict = group_by_augmentations(nude_df)

    train_df, validation_df, test_df = split_and_shufle(group_aug_dict, columns)
    ashbdsjkfdj










