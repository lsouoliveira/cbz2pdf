from zipfile import ZipFile
from tempfile import TemporaryDirectory
import argparse
import os
import subprocess

IMG_PATTERN ='*.{png,jpeg,jpg}' 

def build_magick_convert_cmd(images_path, output_path):
    return ['magick', 'convert', images_path, "-quality", "100", output_path] 

def format_output_filename(filename):
    return '{}.pdf'.format(filename)

def convert_cbz_to_pdf(file_path, output_path):
    filename, _ = os.path.splitext(file_path)

    with ZipFile(file_path) as zip_file:
        with TemporaryDirectory() as tmp_dir_path:
            zip_file.extractall(tmp_dir_path)

            tmp_images_path = os.path.join(tmp_dir_path, IMG_PATTERN)
            pdf_output_path = os.path.join(output_path, format_output_filename(filename)) 

            command = build_magick_convert_cmd(tmp_images_path, pdf_output_path)

            subprocess.run(command, check=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='cbz2pdf', description="Convert a CBZ file to a PDF file.")

    parser.add_argument('output', type=str, help='The output file path')
    parser.add_argument('file', type=str, help='The file path')

    args = parser.parse_args()

    convert_cbz_to_pdf(args.file, args.output)
