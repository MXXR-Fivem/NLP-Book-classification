import argparse
from collections.abc import Callable


def argument_validation(
    parser: argparse.ArgumentParser,
    args: argparse.Namespace,
    args_action: dict[str, dict[str, Callable | list]],
) -> None:
    """
    Validate combinations of arguments.

    ## Parameters
        **parser**: Arguments parser
        **args**: Arguments Namespace

    ## Returns
        None
    """

    selected_commands = [cmd for cmd in args_action if getattr(args, cmd)]

    if len(selected_commands) != 1:
        parser.error('You must specify exactly one command.')

    command = selected_commands[0]

    if not args_action[command].get('sub_args', []):
        return

    command_sub_args = args_action[command]['sub_args']

    if 'book_id' in command_sub_args:
        if args.book_id is None:
            parser.error(f'--{command} requires book_id.')

        bad_flags = []
        for flag in args._get_kwargs():
            if flag[1] and flag[0] not in command_sub_args and flag[0] not in args_action:
                bad_flags.append(flag[0])

        allowed_commands = [
            cmd for cmd, data in args_action.items() if set(bad_flags).issubset(data.get('sub_args', []))
        ]

        if bad_flags:
            parser.error(
                f'{" / ".join(bad_flags)} can only be used with --{" --".join(allowed_commands)}'
            )
    else:
        found = 0
        for i, expected_arg in enumerate(command_sub_args):
            if (
                getattr(args, expected_arg) is None
                and i == len(command_sub_args) - 1
                and found == 0
            ):
                parser.error(f'--{command} requires at least {" or ".join(command_sub_args)}.')
            elif getattr(args, expected_arg) is not None:
                found += 1
