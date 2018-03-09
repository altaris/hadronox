hadronox
========

I can't be bothered to write a comprehensive understandable documentation. For now, there's a brief description of the configuration file syntax, and an example. Hopefully i'll be able to make this thing work next time i need it.

# Configuration file

The configuration file tells `hadronox` wtf it should do:
```
    hadronox -c path/to/stuff/config.json
```

It is written in JSON.

## `meta`

Contains all metadata.

## `language`

Translations.

## `targets`

All paths are relative to the config file.

* `name`: For log purposes.
* `template`: Path to template file.
* `input`: Path to the input `csv` file.
* `output`: Path to the output document.
* `sort`: List of sort columns (of the input `csv` file).
* `groups`: List of groups descriptors.

### Group descriptors

A `csv` file is a list of row. This list can be divided into disjoint sublist according to the specifications of a group descriptor.

* `column`: Name of the separating column, i.e. that from which the rows are regrouped by value.
* `additionalColumns`: Each group can have additional columns whose value is defined by that of the separating column. See example.
