from src.preprocessing_object_detection_dataset.process_nude_images import process_nude_images


def create_csv(output_path, annots_folder_path, nude_img_folder_path, non_nude_img_folder_path):

    columns = ['image_path','tags','boobsPecs','nipples','Vaginas','penis','nakedWoman','nakedMan', 'nonNude' ]

    nude_train_df, nude_test_df = process_nude_images(columns, annots_folder_path, nude_img_folder_path)
