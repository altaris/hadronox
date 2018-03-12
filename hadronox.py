#!/usr/bin/env python3

import csv
import json
import optparse
import os

from relatorio.templates.opendocument import Template


class AbstractTarget(dict):

    def make(self, metadatas):
        pass


class TemplateTarget(AbstractTarget):

    def make(self, metadatas):
        raw = []
        with open(self["input"]) as csvfile:
            raw = sorted(list(csv.DictReader(csvfile)),
                         key = lambda x : self._sortKey(x))
        data = self._makeGroups(raw, self.get("groups", []))
        with open(self["output"], "wb") as outfile:
            template = Template(source = '', filepath = self["template"])
            doc = template.generate(data = data, meta = metadatas)
            outfile.write(doc.render().getvalue())

    def _makeGroups(self, ungroupedData, sepList):
        if len(sepList) == 0:
            return ungroupedData
        else:
            sep = sepList[0]
            groupedDict = {}
            for r in ungroupedData:
                val = r[sep["column"]]
                if val not in groupedDict.keys():
                    groupedDict[val] = []
                groupedDict[val] += [r]
            data = []
            for k in sorted(groupedDict.keys()):
                group = {
                    "value" : k,
                    "data"  : self._makeGroups(groupedDict[k], sepList[1:])
                }
                additionalColumns = sep.get("additionalColumns", {})
                for a in additionalColumns.keys():
                    group[a] = additionalColumns[a].get(k, "??") 
                data += [group]
            return { sep["column"] + "_list" : data }

    def _sortKey(self, x):
        res = ""
        for k in self.get("sort", []):
            res += x[k]
        return res


class EmailTarget(AbstractTarget):

    def make(self, metadatas):
        print("Lololo")


targetTypes = {"email"    : EmailTarget,
               "template" : TemplateTarget}

if __name__ == "__main__":  
    
    parser = optparse.OptionParser()
    parser.add_option("-c", "--config", action = "store", dest = "config",
                      type = "string", help = "Configuration file")
    parser.add_option("-t", "--targets", action = "store", dest = "targets",
                      type = "string",
                      help = "Targets to execute, comma-separated",
                      default = "all")
    parser.add_option("-l", "--list-targets", action = "store_true",
                      dest = "listTargets", default = False,
                      help = "List available targets")
    (options, args) = parser.parse_args()

    with open(options.config, 'r') as configfile:
        os.chdir(os.path.dirname(options.config))
        config = json.loads(configfile.read())
        targetMap = {}
        for t in config["targets"]:
            targetMap[t["name"]] = targetTypes[t["type"]](t)
        if options.listTargets:
            print("Available targets: ", sorted(targetMap.keys()))
        else: 
            targets = []
            if options.targets == "all":
                targets = targetMap.keys()
            else:
                targets = options.targets.split(",")
            for k in targets:
                print("Making target " + k + " ... ", end = "")
                targetMap[k].make(config["meta"])
                print("Done")