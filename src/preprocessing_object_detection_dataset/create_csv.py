from src.preprocessing_object_detection_dataset.process_nude_images import process_nude_images, process_sfw_images
import pandas as pd
import os
from sklearn.utils import shuffle

def create_csv(output_path, annots_folder_path, nude_img_folder_path, non_nude_img_folder_path,are_images_augmented):

    columns = ['image_path','tags','boobsPecs','nipples','Vaginas','penis','nakedWoman','nakedMan', 'nonNude' ]

    nude_train_df, nude_val_df, nude_test_df = process_nude_images(columns, annots_folder_path, nude_img_folder_path,are_images_augmented)

    sfw_train_df, sfw_val_df, sfw_test_df = process_sfw_images(columns, non_nude_img_folder_path,are_images_augmented)

    train_df = pd.concat([nude_train_df, sfw_train_df])
    val_df = pd.concat([nude_val_df, sfw_val_df])
    test_df = pd.concat([nude_test_df, sfw_test_df])

    ls = {'train.csv': train_df,
          'val.csv': val_df,
          'test.csv':test_df}

    for name, df in ls.items():
        save_path = os.path.join(output_path, name)
        df = shuffle(df)
        df.to_csv(save_path, index=False, quotechar='"', encoding='ascii')






