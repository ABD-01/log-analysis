import argparse
import warnings
from tabulate import tabulate


def Parser(**kwargs):
    
    parser = argparse.ArgumentParser(description="Log Analysis", formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=32))
    parser.add_argument("-l", "--log-file", type=str, help="Path to log file", required=True)
    parser.add_argument("-o", "--out-file", type=str, help="Path to output log file")
    parser.add_argument("-k", "--keywords", nargs='*', default=[], metavar="eg: FALCON, WATCHDOG, etc", help="Provide Additional Keywords to be added")
    parser.add_argument("-t", "--topics", nargs='*', default=[], metavar="eg: telemetry", help="Specific topics to be looked up. (For MQTT Publish Msgs)")
    parser.add_argument("-r", "--regex", nargs="*", help="Raw string command or regex expression")
    parser.add_argument("-c", "--ignore-case", action="store_true", help="Ignore Match Case")
    parser.add_argument("-dp", '--disable-progresslive', action='store_true', help='Disable tqdm progress bar')
    parser.add_argument("--show-empty", action="store_true", help="Show empty values as well")

    parser.add_argument("--all", action="store_true", help="Show all available analysis")

    if kwargs:
        parser.add_argument("-m","--module", choices=kwargs.keys(), help="Choose the related module for log analysis")
        for k,v in kwargs.items():
            module_parser = parser.add_argument_group(k.title(), description=f"{k.title()} related log analysis")
            for subfunc in v:
                module_parser.add_argument(f"--{subfunc}", action="store_true", help=f"{subfunc.upper()} related log analysis")

    return parser

# For testing purposes only
if __name__ == "__main__":

    MODULE_SUBFUNCTIONS = {
    "network": ["tcp", "mqtt"],
    "sleep": ["ignition", "sleepcycle"]
    }

    parser = Parser(**MODULE_SUBFUNCTIONS)
    args = parser.parse_args()

    if args.regex:
        warning_msg = "Warning: --regex argument is not implemented yet. It will be added in a future update."
        warnings.warn(warning_msg, category=FutureWarning)

    # Create a table to display the parsed arguments
    table = []

    # Iterate over the parsed arguments and add them to the table
    for arg in vars(args):
        value = getattr(args, arg)
        arg_type = type(value).__name__
        table.append([arg, value, arg_type])

    print(tabulate(table, headers=["Argument", "Value", "Type"], tablefmt="fancy_grid"))