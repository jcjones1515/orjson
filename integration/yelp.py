#!/usr/bin/env python3
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys
from pathlib import Path

import orjson

# https://www.yelp.com/dataset, ~8.6GiB
FILES = {
    "yelp_academic_dataset_business.json",
    "yelp_academic_dataset_checkin.json",
    "yelp_academic_dataset_review.json",
    "yelp_academic_dataset_tip.json",
    "yelp_academic_dataset_user.json",
}

for filename in FILES:
    message = f"Processing {filename} ..."
    sys.stdout.buffer.write(f"{message}".encode("ascii"))
    count = 0
    data = Path(f"data/yelp/{filename}").read_bytes()
    for line in data.split(b"\n"):
        if not line:
            continue
        count += 1
        deserialized = orjson.loads(line)
        assert orjson.loads(orjson.dumps(deserialized)) == deserialized
        if count % 100 == 0:
            sys.stdout.buffer.write(f"\r{message} {count} entries".encode("ascii"))

    sys.stdout.buffer.write(f"\r{message} {count} entries\n".encode("ascii"))
