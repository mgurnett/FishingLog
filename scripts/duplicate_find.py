from catches.models import *
def get_list(vids):
    print (type(vids))
    urls_list = []
    for v in vids:
        urls_list.append (v.url)
    return urls_list

def find_dups(url_list):
    dup_list = [i for i, x in enumerate(url_list) if url_list.count(x) > 1]

    return (dup_list)

    
def run():
    vids = Video.objects.all()
    v_list = get_list(vids)
    # print (v_list)
    dups = find_dups(v_list)
    print (dups)
    for x in dups:
        print (vids[x].name)