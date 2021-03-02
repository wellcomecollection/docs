#!/usr/bin/env python

import os


if __name__ == '__main__':
    for f in sorted(os.listdir(".")):
        if os.path.isdir(f):
            try:
                readme_header = next(open(os.path.join(f, 'README.md')))
            except FileNotFoundError:
                continue

            title = readme_header.strip('#').strip()
            print(f'- [{title}](./{f}/README.md)')