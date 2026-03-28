import argparse

operations = {
    'add': lambda x, y: x + y,
    'sub': lambda x, y: x - y,
    'mul': lambda x, y: x * y,
    'div': lambda x, y: x / y,
    'divdiv': lambda x, y: x // y,
}

operations_sign = {'add': '+', 'sub': '-', 'mul': '*', 'div': '/', 'divdiv': '/'}


def calculate(
    x: int | float,
    y: int | float,
    operator: str = 'add',
    float_format_div: bool = False,
    int_format_div: bool = True,
) -> int | float:
    """
    Compute the value of x 'operator' y.

    # Parameters
        **x**: x value (int or float)
        **y**: y value (int or float)
        **operator**: Operator (default +) (add, sub, mul, div)

    # Returns
        Result of the operation.
    """

    if (
        not x.replace('-', '').replace('.0', '').isdigit()
        or not y.replace('-', '').replace('.0', '').isdigit()
        or not isinstance(operator, str)
    ):
        raise TypeError
    elif not x or not y or operator not in operations:
        raise ValueError

    x = float(x)
    y = float(y)

    if x == 0.0 or y == 0.0:
        return 'Error : Division by zero is not allowed.'
    elif operator == 'div' and int_format_div and float_format_div:
        return f'Warning: Both --int and --float provided. Using float division by default.\n{x} {operations_sign[operator]} {y} = {float(operations[operator](x, y))}'
    elif operator == 'div' and int_format_div:
        return f'{x} {operations_sign[operator + operator]} {y} = {int(operations[operator + operator](x, y))}'
    elif operator == 'div' and (not int_format_div and not float_format_div):
        return f'Info: No division mode specified. Using float division by default.\n{x} {operations_sign[operator]} {y} = {float(operations[operator](x, y))}'

    return f'{x} {operations_sign[operator]} {y} = {float(operations[operator](x, y))}'


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)

group.add_argument('--add', action='store_true')
group.add_argument('--sub', action='store_true')
group.add_argument('--mul', action='store_true')
group.add_argument('--div', action='store_true')
parser.add_argument('--float', action='store_true')
parser.add_argument('--int', action='store_true')

parser.add_argument('numbers', nargs='*')

args = parser.parse_args()

if not args.add and not args.sub and not args.mul and not args.div:
    parser.error('one of the arguments --add --sub --mul --div is required')


def get_current_arg(args: argparse) -> list[list[str, bool]]:
    """
    Get current arguments sorted by usage.

    # Parameters
        **args**: List of arguments object

    # Returns
        The current arguments sorted by usage
    """
    return sorted(args, key=lambda x: x[1], reverse=True)[0][0]


current_arg = get_current_arg(args._get_kwargs())
if current_arg in operations:
    if len(args._get_kwargs()[0][1]) > 2:
        print('Error: You must provide exactly two numbers.')
    else:
        print(
            calculate(
                args.numbers[0],
                args.numbers[1],
                current_arg,
                (args.div and args.float),
                (args.div and args.int),
            )
        )
