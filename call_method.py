import gdb

#********************************************************************************

class CallMethod(gdb.Function):
    '''Call C++ method or function and return its return value.
    usage from GDB CLI:
    print $call_method(obj.methodName(...))
    usage from Pythone-code:
    CallMethod.invoke("obj.methodName(...)")'''

    def __init__(self):
        super(CallMethod, self).__init__("call_method")

    @classmethod
    def invoke(cls, argument):
        # Convenience function call_method(...) was called from GDB CLI
        retval = argument   # argument is already computed expr, argument is gdb.Value

        if isinstance(argument, str):
            # Convenience function CallMethod.invoke('...') was called from Python-code
            gdb.execute(f'set $tmp_retval = {argument}')
            retval = gdb.convenience_variable('tmp_retval')    # retval is gdb.Value

        return retval

CallMethod()
#********************************************************************************
