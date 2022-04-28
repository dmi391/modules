
# Own GDB-commands and GDB-functions

----

GDB doc:

* 23.2.2.20 Commands In Python;
* 23.2.2.22 Writing new convenience functions

To get help for any command call `help <command>` right in GDB-console.

Own GDB-commands and GDB-functions are implemented with using Python-GDB-API.
GDB-commands and GDB-functions are available for use from GDB CLI and from python-GDB script.
Each GDB-command and GDB-function is implemented as separate python-class. To use this commands it is necessary to import in python code class that implements required command.

Using in GDB-console as usual. Example: `command arg1 arg2`.
To use in python code call `method .invoke(...)` of class that implements command. Arguments of method `.invoke(cls, argument, from_tty)`: `argument<str>` - is arguments of command; `from_tty<bool>` - should be False when call from python code. Example: `CommandClass.invoke('arg1, arg2', False)`.


## Module gdb_connection

**Command 'begin' - class BeginSession:**  
Perform start GDB actions.  
Arguments: path-to-elf-file  
GDB CLI: `begin path-to-elf-file`  
Python-code: `BeginSession.invoke('path-to-elf-file', False)`

**Command 'shutdown' - class Shutdown:**  
Perform GDB actions to finish GDB session.  
usage: `shutdown`  
No arguments.  

**Command 'output' - class Output:**  
Output styled text message to GDB-console.  
usage: `output message_type message_text`  
message_type = "Ok:" | "Err:" | "Warn:" | "Info:"  
Example: `output Warn: Something is wrong!`


## Module memory

**Command 'dumpmem' - class DumpMemory:**  
Dump memory data to a file (wrap over GDB-command 'dump memory').  
usage: `dumpmem filename start_addr end_addr`

**Command 'appmem' - class AppendMemory:**  
Append memory data to a file (wrap over GDB-command 'append memory').  
usage: `appmem filename start_addr end_addr`

**Command 'restoremem' - class RestoreMemory:**  
Restore memory data from a file (wrap over GDB-command 'restore').  
usage: `restoremem filename addr [start_offset] [end_offset]`

**Command 'rmem' - class ReadMemory:**  
Read memory data and store it to a file.  
usage: `rmem filename addr length`  
(addr taken as a symbol)

**Command 'wmem' - class WriteMemory:**  
Write data to memory from a file.  
usage: `wmem filename addr [length]`  
(addr taken as a symbol)


## Module call_method

**Convenience function $call_method(...) - class CallMethod:**  
Call C++ method or function and return its return value. Expression taken as argument.  
GDB CLI: `print $call_method(obj.methodName(...))`  
Python-code: `CallMethod.invoke('obj.methodName(...)')`


## Module profile

**Command 'prof' - classes EndPoint and StartPoint:**  
Profiling of function/method using gdb.FinishBreakpoint after gdb.Breakpoint.  
(Similarly with [Python interpreter in GNU Debugger](https://www.pythonsheets.com/appendix/python-gdb.html)). It works for object methods and for static methods.  
GDB CLI: `prof methodName`  
Python-code: `Profile.invoke('methodName', False)`

