#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin


def csv2areas(csv_file='areas.csv', \
              create_kinds=True, \
              skip_first=False, \
              prefix=None):

    ''' Creates Area objects from a CSV file.

    FORMAT:

    NAME | TYPE_SLUG | PARENT_ID '''

    from simple_locations.models import Area, AreaType

    try:
        fhandler = open(csv_file)
    except IOError:
        print "Unable to open file %s" % csv_file
        return None

    for line in fhandler:

        # skip header line?
        if skip_first:
            skip_first = False
            continue

        # retrieve raw data
        data = line.strip().split(',')
        name = data[0]
        type_slug = data[1]
        parent_id = data[2] or None
        parent = None
        try:
            name = name.decode('utf-8')
        except:
            pass

        # find or create AreaType
        try:
            kind = AreaType.objects.get(slug=type_slug)
        except AreaType.DoesNotExist:
            if create_kinds:
                kind = AreaType(slug=type_slug, name=type_slug.title())
                kind.save()
            else:
                raise

        # find parent
        if parent_id:
            parent = Area.objects.get(id=int(parent_id))

        print u"N: %(name)s - T: %(type)s - TS: %(type_slug)s - " \
               "P: %(parent)s - PID: %(parent_id)s" % \
               {'name': name, 'type': kind, 'type_slug': type_slug, \
                'parent': parent, 'parent_id': parent_id}

        area = Area(name=name, kind=kind, parent=parent)
        area.save()
