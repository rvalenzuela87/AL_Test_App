# Serializers
This subpackage contains the modules responsible for serializing the records in memory prior
to saving them to a backup file. Currently, the app **only** supports serialization for 
**json** and **xml**.

This subpackage also contains the *Serial* interface which every serializer module implements.

The serializer modules are used by the *RecordsManager* singleton to serialize the list of
records it currently holds prior to writing it to a backup file.

The serializer modules **do not write to files**. They only offer the ability to serialize
python data to the correspondant backup type (json or xml) and loading the data contained in
the backup files to a python list.

The writing to the backup file is an exclusive responsability of the *RecordsManager* singleton.

## Design
This package implements the **Building Factory** design pattern and, as such, a SerializersBuilder 
class is provided under the module *serializers_builder*.

The Building Factory pattern was chosen to make the addition of new supported serialization types
easier. By importing the serializers_builder module, one has access to all of the app's available
serializers modules without knowing each one, individually.

The importing of serializer modules within the serializers_builder module is done dynamically so
there is no need to edit it once a new serializer module is added to the package.

It is encouraged to use the SerializersBuilder class to create instances of the different serializer
classes available.

## Add Custom Serializer
To add a custom serializer module, follow these steps.

Create the new serializer module under the *serializers* subpackage. The module must be named in the
following fashion:

*extension*_serial

For instance, *yaml*_serial.

The module must contain a variable named CLASS_NAME with the serializer's class' name. The latter
has to be named using camel-case, as so:

*Extension*Serial

For instance, *Yaml*Serial.

The exporter class must implement the *Serial* interface and provide definitions for its methods
*load*, and *serial*.

Lastly, the new supported extension has to be added to the configuration file (*config.json*) under
the app's *config* subdirectory.