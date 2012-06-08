#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin


def csv2areas(csv_file='areas.csv', \
              create_kinds=True, \
              skip_first=False, \
              prefix=None):

    ''' Creates Area objects from a CSV file.

    FORMAT:

    REGION | CERCLE | ARRONDISSEMENT | COMMUNE | VILLAGE | LAT | LONG '''

    from simple_locations.models import Area, AreaType, Point

    try:
        fhandler = open(csv_file)
    except IOError:
        print "Unable to open file %s" % csv_file
        return None

    # create types of areas
    ALL_KINDS = [
        ('country', u"Country"),
        ('region', u"Region"),
        ('cercle', u"Cercle"),
        ('arrondissement', u"Arrondissement"),
        ('commune', u"Commune"),
        ('village', u"Village")
    ]

    kinds = {}

    for kslug, kname in ALL_KINDS:
        try:
            kinds[kslug] = AreaType.objects.create(name=kname, slug=kslug)
        except AreaType.DoesNotExist: pass

    # add mali root Area
    try:
        mali = Area.objects.create(name=u"Mali", kind=kinds['country'])
    except:
        raise


    for line in fhandler:

        # skip header line?
        if skip_first:
            skip_first = False
            continue

        # retrieve raw data
        data = line.strip().split(',')
        clean_data = {}
        clean_data['region'] = data[0].title()
        clean_data['cercle'] = data[1].title()
        clean_data['arrondissement'] = data[2].title()
        clean_data['commune'] = data[3].title()
        clean_data['village'] = data[4].title()
        clean_data['lat'] = data[5] or None
        clean_data['lon'] = data[6] or None

        #print u"REGION:%s-CERCLE:%s-ARRDT:%s-COMMUNE:%s-VILLAGE:%s-LAT:%s-LON:%s" % (region_name, cercle_name, arrdt_name, commune_name, village_name, village_lat, village_lon)


        for kslug, kname in ALL_KINDS:
            if kslug == 'country':
                parent = mali
                continue

            try:
                area = Area.objects.get(kind=kinds[kslug], name=clean_data[kslug])
            except Area.DoesNotExist:
                if clean_data[kslug]:
                    area = Area.objects.create(name=clean_data[kslug], kind=kinds[kslug], parent=parent)

            parent = area

        if clean_data['lat'] and clean_data['lon']:
            point = Point.objects.create(latitude=clean_data['lat'], longitude=clean_data['lon'])
            area.location = point
            area.save()
        

        print u"AREA: %s - PARENT: %s" % (area, area.parent)

#    mali.code = 'mali'
#    mali.save()
