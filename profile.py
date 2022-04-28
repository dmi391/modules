import gdb

#********************************************************************************

class EndPoint(gdb.FinishBreakpoint):
    def __init__(self, breakpoint, *a, **kw):
        super().__init__(*a, **kw)
        self.silent = True
        self.breakpoint = breakpoint

    def stop(self):
        # normal finish
        end = int(gdb.parse_and_eval('$mcycle'))
        start, out = self.breakpoint.stack.pop()
        diff = end - start
        print(out.strip())
        print(f"\tCost in mcycle: {diff}")
        return False

class StartPoint(gdb.Breakpoint):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.silent = True
        self.stack = []

    def stop(self):
        start = int(gdb.parse_and_eval('$mcycle'))
        # start, end, diff
        frame = gdb.selected_frame()    # == gdb.newest_frame()
        sym_and_line = frame.find_sal()
        func = frame.function().name
        filename = sym_and_line.symtab.filename
        line = sym_and_line.line
        block = frame.block()

        # older (upper) frame
        of = frame.older()
        sym_and_line = of.find_sal()
        of_func = of.function().name
        of_filename = sym_and_line.symtab.filename
        of_line = sym_and_line.line

        args = []
        for s in block:
            if not s.is_argument:
                continue
            name = s.name
            typ = s.type
            val = s.value(frame)
            args.append(f"{name}: {val} [{typ}]")

        # format
        out = ""
        out += f"{func} @ {filename}:{line}\n"
        out += f"\t\t> Called from {of_func} @ {of_filename}:{of_line}\n"
        for a in args:
            out += f"\t{a}\n"

        # append current status to a breakpoint stack
        self.stack.append((start, out))
        EndPoint(self, internal=True)   # Pass StartPoint-object as self to EndPoint(...)
        return False

class Profile(gdb.Command):
    '''Simple profiling.
    usage:
    prof function/method name'''

    def __init__(self):
        super().__init__("prof", gdb.COMMAND_USER)
    
    @classmethod
    def invoke(cls, args, tty):
        StartPoint(args)

Profile()
#********************************************************************************
