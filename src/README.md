This is the app's *src* package with contains the app's must important modules and
packages:
+ **commands**.- This package contains the command modules used for editing or exporting the 
  records in memory.
+ **exporters**.- Contains the exporter modules responsible for writing the records in memory
  to a report-like file.
+ **serializers**.- Contains the serializer modules used to serialize records data to one of the
  app's supported backup types or loading the records from them.
+ **utils**.- Contains utility modules for commands and configuration as well as some validation
  functions.

## Records Manager
The records_manager module contains the singleton class RecordsManager. This is the class
responsible for keeping in memory the personal records and adding or deleting rows.

It was designed as a singleton class to keep data consistency and ease of access given that
every command within the app use it as their respective receiver object. For more information,
please refer to the *commands* subpackage's *README* file.