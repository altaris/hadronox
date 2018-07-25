hadronox
========

I can't be bothered to write a comprehensive understandable documentation. For now, there's a brief description of the configuration file syntax, and an example. Hopefully I'll be able to make this thing work next time I need it.

# Command line arguments

Just type:
```
hadronox.py --help
```

# Configuration file

It is written in JSON. All paths are relative to the configuration file unless stated otherwise.

## `meta`

Contains all metadata.

## `targets`

All paths are relative to the config file.

* `name`: Name of the target.
* `type`: See below.

### Target type `template`

* `groups`: List of groups descriptors, see after.
* `input`: Path to the input `csv` file.
* `output`: Path to the output document.
* `sort`: List of sort columns (of the input `csv` file).
* `template`: Path to template file.

Group descriptors: A `csv` file is a list of row. This list can be divided into disjoint sublist according to the specifications of a group descriptor.

* `additionalColumns`: Each group can have additional columns whose value is defined by that of the separating column. See example.
* `column`: Name of the separating column, i.e. that from which the rows are regrouped by value.

### Target type `email`

For this target, `hadronox` establishes a TLS (normal passowrd) connection to a specified SMTP server. The password is asked upon execution.

* `email`: Name of the `csv` column where the email adress of the receipients is stored.
* `from`: Email address of the sender.
* `host`: Address of the host SPTM server.
* `input`: Path to input `csv` file.
* `port`: Port.
* `subject`: Subject of the email.
* `template`: Path to template email.
* `username`: Username to log in to host SMTP server.
