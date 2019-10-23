from src.image_preprocessor import process_all_images
import argparse
from src.transformations import TransformationsEnum

def init(args):
    output_path = args.output_path
    input_path = args.input_path
    resized_image_shape = (args.resize_image_width, args.resize_image_height)

    transformations = []
    if args.to_hog == True:
        transformations.append(TransformationsEnum('hog'))
    if args.to_greyscale == True:
        transformations.append(TransformationsEnum('greyscale'))

    process_all_images(input_path= input_path, output_path=output_path, resized_image_shape=resized_image_shape,transformations = transformations)


def main():
    parser = argparse.ArgumentParser(description='Preprocessing the images. Reads images from category folders,'
                                                 ' saves them to one folder and creates CSV file that describes each file.')

    parser.add_argument(
        "--output_path",
        type=str,
        help="Path to place where you want your output. If not empty you will be asked to delete it."
    )

    parser.add_argument(
        "--input_path",
        type=str,
        help="Path to root folder with the folders of categories. Categories in CSV will be named after folders names"
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
        "--to_greyscale",
        type=bool,
        help="Converts images to greyscale (and to PNG)",
        default=False,
    )

    parser.add_argument(
        "--to_hog",
        type=bool,
        help="Converts images to Histogram of oriented gradients (and to PNG)",
        default=False,
    )

    args = parser.parse_args()
    print(print(args))
    init(args)

if __name__ == '__main__':
    main()
