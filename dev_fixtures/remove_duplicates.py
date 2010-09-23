#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import simplejson
import pprint

JSON_FILE  = 'locations_mali.json'


j = simplejson.loads(open(JSON_FILE).read())

models = set()
pairs = {}

for obj in j:
    try:
        code = obj['fields']['code']
        kind = obj['fields']['kind']
        pairs[(code, kind)] = pairs.get((code, kind), 0) + 1
    except KeyError:
        pass
        
duplicates =  dict((key, []) for key, value in pairs.iteritems() if value > 1)

for obj in j:

    try:
        code = obj['fields']['code']
        kind = obj['fields']['kind']
        if (code, kind) in duplicates:
            duplicates[(code, kind)].append(obj)
    except KeyError:
        pass
        
for title, objs in duplicates.iteritems():
    print "=======", title, "========="
    for obj in objs:
        pprint.pprint(obj)

uniques = open("mali_fixture_truncated.json", 'w')
count = 0
for i, obj in enumerate(list(j)):
    try:
        code = obj['fields']['code']
        kind = obj['fields']['kind']
        if (code, kind) in duplicates:
            j.pop(i - count)
            count += 1
    except KeyError:
        pass
 
simplejson.dump(j, uniques)
uniques.close()


#[('<Area: Commune of Faraba>', 4), ('<Area: Commune of Somo>', 4), ('<Area: Commune of Tilemsi>', 4), ('<Area: Commune of Kapala>', 4), ('<Area: Commune of Niamana>', 4), ('<Area: Commune of Bougoula>', 4), ('<Area: Commune of Farako>', 4), ('<Area: Commune of Bamba>', 4), (u'<Area: Commune of Di\xe9dougou>', 4), ('<Area: Commune of Koula>', 4), ('<Area: Commune of Benkadi>', 4), ('<Area: Commune of Baye>', 4), ('<Area: Commune of Dogofry>', 4)]

