from renderers import ArcGISRenderFactory
from random import seed
import argparse
import os


def verify_args(parser, args):
    """
    Verify all argument are correct to run the script.
    """

    if not os.path.exists(args.color_scheme):
        msg = "Must specify a valid path to a csv color scheme."
        parser.error(msg)

    if not os.path.exists(args.js_path):
        msg = "Must specify a valid path to save JS code to."
        parser.error(msg)

    if args.layer == "domain":
        if args.img_path is not None and not os.path.exists(args.img_path):
            msg = "Must specify a valid path to save color scheme images to."
            parser.error(msg)

    elif args.layer == "kuni":
        if args.img_path is not None or args.gen_images or args.img_server:
            msg = "Kuni layer does not use image fill symbology. No need to specify:\n\
                img_path | gen_images | img_server"

            parser.error(msg)


if __name__ == "__main__":
    app_desc = \
        """
        Python3 script to procedurally generate JS code and images to use with ArcgGIS Javascript API FeatureLayer renderer objects.
        JS and images together form a color scheme for a given layer. Images only created if --img_path argument is specified.

                Example Usage:
                    python3 colorSchemes.py --layer=domain --color_scheme=default.csv --js_path=./js/ --img_path=./imgs/

                NOTES:
                    (1) PATH names MUST end in a backslash
                    (2) Must run: export IMG_URL="<my_image_base_url>/" to specify image server address before start of script.
        """

    parser = argparse.ArgumentParser(description=app_desc)
    parser.add_argument(
        "--layer",
        type=str,
        help=
        "[domain | kuni] - Specify layer to generate color scheme: REQUIRED")
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="[int] - Seed for random generation: Default None")
    parser.add_argument(
        "--color_scheme",
        type=str,
        help="[PATH (csv)] - File path to color scheme: REQUIRED")
    parser.add_argument(
        "--js_path",
        type=str,
        help="[PATH] - Absolute path to save Javascript code: REQUIRED")
    parser.add_argument(
        "--img_path",
        type=str,
        default=None,
        help="[PATH] - Absolute path to create and save images: Default None")

    args = parser.parse_args()

    if args.seed:
        seed(args.seed)

    verify_args(parser, args)

    # Generate the code and images
    generator = ArcGISRenderFactory(args.img_path, args.js_path,
                                    args.color_scheme)
    generator.create_renderer(args.layer)
