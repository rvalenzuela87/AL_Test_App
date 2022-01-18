# Exporters
This subpackage contains the modules responsible for creating the app's report files. There is one
exporter module for each report file extension supported. Currently, the app only supports exporting
to txt and html formats.

This subpackage also contains the *Exporter* interface which every exporter module implements.

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