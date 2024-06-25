from catches.models import Lake, DISTRICTS

def find_dist_num (dists, name):
    for d in dists:
        if name == d[1]:
            return d[0]
    return 60


def run():
    lakes = Lake.objects.all()
    dists = list(DISTRICTS)

    # print (lakes.count())
    # for l in lakes:
    #     if l.district:
    #         print (f"{l} + {l.district}")
    #         loc = dicts.index(l.district)
    #         # print (f"{l} + {l.district} + {loc}")
    # print (type (dists))
    # for d in dists:
    #     print (d[1])

    # for l in lakes:
    #     loc = find_dist_num(dists, l.district)
    #     print (f"{l} + {l.district} + {loc}")
    #     l.district_int = loc
    #     l.save()

    for l in lakes:
        print (l.dist_name)