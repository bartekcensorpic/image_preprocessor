from src.image_preprocessor import process_all_images
import argparse

def init(args):
    output_path = args.output_path
    input_path = args.input_path
    resized_image_shape = (args.resize_image_width, args.resize_image_height)
    process_all_images(input_path= input_path, output_path=output_path, resized_image_shape=resized_image_shape)


def main():
    parser = argparse.ArgumentParser(description='Preprocessing the images')

    parser.add_argument(
        "--output_path",
        type=str,
        help="Path to place where you want your output."
    )

    parser.add_argument(
        "--input_path",
        type=str,
        help="Path to root folder with the folders of categories."
    )

    parser.add_argument(
        "--resize_image_width",
        type=int,
        help="Width of resized images in pixels (int)",
        default=640,
    )

    parser.add_argument(
        "--resize_image_height",
        type=int,
        help="Height of resized images in pixels (int)",
        default=640,

    )

    args = parser.parse_args()
    print(print(args))
    init(args)

if __name__ == '__main__':
    main()
