# Commands

## About
This subpackage contains all the command modules available in the app. It also contains
the *Command* interface implemented by every command module.

## Design
The necessity to expand the app's range of actions as well as the need to issue requests
by the main menu without necessarily knowing anything about the operation to execute, led
to the implementation of the behavioral design pattern *Command* to manage the app's 
functionality.

Each command module implements the *Command* interface (declared within the same subpackage).
By doing so, the app's main menu can execute every command in the same manner without the
need to diferentiate between a particular command and another.

The *Command* interface declares the *execute* method, for which each of the interface's 
implementations must provide a definition. This is the method responsible for the command's
actions.

The interface also declares the *set_params* method which is defined within the interface but
some implementations overwrite it with its own definition. This method takes positional and 
keyword arguments to set up the command's parameters values which are necessary for executing
the command. Therefore, the arguments the parameters have to be set before a call to the 
*execute* method is done.

Every implementation of the *Command* interface takes as first argument a *receiver* object
when instantiated. This object is used by the *execute* command and it is this object which
usually encapsulates the real functionality being encapsulated by the command.

Every basic command: add, delete, export, list, new, open and save take the app's 
*RecordsManager* singleton as their receiver.

## Design
This package implements the **Building Factory** design pattern and, as such, a CommandsBuilder 
class is provided under the module *commands_builder* inside this package.

The Building Factory pattern was chosen to make the addition of new command modules easier.
By importing the commands_builder module, one has access to all of the app's available
commands modules without knowing each one, individually.

The importing of command modules within the commands_builder module is done dynamically so
there is no need to edit it once a new command module is added to the package.

It is encouraged to use the CommandsBuilder class to create instances of the different command
classes available.

## Add Custom Command
To add a custom command, a new module must be created under the *commands* subpackage and must
be named with the following convention: 

*action*_command

For instance, *edit_command* or *shuffle_command*.

The new module must contain a variable named CLASS_NAME with the name of the module class which
name has to be in cammel-case, as so:

*Action*Command

For instance, *EditCommand* or *ShuffleCommand*.

The module's class has to implement the *Command* interface and a provide a definition for its
*execute* method.

By following those steps, the new command should be identifiable by the app.

## Basic Commands Overview

### New Command
Clears the list in memory and resets the *RecordsManager* singleton. The command ask the user
for confirmation before resetting the singleton.

This command takes no arguments.

### Open Command
Opens the backup file passed as argument or asks the user to specify one. This command takes
one positional or keyword argument.

If no filename is specified, the command will trigger a prompt operation asking the user to
specify a filename.

Bear in mind that the command **asks for the file name only, not its path**. All backup files are
looked for inside the *backup* directory by default. This was done for time constraints.

    >>: open 'backupFile.json'

The app supports xml and json file extensions, only. For expanding the range of supported extensions,
please refer to the *serializers* subpackage's *README* file.

### List Command
Displays the records currently in memory, i.e. loaded within the *RecordsManager* singleton. It 
supports *glob* like sintax for filtering. This command doesn's specify parameters' names explicitly
but it supports the same names as the *add* command.

If no arguments are specified, then all the records in memory will be displayed.

    >>: list

To display only the records filtered by *name* or those for which the *name* column matches a glob-like
expression, call the command with the keyword argument *name*:

    >>: list -name 'Raf*'

For more information on the list command, refer to the command's help.

### Add Command
Adds  new record to the list in memory. Supports positional and keyword arguments. Next, the list
of parameters long names and short names supported by the add command: 

+ name (n)
+ lastname (ln)
+ address (ad)
+ city (c)
+ phone (p)

It is required to submit an argument for each one of the command's parameters. Otherwise a prompt
operation will be triggered.

Next, an example of a call to the add command, with positional arguments, within the app.

    >>: add 'Rafael' 'Valenzuela' '10 Mulholland Drv' 'Hollywood' '123456'

A call to the add command, this time, with keyword arguments.

    >>: add -name 'Rafael' -lastname 'Valenzuela' -address '10 Mulholland Drv' -city 'Hollywood' -phone '123456'

For more information on the add command, refer to the command's help.

### Delete Command
Deletes a row from the list of records currently in memory. It takes one positional or keyword argument.

+ index (i)

To delete a specific row:

    >>: delete -index '4'

Or, with positional arguments:

    >>: delete '4'

### Save Command
Creates a backup file with the records in memory. Currently, the app only offers support for json and xml
files.

It takes a single positional or keyword argument.

+ filename (n)

This argument is necessary for the command's execution so, if no argument is provided, then a prompt operation
will be triggered, asking the user fo specify the backup file's name.

    >>: save -filename 'backupFile.json'

By default, all backup files are stored inside the *backup* directory under the app's main directory. This was done
for time constraints.

### Export Command
Creates either a txt or html file displaying the records currently in memory, formated in a human-readable way.
Currently, the app only supports exporting to txt or html. For more information on adding support for more types, 
please refer to the *exporters* subpackage's *README* file.

Supports a single positional or keyword argument.

+ filename (n)

By default, the created files are saved to the *reports* sub directory under the app's main directory. This was
done for time constraints.

    >>: export -filename 'report.html'
