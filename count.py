#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import re
import os

def parse_entities(s):
    s = s.replace('&ccirc;', 'ĉ')
    s = s.replace('&gcirc;', 'ĝ')
    s = s.replace('&jcirc;', 'ĵ')
    s = s.replace('&hcirc;', 'ĥ')
    s = s.replace('&scirc;', 'ŝ')
    s = s.replace('&Ccirc;', 'Ĉ')
    s = s.replace('&Gcirc;', 'Ĝ')
    s = s.replace('&Jcirc;', 'Ĵ')
    s = s.replace('&Hcirc;', 'Ĥ')
    s = s.replace('&Scirc;', 'Ŝ')
    s = s.replace('&ubreve;', 'ŭ')
    s = s.replace('&Ubreve;', 'Ŭ')
    return s

# Get all files.
filenames = glob.glob('revo/xml/*.xml')
slugs = {}

#filenames = filenames[:1000]
roots = {}
for i in range(1,19):
    roots[i] = {}

# Roots will be saved in a dictionary.
#
# Example:
# roots[6][protest] = {root: protest, slug: protest}
#
# Explanation:
# 6 = word length
# root = Esperanto root
# slug = filename in ReVo

for filename in filenames:
    f = open(filename, 'r')
    content = f.read()
    # Yes, RegExes are ugly, but after 2 hours dealing with various XML parsers decoding XML entities,
    # this was the best way to go.
    m = re.search('<rad>(.*)</rad>', content)
    f.close()
    if not m:
        continue
    root = m.group(1)
    if len(root) < 2:
        continue
    if len(root) > 18:
        continue
    root = root.lower()
    root = parse_entities(root)

    basename = os.path.basename(filename)
    slug,extension = basename.split('.')
    slugs[root] = slug

    roots[len(root)][root] = {
        'slug': slug,
        'root': root
    }



#print roots
#exit()
min = 2
max = 18
#length = 3
clashes = {}

# For all word lengths.
for length in range(min+1,max+1):
    #print length
    # The middle wanders through the word length from left to right.
    for middle in range(1, length):
        left_from    = 0
        left_to      = middle-1
        right_from   = middle
        right_to     = length-1
        left_length  = left_to - left_from + 1
        right_length = right_to - right_from + 1

        #print left_length, right_length

        for left_root in roots[left_length].keys():
            for right_root in roots[right_length].keys():
                # Put new root together
                # and test if it exists.
                clash = left_root + right_root
                if clash in roots[length]:
                    #print left_root, right_root
                    if not clash in clashes:
                        clashes[clash] = []
                    clashes[clash].append((roots[left_length][left_root], roots[right_length][right_root]))

# Output clashes.
print '<ol>'
for clash in clashes.keys():
    print '<li>'
    slug = roots[len(clash)][clash]['slug']
    print '<a href="http://www.reta-vortaro.de/revo/art/' + slug + '.html">'
    print clash
    print '</a>'
    print '<ol>'
    for pair in clashes[clash]:
        print '<li>'
        slug = pair[0]['slug']
        root = pair[0]['root']
        print '<a href="http://www.reta-vortaro.de/revo/art/' + slug + '.html">'
        print root
        print '</a>'
        slug = pair[1]['slug']
        root = pair[1]['root']
        print '<a href="http://www.reta-vortaro.de/revo/art/' + slug + '.html">'
        print root
        print '</a>'
        print '</li>'
    print '</ol>'
    print '</li>'
print '</ol>'


