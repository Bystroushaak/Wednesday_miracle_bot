#! /usr/bin/env python3
import os
import json
import shutil
from contextlib import contextmanager


@contextmanager
def in_tmp_dir(dirname):
    os.makedirs(dirname, exist_ok=True)
    os.chdir(dirname)

    yield

    os.chdir("..")
    shutil.rmtree(dirname)


def download_wednesday_dataset():
    command = r"""youtube-dl "https://www.youtube.com/playlist?list=PLy3-VH7qrUZ5IVq_lISnoccVIYZCMvi-8" --write-info-json --skip-download -o '%(playlist_index)s.%(ext)s'"""

    with in_tmp_dir("json_data"):
        os.system(command)

        for fn in sorted(os.listdir(".")):
            with open(fn) as f:
                data = json.loads(f.read())
                yield "https://www.youtube.com/watch?v=" + data["id"]


with open("wednesdays.json", "wt") as f:
    data = json.dumps(list(download_wednesday_dataset()), indent=4)
    f.write(data)
    print(data)
