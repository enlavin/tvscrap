# -*- coding: utf-8 -*-
# GNU General Public Licence (GPL)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.

# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA
__all__ = ['decode_torrent']

import itertools


def isdigit(c):
    return c >= ord(b'0') and c <= ord(b'9')


def parse_str(s):
    buf = bytearray()
    while True:
        c = next(s)
        while isdigit(c):
            buf.append(c)
            c = next(s)

        if c != ord(b':'):
            raise ValueError()

        length = int(buf.decode('utf-8'))
        buf = bytearray()
        for i in range(length):
            buf.append(next(s))

        try:
            string = buf.decode('utf-8')
        except UnicodeDecodeError:
            string = list(buf)
        return string


def parse_int(s):
    buf = bytearray()
    while True:
        c = next(s)
        while isdigit(c):
            buf.append(c)
            c = next(s)

        if c != ord(b'e'):
            raise ValueError()

        return int(buf.decode('utf-8'))


def parse_list(s):
    l = []
    while True:
        item = parse(s)
        if item is None:
            break
        l.append(item)

    #if next(s) != ord(b'e'):
    #    raise ValueError()

    return l


def parse_dict(s):
    d = {}

    while True:
        c = next(s)

        if c == ord('e'):
            break

        key = parse_str(itertools.chain([c], s))
        value = parse(s)

        d[key] = value

    return d


def parse(s):
    c = next(s)
    if c == ord(b'd'):
        return parse_dict(s)

    if c == ord(b'l'):
        return parse_list(s)

    if c == ord(b'i'):
        return parse_int(s)

    if isdigit(c):
        return parse_str(itertools.chain([c], s))

    if c == ord(b'e'):
        return None

    raise ValueError()


def decode_torrent(torrentfile):
    with open(torrentfile, 'rb') as tf:
        return parse(iter(tf.read()))
