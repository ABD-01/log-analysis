# PySide6 Notes

[TOC]

# Using Sys to send signals across scripts

```python
class EmittingStream(QObject):
    textWritten = Signal(str)
    progress = Signal(int)
    def write(self, text):
        self.textWritten.emit(text)

    def set_progress(self, value):
        self.progress.emit(value)

    def flush(self):
        pass
```

**sys.stdout** has attribute write 

I overwrote it

```python
stream = EmittingStream()
sys.stdout = stream
stream.textWritten.connect(self.showOuput)
stream.progress.connect(self.setProgress)
```

Ref: 

- [How to understand sys.stdout and sys.stderr in Python - Stack Overflow](https://stackoverflow.com/questions/31420317/how-to-understand-sys-stdout-and-sys-stderr-in-python)
- [How to understand sys.stdout and sys.stderr in Python](https://stackoverflow.com/questions/31420317/how-to-understand-sys-stdout-and-sys-stderr-in-python)

# Starting a python script in new thread

## 1. Using threading Module

```python
from PySide6.QtCore import QObject, QThreadPool, Signal

class LogPyGUI(QMainWindow):
	def __init__(self):
		...
		self.threadpool = QThreadPool()
		...
		self.ui.start_button.clicked.connect(self.start_analysis)
		...

	def start_analysis(self):
		...
		command = ["logpy"]
	  command.extend(["-l", self.args.log_file])
	  command.extend(["-o", self.args.out_file])
	  ...
		command.extend(["--GUI"])
		
		sys.argv = command
	  stream = EmittingStream()
	  sys.stdout = stream
	  stream.textWritten.connect(self.showOuput)
	  stream.progress.connect(self.setProgress)
	
	  analysis_thread = threading.Thread(target=main())
		# Where main.py takes command line arguments
	  analysis_thread.start()

	# To reset the sys.stdout back to default
	def __del__(self):
		sys.stdout = sys.__stdout__
```

## 2. Using QRunnable

```python
from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal, Slot, QThread

class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)

class Worker(QRunnable):
    def __init__(self, args):
        super(Worker, self).__init__()
        self.p = args
        self.signals = WorkerSignals()

    def AnalyzeLogs(self, p, progress_callback):
        log_analyzer = LogAnalyzer(p)
				...
        return log_analyzer.print_summary()

    @Slot()
    def run(self):

        try:
           output = self.AnalyzeLogs(self.p, self.signals.progress)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(output)
        finally:
            self.signals.finished.emit()

class LogPyGUI(QMainWindow):
    def __init__(self):
        super().__init__()
				...
        self.threadpool = QThreadPool()
				...
				self.ui.start_button.clicked.connect(self.start_a)
				...

    def finished(self):
        QMessageBox.about(self, "Finished", "Log Analysis Finished")

    @Slot()
    def start(self):
        if not self.get_args():
            return

        self.worker = Worker(self.args) 
        self.worker.signals.result.connect(self.showOuput)
        self.worker.signals.finished.connect(self.finished)
        self.worker.signals.progress.connect(self.setProgress)

        self.threadpool.start(self.worker)
```

## 3. Using QObject and QThread

Reference: [QThread - Qt for Python](https://doc.qt.io/qtforpython-6/PySide6/QtCore/QThread.html)

```python
from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal, Slot, QThread

class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)

class Worker(QObject):
    def __init__(self, args):
        super(Worker, self).__init__()
        self.p = args
        self.signals = WorkerSignals()

    def AnalyzeLogs(self, p, progress_callback):
        return log_analyzer.print_summary()

    def run(self):

        try:
           output = self.AnalyzeLogs(self.p, self.signals.progress)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(output)
        finally:
            self.signals.finished.emit()

class LogPyGUI(QMainWindow):
    def __init__(self):
        super().__init__()
				...
        self.threadpool = QThreadPool()
				...
				self.ui.start_button.clicked.connect(self.start_analysis)
				...

    def finished(self):
        QMessageBox.about(self, "Finished", "Log Analysis Finished")
        print("LOG ANALYSIS COMPLETE")
        self.ui.start_button.setEnabled(True)
        self.thread.quit()

    @Slot()
    def start(self):
        if not self.get_args():
            return
        self.ui.start_button.setEnabled(False)

        self.thread = QThread()
        self.worker = Worker(self.args) 
        self.worker.moveToThread(self.thread)
        self.worker.signals.result.connect(self.showOuput)
        self.worker.signals.finished.connect(self.finished)
        self.worker.signals.progress.connect(self.setProgress)

        self.thread.started.connect(self.worker.run)
        self.thread.finished.connect(self.thread.quit)
        self.worker.start()

```

# Creating Python Package

## [Old Way] Setuptools

The **`setup.py`** file is used to package your Python module so that it can be easily installed and distributed. It typically contains information about your package, such as its name, version, description, author, and the modules or packages it includes. Here's a basic example of a **`setup.py`** file for a module:

```python
from setuptools import setup, find_packages

setup(
    name='your_module',          # Replace 'your_module' with your module name
    version='1.0.0',             # Replace '1.0.0' with your desired version number
    description='Description of your module',
    author='Your Name',
    packages=find_packages(),
    install_requires=[
        're',                    # List any dependencies required by your module here
        'easydict',
        'tabulate',
        'argparse',
        # Add more dependencies if needed
    ],
    entry_points={
        'console_scripts': [
            'your_script_name=your_module.main:main',   # Replace 'your_script_name' with the name of your main script
        ],
    },
)
```

- **`version`**: The version number of your module. Use the **[Semantic Versioning](https://semver.org/)** scheme (major.minor.patch).

To create a distributable package

`python setup.py sdist`

This will create a **`.tar.gz`** file in the **`dist`** directory

`pip install /path/to/your_module-1.0.0.tar.gz`

## Building package using pyproject.toml

> **Info: Using `setup.py`**
> 
> 
> Setuptools offers first class support for `setup.py` files as a configuration mechanism.
> 
> It is important to remember, however, that running this file as a script (e.g. `python setup.py sdist`) is strongly **discouraged**, and that the majority of the command line interfaces are (or will be) **deprecated** (e.g. `python setup.py install`, `python setup.py bdist_wininst`, …).
> 
> We also recommend users to expose as much as possible configuration in a more *declarative* way via the [pyproject.toml](https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html) or [setup.cfg](https://setuptools.pypa.io/en/latest/userguide/declarative_config.html), and keep the `setup.py` minimal with only the dynamic parts (or even omit it completely if applicable).
> 
> See [Why you shouldn’t invoke setup.py directly](https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html) for more background.
> 
> — From: [Quickstart - setuptools 68.1.2.post20230818 documentation (pypa.io)](https://setuptools.pypa.io/en/latest/userguide/quickstart.html#basic-use)
<br></br>
> The Python packaging community is moving towards using declarative configuration files like **`pyproject.toml`** or **`setup.cfg`** instead of relying on the traditional **`setup.py`** script. This is part of the Python Packaging Authority (PyPA) initiative to improve the packaging ecosystem.
> 
> 
> — ChatGPT
> 

To make use of **`pyproject.toml`**, you will need to have the **`setuptools`** package version 46.4.0 or later installed, as it added support for this configuration file.

Example:

```toml
[build-system]
requires = ["setuptools>=46.4.0", "wheel"]
build-backend = "setuptools.build_meta"

[tool.logpy]
name = "logpy"
version = "1.0.0"
author = "Your Name"
author_email = "your@email.com"
description = "Your log analysis tool"
# Add other metadata options as needed

[tool.logpy.entry_points]
console_scripts = ["logpy=logpy.main:main"]
```

> With **`pyproject.toml`** defined, you can then build and distribute your package using modern tools like **`flit`** or **`poetry`**, which leverage this configuration file for building, packaging, and distribution.
> 
> 
> — ChatGPT
> 

### Poetry

Poetry: [Basic usage | Documentation | Poetry - Python dependency management and packaging made easy (python-poetry.org)](https://python-poetry.org/docs/basic-usage/)

Example:

```toml
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[tool.poetry]
name = "logpy"
version = "0.1.0"
description = "Your Log Analysis Package"
authors = ["Your Name <your.email@example.com>"]
license = "MIT"
keywords = ["log", "analysis"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
]

[tool.poetry.dependencies]
python = "^3.7"
tabulate = "^0.8"
easydict = "^1.9"
argparse = "^1.4"

[tool.poetry.scripts]
logpy = "logpy.main:main"
```

1. **`[build-system]`**: This section is required for specifying the build system to use. In this case, we are using **`setuptools.build_meta`**.
2. **`[tool.poetry]`**: This section is for defining metadata about your package like its name, version, description, authors, license, keywords, and classifiers. You can modify these values to match your project details.
3. **`[tool.poetry.dependencies]`**: This section lists the dependencies required by your package. It includes the modules you mentioned: **`tabulate`**, **`easydict`**, and **`argparse`**.
4. **`[tool.poetry.scripts]`**: This section allows you to define command-line scripts that will be available after the package is installed. In this case, we define a script named **`logpy`**, and it is associated with the **`main:main`** function in your **`main.py`** script. When users run **`logpy`** in the terminal, it will execute the **`main()`** function from **`main.py`**.

```toml
[tool.logpy.entry_points]
console_scripts = ["logpy=logpy.main:main"]

## Turns into

[tool.poetry.scripts]
logpy = "logpy.main:main"
```

> In Python packaging, **`poetry`** is a tool for dependency management and packaging. It provides a more modern and user-friendly approach to managing project dependencies and creating distributable packages. The **`pyproject.toml`** file is used by Poetry to define the project's metadata, dependencies, scripts, and other configuration options.
> 
> 
> On the other hand, **`setup.py`** is a traditional way of defining project metadata and packaging details. Historically, it has been used with **`setuptools`** for building and distributing Python packages. It's still widely used and supported, but as mentioned in the setuptools documentation, it's recommended to use a more declarative approach with **`pyproject.toml`** or **`setup.cfg`** and keep the **`setup.py`** minimal with only the dynamic parts.
> 
> Here's why **`pyproject.toml`** with **`poetry`** is preferred over **`setup.py`** for defining scripts and dependencies:
> 
> 1. **More Declarative Configuration**: **`pyproject.toml`** is more declarative, and it separates the project configuration from the build configuration. It allows you to define the project metadata, dependencies, and scripts more cleanly.
> 2. **Locking Dependencies**: Poetry provides a way to lock the dependencies by generating a **`poetry.lock`** file. This file ensures that the project uses specific versions of the dependencies, ensuring a consistent environment across different installations.
> 3. **Easier Dependency Management**: Poetry simplifies dependency management by offering various commands to add, update, and remove packages easily.
> 
> Regarding your second example, the **`[project]`** section with **`setup.py`** is used when defining metadata for traditional Python packaging using **`setuptools`**. It is still widely used and is a valid way to define scripts and dependencies.
> 
> However, when using **`poetry`**, the scripts and dependencies are defined under the **`[tool.poetry]`** section in the **`pyproject.toml`** file. It provides a more modern and unified way to define all aspects of the project, including scripts, dependencies, and package details.
> 
> In summary, if you are using **`poetry`** for managing your project and dependencies, it's best to define scripts and dependencies in the **`pyproject.toml`** file under **`[tool.poetry.scripts]`** and **`[tool.poetry.dependencies]`** sections, respectively. This aligns with the more modern and declarative approach that **`poetry`** provides.
> 
> — ChatGPT
> 

**Usage**:

![poetry build](https://bitbucket.org/repo/jKLL9ey/images/1021884919-Untitled.png)

poetry build

To install

`pip install .\dist\logpy-1.3.3-py3-none-any.whl`

Having multiple entry points:

```toml
[tool.poetry.scripts]
logpy = "logpy.main:main"
logpy-gui = "logpy.gui:gui"
logpy-gui2 = "logpy.gui_devel:gui"
```

# Creating Executable Python Package for PySide6

Reference:

- [Packaging PySide2 applications for Windows with PyInstaller & InstallForge (pythonguis.com)](https://www.pythonguis.com/tutorials/packaging-pyside2-applications-windows-pyinstaller/)
- [Using PyInstaller — PyInstaller 5.13.0 documentation](https://pyinstaller.org/en/stable/usage.html)

To create .exe for GUI:

`pyinstaller .\logpy\gui_devel.py .\logpy\gui.py -n LogPy-Gui --noconsole`

## Using .spec file

References:

- [[PyInstaller] Create multiple exe's in one folder | ZA-Coding (zacoding.com)](https://www.zacoding.com/en/post/pyinstaller-create-multiple-executables/)

Making .spec files:

- For **logpy/main.py**
    
    ```powershell
    pyi-makespec .\logpy\main.py -n LogPy
    ```
    
- For **logpy/gui.py**
    
    ```powershell
    pyi-makespec .\logpy\gui.py `
    		-n LogPy-Gui `
    		--noconsole `
    		--icon=logpy/guiutils/results-icon.ico `
    		--add-data="README.md;." `
    		--add-data="logpy/guiutils/results-icon.ico;icons"
    ```
    
- For **logpy/gui_devel.py**
    
    ```powershell
    pyi-makespec .\logpy\gui_devel.py `
    		-n LogPy-Gui2 `
    		--noconsole `
    		--icon=logpy/guiutils/results-icon.ico `
    		--add-data="README.md;." `
    		--add-data="logpy/guiutils/results-icon.ico;icons" `
    		--add-data="logpy/guiutils/analysis-icon.ico;icons"
    ```
    

Combining all spec files in **********************LogPy.spec********************** file:

```toml
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

logpy = Analysis(['logpy\\main.py'], ...)
logpy_pyz = PYZ(logpy.pure, ...)
logpy_exe = EXE(logpy_pyz, name='LogPy', ...,)

gui = Analysis(['logpy\\gui.py'], ...)
gui_pyz = PYZ(gui.pure, ...)
gui_exe = EXE(gui_pyz, name='LogPy-Gui',icon=['logpy\\guiutils\\results-icon.ico'], ...)

gui2 = Analysis(['logpy\\gui_devel.py'], datas=[('README.md', '.'), ('logpy/guiutils/results-icon.ico', 'icons')], ...)
gui2_pyz = PYZ(gui2.pure, ...)
gui2_exe = EXE(gui2_pyz, icon=['logpy\\guiutils\\results-icon.ico'], ...)

coll = COLLECT(
    logpy_exe,
    logpy.binaries,
    logpy.zipfiles,
    logpy.datas,

    gui_exe,
    gui.binaries,
    gui.zipfiles,
    gui.datas,

    gui2_exe,
    gui2.binaries,
    gui2.zipfiles,
    gui2.datas,

    strip=False,
    upx=True,
    upx_exclude=[],
    name='LogPy',
)
```

To build:

`pyinstaller .\LogPy.spec`

## Using InstallForge

Refer: 

[Quick Start Guide - InstallForge Documentation](https://installforge.net/docs/getting-started/quick-start-guide/#building-the-setup-package)