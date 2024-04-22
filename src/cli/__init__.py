_available_commands: dict = {}

def add_command(name: str, pre_requisite_arg: str | None = ""):
    def wrapper(function: (...)):
        global _available_commands
        _available_commands[pre_requisite_arg + name] = function
    return wrapper


def execute_command(name: str, args: list[str]):
    _arg_len = len(args)

    _pre_name = (_arg_len > 0 and args[0] or "") + name
    _pre_args = (_arg_len > 1 and args[1::]) or []

    _pre_result = _available_commands.get(_pre_name)

    _result = _available_commands.get(name)

    if callable(_pre_result):
        _pre_result(*_pre_args)
    elif callable(_result):
        _result(*args)
    else:
        raise Exception("Erhmm, what the scallop?")