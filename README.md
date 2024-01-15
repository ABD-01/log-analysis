# LogPy - Your Log Analysis Tool

[![License: GPL v2](https://img.shields.io/badge/License-GPL_v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)

- [LogPy - Your Log Analysis Tool](#logpy---your-log-analysis-tool)
  * [Overview](#overview)
  * [Notes](#notes)
  * [Features](#features)
  * [Installation](#installation)
  * [Usage](#usage)
  * [Examples](#examples)
  * [Contact](#contact)

<!-- <small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small> -->

## Overview

LogPy is a command-line tool designed for log analysis. It allows you to parse log files, extract relevant information, and generate useful insights from the log data.

## Notes
[Notes.md](Notes.md) contains my notes on Python's Multi-Threading, using PySide6 for GUI tools, creating pythnon package, and more.   

## Features

- Analyze network-related logs, including TCP connections, MQTT messages, and more.
- Perform sleep-related log analysis, such as tracking sleep cycles, wake events, etc.
- Use regular expressions for custom log parsing and analysis.
- Easily specify log files, output files, keywords, and topics through command-line arguments.
- Toggle options to control the analysis process, such as ignoring case or disabling the progress bar.

## Installation

To install LogPy, you can use the distributable package provided by the developer. Follow the instructions below to install LogPy on your system:

```
pip install logpy-1.2.1-py3-none-any.whl
```

Replace `logpy-1.2.1-py3-none-any.whl` with the correct filename of the package.

## Usage

After installing LogPy, you can use it from the command line as follows:

```
>> logpy --help

usage: logpy [-h] -l LOG_FILE [-o OUT_FILE] [-k [eg: FALCON, WATCHDOG, etc ...]] [-t [eg: telemetry ...]]
             [-r [REGEX ...]] [-c] [-dp] [--show-empty] [--all] [-m {network,sleep,gps,can}] [--tcp] [--mqtt]
             [--netswitching] [--pdpdeact] [--netregistration] [--ignition] [--sleepcycle] [--gps] [--can] [-v]

Log Analysis Command Line Tool.
For GUI based tool use: `logpy-gui`

options:
  -h, --help                    show this help message and exit
  -l LOG_FILE, --log-file LOG_FILE
                                Path to log file
  -o OUT_FILE, --out-file OUT_FILE
                                Path to output log file
  -k [eg: FALCON, WATCHDOG, etc ...], --keywords [eg: FALCON, WATCHDOG, etc ...]
                                Provide Additional Keywords to be added
  -t [eg: telemetry ...], --topics [eg: telemetry ...]
                                Specific topics to be looked up. (For MQTT Publish Msgs)
  -r [REGEX ...], --regex [REGEX ...]
                                Raw string command or regex expression
  -c, --ignore-case             Ignore Match Case
  -dp, --disable-progresslive   Disable tqdm progress bar
  --show-empty                  Show empty values as well
  --all                         Show all available analysis
  -m {network,sleep,gps,can}, --module {network,sleep,gps,can}
                                Choose the related module for log analysis
  -v, --version                 Show version

Network:
  Network related log analysis

  --tcp                         TCP related log analysis
  --mqtt                        MQTT related log analysis
  --netswitching                NETSWITCHING related log analysis
  --pdpdeact                    PDPDEACT related log analysis
  --netregistration             NETREGISTRATION related log analysis

Sleep:
  Sleep related log analysis

  --ignition                    IGNITION related log analysis
  --sleepcycle                  SLEEPCYCLE related log analysis

Gps:
  Gps related log analysis

  --gps                         GPS related log analysis

Can:
  Can related log analysis

  --can                         CAN related log analysis
```

This will display the available command-line options and usage instructions.

## Examples

Here are some examples of how to use LogPy:

- Analyze network module related logs with TCP and MQTT analysis:
```
logpy -m network --tcp --mqtt -l /path/to/logfile.txt
```

- Perform sleep module related log analysis with wake and sleep cycle analysis:
```
logpy -m sleep -l /path/to/logfile.txt
```

- Search for additional keywords in log file
```
logpy -k FALCON WATCHDOG -l /path/to/logfile.txt
```

- Perform analysis of all modules:
```
logpy --all -l /path/to/logfile.txt
```

<!-- - Analyze logs using custom regular expressions:
```bash
logpy --regex pubresponse "\+QMTPUB: (\d),(\d)" -l /path/to/logfile.txt
``` -->

## GUI
Added a GUI version for the logpy application usinf [PySide6](https://doc.qt.io/qtforpython-6/index.html).

This can be started using:
```sh
logpy-gui
```
Supports light and dark themes.
All the command line arguments are available as toggle buttons or fields.
Shortcuts:
`Ctrl + O` - Open log file
`Ctrl + L` - Clear the output
`Ctrl + T` - Toggle Theme

![](media/image.png)
![](media/image-1.png)
![](media/image-2.png)
![](media/image-3.png)

The GUI tool can also be distributed as a standalone application. This can be done using the [PyInstaller](https://www.pyinstaller.org/) and [InstallForge](https://installforge.net/). You can find more about the procedure in my [Notes.md](Notes.md#creating-executable-python-package-for-pyside6).



## Contact

If you have any questions or need support, you can reach out to the developer.

Happy log analysis with LogPy! 🚀