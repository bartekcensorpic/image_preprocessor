
import argparse

from src.preprocessing_object_detection_dataset.create_csv import create_csv


def init(args):
    """
    Assumption here is that we have 3 folders with: images with nudity, annotations files and negative examples.

    Allowed classes are:
    boobsPecs
    nipples
    Vaginas
    penis
    nakedWoman
    nakedMan

    it also assumes that images are augmented and their names follow this pattern: (?P<file_path>.*)(_aug_){1}\d+_\d+(\.jpg|\.png)

    it creates 3 CSV files with absolute path to each file, tags, nipples,    Vaginas,    penis,    nakedWoman,    nakedMan, nonNude

    So if differs from CSV produced by other methods from this project
    :param args:
    :return:
    """

    output_path = args.output_path
    annots_folder_path = args.annots_folder_path
    nude_img_folder_path = args.nude_img_folder_path
    non_nude_img_folder_path = args.non_nude_img_folder_path

    create_csv(output_path, annots_folder_path, nude_img_folder_path, non_nude_img_folder_path)

    print('###########Script done')


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--output_path",
        type=str,
        help="Path to place where you want your output. "
    )

    parser.add_argument(
        "--annots_folder_path",
        type=str,
    )
    parser.add_argument(
        "--nude_img_folder_path",
        type=str,
    )
    parser.add_argument(
        "--non_nude_img_folder_path",
        type=str,
    )


    args = parser.parse_args()
    print(print(args))
    init(args)

if __name__ == '__main__':
    main()
