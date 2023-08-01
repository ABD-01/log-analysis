import os.path as osp
import re
import sys
import threading
import traceback
from functools import partial
from os import makedirs, mkdir

from pathlib import Path
import markdown
from easydict import EasyDict
from guiutils.helpDialog import HelpDialog
from guiutils.ui_mainwindow import Ui_MainWindow
from logutils import MODULE_ADDLOG, MODULE_SUBFUNCTIONS, BasicLog, LogAnalyzer
from PySide6.QtCore import (Property, QThread, QFile, QIODevice, QObject, QRunnable, Qt,
                            QThreadPool, QUrl, Signal, Slot)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFileDialog,
                               QHBoxLayout, QLabel, QLineEdit, QMainWindow,
                               QMenuBar, QMessageBox, QProgressBar,
                               QPushButton, QTextBrowser, QTextEdit,
                               QVBoxLayout, QWidget)
# from qt_material import QtStyleTools, apply_stylesheet
import qdarktheme
from tqdm import tqdm

import main

class EmittingStream(QObject):
    textWritten = Signal(str)
    progress = Signal(int)
    def write(self, text):
        self.textWritten.emit(text)

    def set_progress(self, value):
        self.progress.emit(value)

    def flush(self):
        pass

class LogPyGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.initArgs()
        self.link_actions()
        self.threadpool = QThreadPool()

    def initUI(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.menuNetwork.setEnabled(False)
        self.ui.menuSleep.setEnabled(False)

        self.ui.progress_bar.setValue(0)

        self.theme = "dark"
        qdarktheme.setup_theme(self.theme)

    def initArgs(self):
        self.args = EasyDict()
        self.args.log_file = None
        self.args.out_file = None
        self.args.keywords = []
        self.args.topics = []
        self.args.ignore_case = False
        self.args.disable_progresslive = True # Set to True due to TQDM related buffer issues
        self.args.show_empty = False
        self.args.all = False

        self.args.module = None #["network", "sleep"]

        self.args.tcp=False
        self.args.mqtt=False
        self.args.ignition=False
        self.args.sleepcycle=False

    def link_actions(self):

        self.ui.actionOpen.triggered.connect(self.open)
        self.ui.actionExit.triggered.connect(self.close)

        self.ui.actionNetwork.triggered.connect(self.moduleSelected("network"))
        self.ui.actionSleep.triggered.connect(self.moduleSelected("sleep"))

        self.ui.actionIgnore_Case.triggered.connect(self.settings("ignore_case"))
        self.ui.actionShow_Empty_Values.triggered.connect(self.settings("show_empty"))
        self.ui.actionClear_Output.triggered.connect(self.clear_output_textedit)
        self.ui.actionTheme.triggered.connect(self.changetheme)

        self.ui.actionREADME.triggered.connect(self.showREADME)

        self.ui.ignore_case_checkbox.clicked.connect(self.settings("ignore_case"))
        self.ui.show_empty_checkbox.clicked.connect(self.settings("show_empty"))

        self.ui.log_file_button.clicked.connect(self.open)
        self.ui.out_file_button.clicked.connect(self.open)

        self.ui.start_button.clicked.connect(self.start_analysis)

    def open(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Log File", "", "Log Files (*.log);;All Files (*)", options=options
        )
        if file_name:
            self.ui.log_file_lineedit.setText(file_name)

    
    def moduleSelected(self, module):
        actions = {"network": self.ui.menuNetwork,
                    "sleep": self.ui.menuSleep}
        def func(arg):
            actions[module].setEnabled(arg)
            self.args.module = module
            if not arg:
                for action in actions[module].actions():
                    action.setChecked(False)
            
        return func

    def settings(self, setting):
        settings = {"ignore_case": (self.ui.ignore_case_checkbox, self.ui.actionIgnore_Case),
                    "show_empty": (self.ui.show_empty_checkbox, self.ui.actionShow_Empty_Values)}
        def func(arg):
            settings[setting][0].setChecked(arg)
            settings[setting][1].setChecked(arg)
            self.args[setting] = arg
        
        return func

    def showREADME(self):
        readme_path = Path("C:/Users/Muhammed/projects/log_analysis/README.md")
        with open(readme_path, "r") as readme_file:
            markdown_content = readme_file.read()

        html_content = markdown.markdown(markdown_content)

        # Create a message box and set the HTML content as the text
        # message_box = QMessageBox(self)
        # message_box.setWindowTitle("LogPy Help")
        # message_box.setTextFormat(Qt.RichText)  # Set the text format to HTML
        # message_box.setText(html_content)
        # message_box.exec_()

        # Create the custom dialog box and pass the README content
        help_dialog = HelpDialog(html_content)
        help_dialog.exec()


    def changetheme(self):
        # apply_stylesheet(self, theme='light_amber.xml') 
        if self.theme == "dark":
            qdarktheme.setup_theme("light")
            self.theme = "light"
        elif self.theme == "light":
            qdarktheme.setup_theme("dark")
            self.theme = "dark"

    def setProgress(self, progress):
        self.ui.progress_bar.setValue(progress)

    def showOuput(self, s):
        self.ui.output_textedit.append(s)

    def clear_output_textedit(self):
        self.ui.output_textedit.clear()

    def finished(self):
        # message_box = QMessageBox.NoIcon(self, "Finished", "Log Analysis Finished")
        # message_box.exec()
        print("LOG ANALYSIS COMPLETE")
        self.ui.start_button.setEnabled(True)

    def get_args(self):
        log_file_path = self.ui.log_file_lineedit.text()
        if len(log_file_path) == 0:
            QMessageBox.critical(self, "Error", "No log file selected")
            return
        if not osp.exists(log_file_path):
            messagebox = QMessageBox.warning(self, "File Error", "Log file not found. \nPlease select a valid log file")
            return

        out_file = self.ui.out_file_lineedit.text()
        if len(out_file) == 0:
            input_directory, basename = osp.split(log_file_path)
            out_file = osp.join(input_directory, "analysedlogs", 'out_'+ str(basename))
            makedirs(osp.join(input_directory, "analysedlogs"), exist_ok=True)
            self.ui.out_file_lineedit.setText(out_file)

        self.args.log_file = log_file_path
        self.args.out_file = out_file 

        keywords_str = self.ui.keywords_lineedit.text()
        if keywords_str:
            self.args.keywords = [keyword.strip() for keyword in re.split(r"(?<!\\);", keywords_str)]

        # self.args.ignore_case = self.ui.ignore_case_checkbox.isChecked()
        # self.args.show_empty = self.ui.show_empty_checkbox.isChecked()
        
        self.args.tcp = self.ui.actionTCP.isChecked()
        self.args.mqtt = self.ui.actionMQTT.isChecked()
        self.args.ignition = self.ui.actionIgnition.isChecked()
        self.args.sleepcycle = self.ui.actionSleep_Cycle.isChecked()


    def start_analysis(self):
        self.get_args()

        command = ["logpy"]
        command.extend(["-l", self.args.log_file])
        command.extend(["-o", self.args.out_file])
        if self.args.keywords:
            command.extend(["-k"] + self.args.keywords)
        if self.args.ignore_case:
            command.append("-c")
        if self.args.show_empty:
            command.append("--show-empty")

        if self.args.module:
            command.extend(["-m", self.args.module])

        if self.args.disable_progresslive:
            command.append("--disable-progresslive")

        command.extend(["--GUI"])

        sys.argv = command
        stream = EmittingStream()
        sys.stdout = stream
        stream.textWritten.connect(self.showOuput)
        stream.progress.connect(self.setProgress)

        analysis_thread = threading.Thread(target=main.main())
        analysis_thread.start()
        analysis_thread.join()

    def __del__(self):
        sys.stdout = sys.__stdout__

def gui():
    app = QApplication(sys.argv)
    window = LogPyGUI()
    qdarktheme.setup_theme()
    # apply_stylesheet(app, theme='dark_amber.xml')
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LogPyGUI()
    # apply_stylesheet(app, theme='dark_purple.xml')
    qdarktheme.setup_theme()

    window.show()
    sys.exit(app.exec())
