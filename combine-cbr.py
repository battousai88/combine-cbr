import os
from pathlib import Path
import argparse
import zipfile as zf


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='+', help='Arbitrary number of input .cbr/.cbz/.zip files')
    parser.add_argument('-f', '--file', help='Text input file listing individual files to combine')
    parser.add_argument('-d', '--dir', nargs='+', help='Directory containing image files to combine into .cbr file')
    parser.add_argument('--create_cbr', nargs='+', help='Create a cbr file from the specified directory containing image files')
    parser.add_argument('-o', '--output', help='Name of the output file. Uses name of input directory if omitted')
    return parser


def zip_recur(filepath, dir, myzip):
    p = Path(filepath)
    myzip.write(filepath, os.path.join(dir, os.path.basename(filepath)))
    if os.path.isdir(filepath):
        files = [f for f in p.iterdir()]
        for fp in files:
            zip_recur(fp, os.path.join(dir, os.path.basename(p)), myzip)


def zip(filepath, output_name):
    try:
        with zf.ZipFile(output_name, 'w') as myzip:
            zip_recur(filepath, '', myzip)
            print("%s created successfully" % output_name)
        with zf.ZipFile(output_name, 'r') as file:
            print('validating %s' % output_name)
            print(file.namelist())
    except IOError as e:
        print(e)


def unzip(filename):
    print('unzipping: %s' % filename)
    try:
        with zf.ZipFile(filename, 'r') as myzip:
            myzip.extractall(os.path.dirname(filename))
    except zf.BadZipfile as e:
        print(e)


def combine(zip_args, output_name):
    zip(zip_args, output_name)


def parse_args():
    parser = create_parser()
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    if args.input:
        [unzip(x) for x in args.input]
    if args.dir:
        pass
    if args.create_cbr:
        [combine(x, output_name='%s/%s' % (os.path.split(x)[0], args.output) if args.output else '%s.cbr' % x) for x in args.create_cbr]
