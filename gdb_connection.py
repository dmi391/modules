import gdb
import sys
import os.path

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from style import Style

#********************************************************************************

class BeginSession(gdb.Command):
    '''Start GDB actions.
    usage:
    begin elf-file'''

    def __init__ (self):
        super(BeginSession, self).__init__('begin', gdb.COMMAND_USER)

    @classmethod
    def invoke(cls, argument, from_tty):
        argv = gdb.string_to_argv(argument)
        if len(argv) != 1:
            raise gdb.GdbError('Command "begin" takes 1 argument. Try "help begin".')
        elf = argv[0]
        ip = 'localhost:3333'
        gdb.execute('set height unlimited')
        gdb.execute('set pagination off')
        gdb.execute(f'file {elf}')
        gdb.execute(f'target remote {ip}')
        gdb.execute('monitor reset halt')
        gdb.execute('load')
        #gdb.execute('set debug remote 1')

BeginSession()
#********************************************************************************

class Shutdown(gdb.Command):
    '''Finish GDB actions.
    usage:
    shutdown'''

    def __init__ (self):
        super(Shutdown, self).__init__('shutdown', gdb.COMMAND_USER)

    @classmethod
    def invoke(cls, argument, from_tty):
        argv = gdb.string_to_argv(argument)
        if len(argv) != 0:
            raise gdb.GdbError('Command "shutdown" takes no arguments. Try "help shutdown".')
        gdb.execute('monitor shutdown')
        gdb.execute('set confirm off')
        gdb.execute('quit')

Shutdown()
#********************************************************************************

class Output(gdb.Command):
    '''Output styled text message to GDB-console.
    usage:
    output message_type message_text
    message_type = "Ok:" | "Err:" | "Warn:" | "Info:"
    Example: output Warn: Something is wrong!'''

    def __init__ (self):
        super(Output, self).__init__('output', gdb.COMMAND_USER)

    @classmethod
    def invoke(cls, argument, from_tty):
        argv = gdb.string_to_argv(argument)
        if len(argv) < 2:
            raise gdb.GdbError('Command "output" takes 2 arguments. Try "help output".')
        msg_type = argv[0]
        msg_text = ' '.join(argv[1:])

        style = Style()
        if msg_type == 'Ok:':
            gdb.write(style.CBOLD + style.CGREEN + msg_text + style.CRESET + '\n')
        elif msg_type == 'Err:':
            gdb.write(style.CBOLD + style.CRED + msg_text + style.CRESET + '\n', gdb.STDERR)
            gdb.flush(gdb.STDERR)
        elif msg_type == 'Warn:':
            gdb.write(style.CBOLD + style.CYELLOW + msg_text + style.CRESET + '\n')
        elif msg_type == 'Info:':
            gdb.write(style.CBOLD + style.CWHITE + msg_text + style.CRESET + '\n')
        else:
            raise gdb.GdbError(f'Undefined output message type "{msg_type}". Try "help output".')
        gdb.flush()

Output()
#********************************************************************************
