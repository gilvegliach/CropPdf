# Example usage:
#   python3 crop_pdf.py -t 40 -i somefile.pdf

import argparse
from pikepdf import Pdf

parser = argparse.ArgumentParser(description="Crop pages of a given pdf")
parser.add_argument("--input", "-i", required=True, help="input file")
parser.add_argument("--output", "-o", help="output file")
parser.add_argument(
    "--asymmetric",
    "-a",
    action="store_true",
    default=False,
    help="flip left and right crop margins on odd pages",
)
parser.add_argument("--top", "-t", type=int, default=45)
parser.add_argument("--left", "-l", type=int, default=45)
parser.add_argument("--right", "-r", type=int, default=45)
parser.add_argument("--bottom", "-b", type=int, default=45)
args = parser.parse_args()

file_in = args.input
file_out = args.output
if file_out is None:
    index = file_in.find(".pdf")
    file_out = file_in + ".cropped"
    if index >= 0:
        file_out = file_in[0:index] + ".cropped.pdf"

top = args.top
left = args.left
right = args.right
bottom = args.bottom

pdf = Pdf.open(file_in)
for i, page in enumerate(pdf.pages):
    should_flip = i % 2 != 0 and args.asymmetric

    # llx lly urx ury
    # Also test .CropBox
    crop_box = page.MediaBox
    crop_box[0] += left if not should_flip else right
    crop_box[1] += bottom
    crop_box[2] -= right if not should_flip else left
    crop_box[3] -= top
    page.MediaBox = crop_box

pdf.save(file_out)
