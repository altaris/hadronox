#!/usr/bin/env python3

import csv
import json
import optparse
import os

from relatorio.templates.opendocument import Template


def generateTarget(target, config):
    
    print("Generating target " + target["name"] + "... ", end = "")

    raw = []
    with open(target["input"]) as csvfile:
        raw = sorted(list(csv.DictReader(csvfile)), key = lambda x : sortKey(target, x))
    data = makeGroups(raw, target.get("groups", []))

    with open(target["output"], "wb") as outfile:
        template = Template(source = '', filepath = target["template"])
        doc = template.generate(data = data, meta = config["meta"],
                                language = config["language"])
        outfile.write(doc.render().getvalue())

    print("Done")


def sortKey(target, x):
    res = ""
    for k in target.get("sort", []):
        res += x[k]
    return res


def makeGroups(l, sepList):

    if len(sepList) == 0:
        return l

    else:

        sep = sepList[0]

        groupedDict = {}
        for r in l:
            val = r[sep["column"]]
            if val not in groupedDict.keys():
                groupedDict[val] = []
            groupedDict[val] += [r]

        data = []
        for k in sorted(groupedDict.keys()):
            group = {
                "value" : k,
                "data"  : makeGroups(groupedDict[k], sepList[1:])
            }
            additionalColumns = sep.get("additionalColumns", {})
            for a in additionalColumns.keys():
                group[a] = additionalColumns[a].get(k, "??") 
            data += [group]

        return { sep["column"] + "_list" : data }


if __name__ == "__main__":  
    
    parser = optparse.OptionParser()
    parser.add_option("-c", "--config", action = "store", dest = "config",
                      type = "string", help = "Configuration file")
    (options, args) = parser.parse_args()

    with open(options.config, 'r') as configfile:
        os.chdir(os.path.dirname(options.config))
        config = json.loads(configfile.read())
        for target in config["targets"]:
            generateTarget(target, config)