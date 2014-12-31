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
from unittest import TestCase
from unittest import TestLoader


class SpanTest(TestCase):

    def test_from_set(self):
        from mete0r_gpl.parsers import Span
        self.assertEquals([Span(1)],
                          list(Span.from_set([1])))
        self.assertEquals([Span(1, 2)],
                          list(Span.from_set([1, 2])))
        self.assertEquals([Span(1, 2), Span(4)],
                          list(Span.from_set([1, 2, 4])))
        self.assertEquals([Span(1, 2), Span(4, 6)],
                          list(Span.from_set([1, 2, 4, 5, 6])))

    def test_str(self):
        from mete0r_gpl.parsers import Span
        self.assertEquals('3', str(Span(3)))
        self.assertEquals('3-4', str(Span(3, 4)))
        self.assertEquals('3-6', str(Span(3, 6)))


project_line = '   pyhwp : hwp file format parser in python'
copyright_line = '    Copyright (C) 2010-2012 mete0r  '
generic_line = '   abc   '
LF = '\n'


class ProjectTest(TestCase):

    def test_project_name(self):
        from mete0r_gpl.parsers import PROJECT_NAME
        self.assertEquals('pyhwp', PROJECT_NAME.parseString('pyhwp  :'))

    def test_project_desc(self):
        from mete0r_gpl.parsers import PROJECT_DESC
        expected = 'hwp file format parser in python'
        actual = PROJECT_DESC.parseString(
            '   hwp file format parser in python  ')
        self.assertEquals(expected, actual)

    def test_project_line_with_lf(self):
        from mete0r_gpl.parsers import Project
        from mete0r_gpl.parsers import PROJECT_LINE

        # ok with LF
        self.assertEquals(Project('pyhwp', 'hwp file format parser in python'),
                          PROJECT_LINE.parseString(project_line + LF))
        self.assertEquals(Project('pyhwp'),
                          PROJECT_LINE.parseString('   pyhwp   ' + LF))

    def test_project_line_without_lf(self):
        from mete0r_gpl.parsers import Project
        from mete0r_gpl.parsers import PROJECT_LINE

        # ok without LF
        self.assertEquals(Project('pyhwp', 'hwp file format parser in python'),
                          PROJECT_LINE.parseString(project_line))
        self.assertEquals(Project('pyhwp'),
                          PROJECT_LINE.parseString('   pyhwp   '))

    def test_project_line_parser_doesnt_consume_after_lf(self):
        from mete0r_gpl.parsers import PROJECT_LINE
        # make sure that the parser does not consume after LF
        from mete0r_gpl.Pysec import match
        self.assertEquals(' NEXTLINE',
                          ((PROJECT_LINE & match(' NEXTLINE')).parseString(
                              project_line + LF + ' NEXTLINE')))


class CopyrightTest(TestCase):

    def test_stringify_years(self):
        from mete0r_gpl.cli import stringify_years
        self.assertEquals('2011-2012',
                          stringify_years([2011, 2012]))
        self.assertEquals('2011-2013',
                          stringify_years([2011, 2012, 2013]))
        self.assertEquals('2011-2013,2015',
                          stringify_years([2011, 2012, 2013, 2015]))
        self.assertEquals('2009,2011-2013,2015',
                          stringify_years([2009, 2011, 2012, 2013, 2015]))

    def test_copyright(self):
        from mete0r_gpl.parsers import COPYRIGHT_SIGN
        self.assertTrue(COPYRIGHT_SIGN.parseString('Copyright (C)'))

        from mete0r_gpl.parsers import Span
        self.assertEquals('2010', str(Span(2010)))
        self.assertEquals('2010-2012', str(Span(2010, 2012)))

        from mete0r_gpl.parsers import YEAR_SPAN
        self.assertEquals(Span(2010, 2012),
                          YEAR_SPAN.parseString('2010-2012'))
        self.assertEquals(Span(2010, 2010),
                          YEAR_SPAN.parseString('2010'))

        from mete0r_gpl.parsers import YEARS
        self.assertEquals(set([2010]),
                          YEARS.parseString('2010'))
        self.assertEquals(set([2010, 2011]),
                          YEARS.parseString('2010,2011'))
        self.assertEquals(set([2010, 2011, 2012]),
                          YEARS.parseString('2010-2012'))
        self.assertEquals(set([2010, 2011, 2013, 2014, 2015, 2017]),
                          YEARS.parseString('2010,2011,2013-2015,2017'))

        from mete0r_gpl.parsers import AUTHOR_NAME
        self.assertEquals('Hello World',
                          AUTHOR_NAME.parseString('Hello World'))
        self.assertEquals('Hello World',
                          AUTHOR_NAME.parseString('Hello World <'))

        from mete0r_gpl.parsers import AUTHOR_EMAIL
        self.assertEquals('user@example.tld',
                          AUTHOR_EMAIL.parseString('<user@example.tld>'))

        from mete0r_gpl.parsers import Author
        from mete0r_gpl.parsers import AUTHOR
        self.assertEquals(Author('hong gil-dong', 'hongd@example.tld'),
                          AUTHOR.parseString(
                              'hong gil-dong <hongd@example.tld>'))
        self.assertEquals(Author('hong gil-dong'),
                          (AUTHOR.parseString('hong gil-dong')))
        self.assertEquals(Author(None, 'hongd@example.tld'),
                          (AUTHOR.parseString('<hongd@example.tld>')))

        from mete0r_gpl.parsers import AUTHORS
        self.assertEquals([Author('mete0r'),
                           Author('hong gil-dong', 'hongd@ex.tld')],
                          AUTHORS.parseString(
                              'mete0r, hong gil-dong <hongd@ex.tld>'))

        from mete0r_gpl.parsers import Copyright
        from mete0r_gpl.parsers import COPYRIGHT_LINE
        # ok with LF
        self.assertEquals(Copyright(set([2010, 2011, 2012]),
                                    [Author('mete0r')]),
                          (COPYRIGHT_LINE.parseString(copyright_line + LF)))

        # ok without LF
        self.assertEquals(Copyright(set([2010, 2011, 2012]),
                                    [Author('mete0r')]),
                          (COPYRIGHT_LINE.parseString(copyright_line)))

        # make sure that the parser does not consume after the LF
        from mete0r_gpl.Pysec import match
        self.assertEquals(' NEXTLINE',
                          (COPYRIGHT_LINE & match(' NEXTLINE')).parseString(
                              copyright_line + LF + ' NEXTLINE'))

    def test_generic_line(self):
        from mete0r_gpl.parsers import GENERIC_LINE
        self.assertEquals(generic_line,
                          GENERIC_LINE.parseString(generic_line + LF))


class LicenseTest(TestCase):
    def test_license(self):
        from mete0r_gpl.parsers import LICENSE

        text = '''#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# ''' + project_line + '''
# ''' + copyright_line + '''
#
#    This file is part of pyhwp project.
#
#   license text.

import unittest
'''
        print LICENSE.parseString(text)


def test_suite():
    return TestLoader().loadTestsFromName(__name__)
