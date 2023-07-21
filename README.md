# LogPy - Your Log Analysis Tool

![License](https://img.shields.io/github/license/your_username/logpy)

## Overview

LogPy is a command-line tool designed for log analysis. It allows you to parse log files, extract relevant information, and generate useful insights from the log data.

## Features

- Analyze network-related logs, including TCP connections, MQTT messages, and more.
- Perform sleep-related log analysis, such as tracking sleep cycles, wake events, etc.
- Use regular expressions for custom log parsing and analysis.
- Easily specify log files, output files, keywords, and topics through command-line arguments.
- Toggle options to control the analysis process, such as ignoring case or disabling the progress bar.

## Installation

To install LogPy, you can use the distributable package provided by the developer. Follow the instructions below to install LogPy on your system:

```bash
pip install logpy-1.0-py3-none-any.whl
```

Replace `logpy-1.0-py3-none-any.whl` with the correct filename of the package.

## Usage

After installing LogPy, you can use it from the command line as follows:

```bash
logpy --help
```

This will display the available command-line options and usage instructions.

## Examples

Here are some examples of how to use LogPy:

- Analyze network-related logs with TCP and MQTT analysis:
```bash
logpy network --tcp --mqtt -l /path/to/logfile.txt
```

- Perform sleep-related log analysis with wake and sleep cycle analysis:
```bash
logpy sleep --wake --sleep-cycle -l /path/to/logfile.txt
```

- Perform analysis of all modules:
```bash
logpy --all -l /path/to/logfile.txt
```

<!-- - Analyze logs using custom regular expressions:
```bash
logpy --regex pubresponse "\+QMTPUB: (\d),(\d)" -l /path/to/logfile.txt
``` -->


## Contact

If you have any questions or need support, you can reach out to the developer at muhammed.shaikh@accoladeelectronics.com.

Happy log analysis with LogPy! 🚀