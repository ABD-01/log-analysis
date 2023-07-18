import argparse

def Parser():
    parser = argparse.ArgumentParser(description="Log Analysis")
    parser.add_argument("-l", "--log_file", type=str, help="Path to log file", default="logs/log2.txt")
    parser.add_argument("-o", "--out_file", type=str, help="Path to output log file", default="analysedlogs/outlog.txt")
    parser.add_argument("-k", "--key_words", nargs='*', default=["FALCON", "WATCHDOG"])
    parser.add_argument("-t", "--topics", nargs='*', default=[])

    return parser