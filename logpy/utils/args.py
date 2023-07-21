import argparse
import warnings
from tabulate import tabulate

def Parser():
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument("-l", "--log-file", type=str, help="Path to log file", required=True)
    parent_parser.add_argument("-o", "--out-file", type=str, help="Path to output log file")
    parent_parser.add_argument("-k", "--keywords", nargs='*', default=[])
    parent_parser.add_argument("-t", "--topics", nargs='*', default=[])
    parent_parser.add_argument("-r", "--regex", nargs=argparse.REMAINDER, help="Raw string command or regex expression")
    parent_parser.add_argument("-c", "--ignore-case", action="store_true", help="Ignore Match Case")
    parent_parser.add_argument("-dp", '--disable-progresslive', action='store_true', help='Disable tqdm progress bar')

    # main parser
    parser = argparse.ArgumentParser(description="Log Analysis", parents=[parent_parser])
    parser.add_argument("--all", action="store_true", help="Show all available analysis")
    subparsers = parser.add_subparsers(dest="module", help="Choose the related module for log analysis", title="Module")

    network_parser = subparsers.add_parser("network", parents=[parent_parser], description="Network related log analysis")
    network_parser.add_argument("--tcp", action="store_true", help="TCP related log analysis")
    network_parser.add_argument("--mqtt", action="store_true", help="MQTT related log analysis")

    sleep_parser = subparsers.add_parser("sleep", parents=[parent_parser], description="Sleep related log analysis")
    sleep_parser.add_argument("--wake", action="store_true", help="Get wake up related log analysis")
    sleep_parser.add_argument("--sleep-cycle", action="store_true", help="Get sleep cycle related log analysis")

    return parser

if __name__ == "__main__":
    parser = Parser()
    args = parser.parse_args()

    if args.regex:
        warning_msg = "Warning: --regex argument is not implemented yet. It will be added in a future update."
        warnings.warn(warning_msg, category=FutureWarning)

    # Create a table to display the parsed arguments
    table = []

    # Add the operation to the table
    if hasattr(args, "module"):
        table.append(["module", args.module])

    # Iterate over the parsed arguments and add them to the table
    for arg in vars(args):
        value = getattr(args, arg)
        arg_type = type(value).__name__
        table.append([arg, value, arg_type])

    print(tabulate(table, headers=["Argument", "Value", "Type"], tablefmt="fancy_grid"))
