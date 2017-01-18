import json
import psycopg2
from pprint import pprint

#   Retrieve taxonomy from comet
#
def getTaxonomy():
    cxn = psycopg2.connect('postgresql://localhost:5432/comet')
    cur = cxn.cursor()
    cur.execute("SELECT taxonomy_json FROM taxonomy")
    return cur.fetchone()[0]

#   Get children from
def getChildren(cat_path):
    children = []
    for category in categories.keys():
        if cat_path == category:
            pass
        elif cat_path in category:
            if '/' not in category[len(cat_path)+1:]:
                children.append(category)

    if children == []:
        return None
    else:
        return children


def createTree(category):
    new_dict = { "name" : categories[category]['label'],
                 "path": category }
    if getChildren(category):
        new_dict["children"] = [ createTree(child) for child in getChildren(category) ]
    return new_dict


if __name__ == "__main__":
    taxonomy = getTaxonomy()
    categories = taxonomy['categories']

    with open('taxonomy_tree.json', 'w') as json_file:
        json_file.write(json.dumps(createTree("Products"),
            sort_keys=False, indent=2, ensure_ascii=False).encode('utf8'))

    print "Taxonomy tree successfully created."
