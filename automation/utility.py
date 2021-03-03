import inspect

def printDecorator(func):
    
    def wrapped(*args, **kwargs):
        callerFrame = inspect.getouterframes(inspect.currentframe(),2)
        caller = callerFrame[1][3]
        printArgs="()"
        if len(args)>1:
            printArgs = str(args[1:])

        logging.warning(caller + "\t->\t" + func.__name__ + printArgs)
        return func(*args, **kwargs)
    return wrapped

def decorateObject(obj, decorator):
    for method_name in dir(obj):
        if not method_name.startswith("_"):
            attr = getattr(obj, method_name)
            wrapped = decorator(attr)
            setattr(obj, method_name, wrapped)
