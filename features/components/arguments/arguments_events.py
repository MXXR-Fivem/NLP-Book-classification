import argparse
from collections.abc import Callable

import requests

from features.components.cache.get_cache import get_cache
from features.components.cache.set_cache import set_cache


def arguments_events(
    registered_args: argparse.Namespace, args_action: dict[str, dict[str, Callable | list]]
) -> None:
    """
    Add arguments event.

    ## Parameters
        **registered_args**: argparse Namespace of registered arguments

    ## Returns
        None
    """

    if not isinstance(registered_args, argparse.Namespace):
        raise TypeError('args parameter must be an argparse Namespace.')

    for arg, data in args_action.items():
        if not getattr(registered_args, arg):
            continue

        if data.get('sub_args', []) and 'book_id' in data['sub_args']:
            result = get_cache([
                getattr(registered_args, sub_arg)
                for sub_arg in data['sub_args']
                if 'id' in sub_arg
            ][0], arg)

            if result is not None:
                print(result, '[from cache]', sep='\n')
                return

        result = data['action'](
            *([getattr(registered_args, sub_arg) for sub_arg in data['sub_args']] if data.get('sub_args', []) else [])
        )

        if result and not isinstance(result, requests.Response):
            print(result)

            if data.get('sub_args', []) and data.get('use_cache', False):
                set_cache(
                    [
                        getattr(registered_args, sub_arg)
                        for sub_arg in data['sub_args']
                        if 'id' in sub_arg
                    ][0],
                    arg,
                    result
                )
                print('[saved in cache]')
    return
