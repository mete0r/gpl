# -*- coding: utf-8 -*-
#
#   mete0r.gpl : Manage GPL'ed source code files
#   Copyright (C) 2015 mete0r <mete0r@sarangbang.or.kr>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
'''
Usage:
    gpl [options] <files>...
    gpl -h | --help
    gpl --version

Options:
    -h --help               Show this screen
    --version               Show version
    --add-year=<year>       Add release year
    --set-author=<author>   Set author
'''
from __future__ import with_statement
import logging
import os
import shutil
import tempfile


logger = logging.getLogger(__name__)


def main():
    from docopt import docopt
    args = docopt(__doc__, version='0.0.0')

    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    license_modifiers = []

    add_year = args['--add-year']
    if add_year:
        year = add_year.strip()
        year = int(year)

        def add_year(license):
            years = license.copyright.years
            years.add(year)
            copyright = license.copyright.setYears(years)
            return license.setCopyright(copyright)
        license_modifiers.append(add_year)

    set_author = args['--set-author']
    if set_author:
        author = set_author.strip()
        from parsers import AUTHOR
        author = AUTHOR.parseString(author)

        def set_author(license):
            copyright = license.copyright
            copyright = copyright.setAuthors([author])
            return license.setCopyright(copyright)
        license_modifiers.append(set_author)

    filenames = args['<files>']

    for path in filenames:
        logger.info('filename: %s', path)
        try:
            process_file(path, license_modifiers)
        except Exception, e:
            logger.exception(e)


def process_file(path, license_modifiers):
    from .parsers import parse_file

    license = parse_file(path)
    for modifier in license_modifiers:
        license = modifier(license)

    fd, tmp_path = tempfile.mkstemp()
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(str(license))
    except:
        os.unlink(tmp_path)
        raise
    else:
        shutil.move(tmp_path, path)


def stringify_years(years):
    from .parsers import Span
    return ','.join(str(span) for span in Span.from_set(years))
