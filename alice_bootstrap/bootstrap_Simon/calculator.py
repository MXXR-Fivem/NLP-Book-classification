import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--add', nargs=2)
parser.add_argument('--sub', nargs=2)
parser.add_argument('--mult', nargs=2)
parser.add_argument('--div', nargs=2)
parser.add_argument('--int', action='store_true')
parser.add_argument('--float', action='store_true')

args = parser.parse_args()

if args.add:
    xargs = float(args.add[0])
    yargs = float(args.add[1])
    print(f'{xargs} + {yargs} = {xargs + yargs}')
elif args.sub:
    xargs = float(args.sub[0])
    yargs = float(args.sub[1])
    print(f'{xargs} - {yargs} = {xargs - yargs}')
elif args.mult:
    xargs = float(args.mult[0])
    yargs = float(args.mult[1])
    print(f'{xargs} * {yargs} = {xargs * yargs}')
elif args.div:
    xargs = float(args.div[0])
    yargs = float(args.div[1])
    if yargs == 0:
        print('Error: Division by zero is not allowed.')
    elif args.float and args.int:
        print('Warning: Both --int and --float provided. Using float division by default.')
    elif args.int:
        print(f'{xargs} // {yargs} = {xargs // yargs}')
    elif args.float:
        print(f'{xargs} / {yargs} = {xargs / yargs}')
    else:
        print('Info: No division mode specified. Using float division by default.')
        print(f'{xargs} // {yargs} = {xargs / yargs}')
