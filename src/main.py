# System Modules
import sys

# Arg check, we need atleast one argument!
assert len(sys.argv) > 1, "No argument provided!"


# Custom Modules
import cli, backend


@cli.add_command("backend", "start")
def _(target: str | None = ""):
    print(target)


cli.execute_command(sys.argv[1], sys.argv[2::])

