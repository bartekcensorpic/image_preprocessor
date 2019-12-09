from src.preprocessing_with_df.image_preprocessor_mturk import process_all_images
import argparse
from src.transformations import TransformationsEnum

def init(args):
    output_path = args.output_path
    csv_file_path = args.csv_file_path
    resized_image_shape = (args.resize_image_width, args.resize_image_height)

    transformations = []
    if args.to_hog == True:
        transformations.append(TransformationsEnum('hog'))
    if args.to_grayscale == True:
        transformations.append(TransformationsEnum('grayscale'))
    if args.edge_enhance == True:
        transformations.append(TransformationsEnum('edge_enh'))
    if args.total_variance_denoising == True:
        transformations.append(TransformationsEnum('tv_den'))

    process_all_images(input_csv_file_path= csv_file_path, output_path=output_path, resized_image_shape=resized_image_shape,transformations = transformations)


def main():
    parser = argparse.ArgumentParser(description='Preprocessing the images. Reads images from category folders,'
                                                 ' saves them to one folder and creates CSV file that describes each file.')

    parser.add_argument(
        "--output_path",
        type=str,
        help="Path to place where you want your output. If not empty you will be asked to delete it."
    )

    parser.add_argument(
        "--csv_file_path",
        type=str,
        help="Path to CSV with data about images"
    )

    parser.add_argument(
        "--resize_image_width",
        type=int,
        help="Width of resized images in pixels (int)",
        default=224,
    )

    parser.add_argument(
        "--resize_image_height",
        type=int,
        help="Height of resized images in pixels (int)",
        default=224,

    )

    parser.add_argument(
        "--to_grayscale",
        type=bool,
        help="Converts images to grayscale (and to PNG)",
        default=False,
    )

    parser.add_argument(
        "--to_hog",
        type=bool,
        help="Converts images to Histogram of oriented gradients (and to PNG)",
        default=False,
    )

    parser.add_argument(
        "--edge_enhance",
        type=bool,
        help="Converts images with edge enhacement",
        default=False,
    )

    parser.add_argument(
        "--total_variance_denoising",
        type=bool,
        help="Converts images with total_variance_denoising",
        default=False,
    )

    args = parser.parse_args()
    print(print(args))
    init(args)

if __name__ == '__main__':
    main()
