# Image preprocessor for image classification algorithm

Due to laziness this program has two entry points and purposes:

1) Our first version of classification algorithm had different classes and structure (cp_algorithm_v2 master branch), we were using S3 buckets so this programs prepares CSV file and copies resized images. Entry point is run_algorithm.py file.

    Pipeline of the whole process of getting data and training algorithms was:
    
    this program -> cp_algorithm_v2 master branch and letting Keras ImageDataGenerator to perform augmentations


    Example parameters:
    
    --output_path
    "C:\Users\Barte\Desktop\trash"
    
    --input_path
    "C:\Users\Barte\Documents\SamplePornData"
    
    --resize_image_width
    224
    
    --resize_image_height
    224
 
2)  Preprocessing image for object_detection_dataset branch of cp_algorithm_v2. As stated there, CSV file and philosophy is a bit different than the one in 1. point, no images are produced.

    Pipeline of the whole process of getting data and training algorithms was:
    
    object_detection_augmentation program -> this one -> cp_algorithm_v2 object_detection_data branch  
    Entry point is src/preprocessing_object_detection_dataset/object_detection_main.py
    
       
    Example paramters:
    
    --annots_folder_path 
    /mnt/efs/augmented_v1/annots
    
    --nude_img_folder_path
    /mnt/efs/augmented_v1/img
    
    --non_nude_img_folder_path
    /mnt/efs/augmented_v1/negative
    
    --output_path
    /mnt/efs/classification_csv
    
    
    

