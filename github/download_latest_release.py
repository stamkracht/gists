"""
Download the latest source code release of a GitHub repository.

Usage:
$ python download_latest_release.py <REPO_URL> <DOWNLOAD_DIR>

e.g. `python download_latest_release.py https://github.com/facebook/rocksdb /build`

It prints the release's version number to stdout, which may be part of
the downloaded archive's root directory name.

Requires:
- Python >=3.6

Known limitations:
- Only works for repositories where a release has been explicitly created. It does not work on all tags.

This script was originally created to download RocksDB from a Dockerfile.
"""

import sys
from urllib.request import OpenerDirector, HTTPRedirectHandler, HTTPSHandler, urlretrieve


assert len(sys.argv) > 1, 'Please provide a repository URL, e.g. https://github.com/facebook/rocksdb'
assert len(sys.argv) > 2, 'Please provide a download directory, e.g. /build'
assert len(sys.argv) < 4, f'Please omit the unexpected arguments: {sys.argv[3:]}'
REPO_URL = sys.argv[1].rstrip('/')
DOWNLOAD_DIR = sys.argv[2].rstrip('/')

od = OpenerDirector()
od.add_handler(HTTPSHandler())
od.add_handler(HTTPRedirectHandler())

resp = od.open(f'{REPO_URL}/releases/latest')
tag_name = resp.headers['location'].split('/')[-1]

release_url = f'{REPO_URL}/archive/{tag_name}.tar.gz'
file_path, headers = urlretrieve(release_url, f'{DOWNLOAD_DIR}/latest.tar.gz')

print(f'{REPO_URL} {tag_name} was downloaded to {file_path}', file=sys.stderr)
print(tag_name.lstrip('v'))
