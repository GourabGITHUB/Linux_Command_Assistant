from commands import get_cmd
from available_commands import cmd_details
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Linux command helper")
    parser.add_argument("context")
    args = parser.parse_args()
    context = args.context

    try:
        all_cmds = get_cmd(args.context)
    except ConnectionError as e:
        print(e)
        raise SystemExit(1)
    if not all_cmds:
        print("No commands found")
        raise SystemExit(1)
    print(cmd_details(all_cmds))
