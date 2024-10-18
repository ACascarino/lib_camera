import matplotlib.pyplot as plt
import numpy as np
import subprocess
from pathlib import Path
from PIL import Image  # To avoid color BGR issues when writing

from string import Template
from test_utils import ImageDecoder, ImageMetrics

met = ImageMetrics()
cwd = Path(__file__).parent.absolute()
imgs = cwd / "src" / "imgs"

cmake_template = Template(
    'cmake \
        -D FILE_IN_NAME="$file_in" \
        -D FILE_OUT_NAME="$file_out" \
        -G Ninja -B build --fresh'
)

build_cmd = "ninja -C build"
run_cmd = "python ../../python/run_xscope_bin.py bin/test_isp_rgb1.xe"


def raw_to_rgb_xcore(raw_file: Path):
    # give cmake a input and output file and runs the isp test
    in_cmake = str(raw_file.relative_to(cwd)).replace("\\", "/")
    out_cmake = in_cmake.replace(".raw", ".rgb")
    out_path = raw_file.with_suffix(".rgb")
    cmake_cmd = cmake_template.substitute(file_in=in_cmake, file_out=out_cmake)
    subprocess.run(cmake_cmd, shell=True, cwd=cwd, check=True)
    subprocess.run(build_cmd, shell=True, cwd=cwd, check=True)
    subprocess.run(run_cmd, shell=True, cwd=cwd, check=True)
    # decode rgb to png image
    dec = ImageDecoder(mode="rgb")
    return dec.decode_rgb(out_path)


def raw_to_rgb_python(raw_file: Path):
    dec = ImageDecoder(mode="raw8")
    return dec.decode_raw8(raw_file)


def test_isp():
    for file_in in imgs.glob("*.raw"):
        # cmake, build, run
        print("\n===================================")
        print("Testing file:", file_in)
        img_xcore = raw_to_rgb_xcore(file_in)
        img_python = raw_to_rgb_python(file_in)
        met.append_metrics(img_xcore, img_python, file_in.stem, assert_metric=True)

    # print and test metrics
    met.print_metrics()


if __name__ == "__main__":
    test_isp()