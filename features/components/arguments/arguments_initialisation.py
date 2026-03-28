import argparse
from collections.abc import Callable

from .arguments_validation import argument_validation


def arguments_initialisation(
    args_action: dict[str, dict[str, Callable | list]],
) -> argparse.Namespace:
    """
    Get the Namespace of registered arguments.

    ## Parameters
        None

    ## Returns
        Argparse Namespace of registered args
    """

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    registered_sub_args = []

    for arg, data in args_action.items():
        group.add_argument(f'--{arg}', action='store_true')

        for opt_arg, arg_type in data.get('optional_args', []):
            parser.add_argument(opt_arg, type=arg_type)

        for sub_arg in data.get('sub_args', []):
            if sub_arg not in registered_sub_args and ('--' + sub_arg) not in [
                arg[0] for arg in data.get('optional_args', [])
            ]:
                parser.add_argument(sub_arg, type=int, nargs='?')
                registered_sub_args.append(sub_arg)

    args = parser.parse_args()
    argument_validation(parser, args, args_action)

    return parser.parse_args()
