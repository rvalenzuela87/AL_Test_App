# Exporters
This subpackage contains the modules responsible for creating the app's report files. There is one
exporter module for each report file extension supported. Currently, the app only supports exporting
to txt and html formats.

This subpackage also contains the *Exporter* interface which every exporter module implements.

## Design
This package implements the **Building Factory** design pattern and, as such, a ExportersBuilder 
class is provided under the module *exporters_builder*.

The Building Factory pattern was chosen to make the addition of new supported export file types
easier. By importing the exporters_builder module, one has access to all of the app's available
exporter modules without knowing each one, individually.

The importing of exporter modules within the exporters_builder module is done dynamically so
there is no need to edit it once a new exporter module is added to the package.

It is encouraged to use the ExportersBuilder class to create instances of the different exporter
classes available.

## Add Custom Exporter
To add a custom exporter module, follow these steps.

Create the new exporter module under the *exporters* subpackage. The module must be named in the
following fashion:

*extension*_exporter

For instance, *csv*_exporter or *pdf*_exporter.

The module must contain a variable named CLASS_NAME with the exporter's class' name. The latter
has to be named using camel-case, as so:

*Extension*Exporter

For instance, *CSV*Exporter or *PDF*Exporter.

The exporter class must implement the *Exporter* interface and provide definitions for its methods
*set_file_name*, *format_data* and *export*.

Lastly, the new supported extension has to be added to the configuration file (*config.json*) under
the app's *config* subdirectory.