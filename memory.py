import gdb
import os.path

#********************************************************************************

class DumpMemory(gdb.Command):
    '''Dump memory data to a file.
    usage:
    dumpmem filename start_addr end_addr'''

    def __init__(self):
        super(DumpMemory, self).__init__("dumpmem", gdb.COMMAND_USER)

    @classmethod
    def invoke(cls, argument, from_tty):
        argv = gdb.string_to_argv(argument)
        len_argv = len(argv)
        if len_argv != 3:
            raise gdb.GdbError('Command "dumpmem" takes 3 arguments. Try "help dumpmem".')
        filename = argv[0]
        start_addr = argv[1]
        end_addr = argv[2]
        gdb.execute(f'dump memory {filename} {start_addr} {end_addr}')

DumpMemory()
#********************************************************************************

class AppendMemory(gdb.Command):
    '''Append memory data to a file.
    usage:
    appmem filename start_addr end_addr'''

    def __init__(self):
        super(AppendMemory, self).__init__("appmem", gdb.COMMAND_USER)

    @classmethod
    def invoke(cls, argument, from_tty):
        argv = gdb.string_to_argv(argument)
        len_argv = len(argv)
        if len_argv != 3:
            raise gdb.GdbError('Command "appmem" takes 3 arguments. Try "help appmem".')
        filename = argv[0]
        start_addr = argv[1]
        end_addr = argv[2]
        gdb.execute(f'append memory {filename} {start_addr} {end_addr}')

AppendMemory()
#********************************************************************************

class RestoreMemory(gdb.Command):
    '''Restore memory data from a file.
    usage:
    restoremem filename addr [start_offset] [end_offset]
    (start_offset - start file offset (offset from start of file), by default is 0.
    end_offset - end file offset, by default is lenght of file.
    start_offset and end_offset in bytes.)
    Original command: restore filename binary addr [start_offset] [end_offset]'''

    def __init__(self):
        super(RestoreMemory, self).__init__("restoremem", gdb.COMMAND_USER)

    @classmethod
    def invoke(cls, argument, from_tty):
        argv = gdb.string_to_argv(argument)
        len_argv = len(argv)
        if len_argv < 2 or len_argv > 4:
            raise gdb.GdbError('Command "restoremem" takes 2..4 arguments. Try "help restoremem".')
        filename = argv[0]
        addr = argv[1]
        start_offset = argv[2] if len_argv >= 3 else ''
        end_offset = argv[3] if len_argv == 4 else ''
        gdb.execute(f'restore {filename} binary {addr-start_offset} {start_offset} {end_offset}')

RestoreMemory()
#********************************************************************************

class ReadMemory(gdb.Command):
    '''Read memory data and store it to a file.
    usage:
    rmem filename addr length
    (addr taken as a symbol)'''

    def __init__(self):
        super(ReadMemory, self).__init__("rmem", gdb.COMMAND_USER)

    @classmethod
    def invoke(cls, argument, from_tty):
        argv = gdb.string_to_argv(argument)
        if len(argv) != 3:
            raise gdb.GdbError('Command "rmem" takes 3 arguments. Try "help rmem".')
        filename = argv[0]

        # Get address of taken symbol
        symbol, _ = gdb.lookup_symbol(argv[1])
        if symbol == None:
            raise gdb.GdbError(f'Symbol "{argv[1]}" is not found.')
        addr = symbol.value().address

        length = argv[2]

        # Get memory data
        inferior = gdb.selected_inferior()
        buf = inferior.read_memory(addr, length)    # memoryview object

        with open(filename, 'wb') as f:
            f.write(buf)

ReadMemory()
#********************************************************************************

class WriteMemory(gdb.Command):
    '''Write data to memory from a file.
    usage:
    wmem filename addr [length]
    (addr taken as a symbol)'''

    def __init__(self):
        super(WriteMemory, self).__init__("wmem", gdb.COMMAND_USER)

    @classmethod
    def invoke(cls, argument, from_tty):
        argv = gdb.string_to_argv(argument)
        len_argv = len(argv)
        if len_argv < 2 or len_argv > 3:
            raise gdb.GdbError('Command "wmem" takes 2..3 arguments. Try "help wmem".')
        filename = argv[0]

        # Get address of taken symbol
        symbol, _ = gdb.lookup_symbol(argv[1])
        if symbol == None:
            raise gdb.GdbError(f'Symbol "{argv[1]}" is not found.')
        addr = symbol.value().address

        length = int(argv[2]) if len_argv == 3 else os.path.getsize(filename)

        # Write to memory
        inferior = gdb.selected_inferior()
        with open(filename, 'rb') as f:
            buf = memoryview(f.read(length))
            inferior.write_memory(addr, buf, length)

WriteMemory()
#********************************************************************************
