# Personal Records App

## About
This tool allows the user to store a person's information such as his\her name, last name, 
address, city and phone number. This information is stored in a list in memory but can
be saved to an external json or xml file which are the only types currently supported.

## Design
The app follows the behavioral design pattern *Command* to encapsulate each of its available
operations such as *adding a new record*, *backup saving*, etc.

All these *command modules* are stored inside the app's *commands* subpackage. Please refer to 
the latter's *README* file for more information about writing new command modules.

For the management of records in memory, the app follows the creational design pattern *Singleton*
to ensure consistency of data throught the app's many modules.

The records in memory are stored inside an instance of the singleton class *records_manager.RecordsManager*.

## Usage
To run the app execute the *main.py* file, located in the app's *src* package, in a command
line terminal.

    python C:\AL_Test_App\src\main.py

A menu will be displayed with 7 options available: New, Open, List, Add, Delete, Save, Export 
and Exit. Each of this options represents a command and can be called using positional as well 
as keyword arguments. In case of not providing any, a prompt loop will start to ask the necessary
information for executing the command. To learn more about each individual command, please
refer to the *commands* subpackage's *README* file within the *src* package.

Positional arguments are stated as the following:

    >>: add 'Rafael' 'Valenzuela' '10 Mulholland Drv' 'Hollywood' '123456'

Keyword arguments are stated as the following:

    >>: add -name 'Rafael' -lastname 'Valenzuela' -address '10 Mulholland Drv' -city 'Hollywood' -phone '123456'

It is important to note that one can run the menu options using the latter's full name or the
shortcut shown in parenthesis in the menu.

    >>: a 'Rafael' 'Valenzuela' '10 Mulholland Drv' 'Hollywood' '123456'

If a backup json or xml file already exists, the app can be run with the file's name as argument
for instant loading of the stored data.

    python C:\AL_Test_App\src\main.py backupFile.json

For more information about the creation of backup files, please refer to the *Save Command* section 
in the *commands* subpackage's *README* file.

## Test
Some test cases are provided under the *tests* subpackage under the app's root package. For time constraints,
not all of the app's functionality has a test case.