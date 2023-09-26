import os.path as osp
import re
import sys
import traceback
from os import makedirs, startfile
import subprocess
from pathlib import Path

import markdown
# from qt_material import QtStyleTools, apply_stylesheet
import qdarktheme
from easydict import EasyDict
from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal, Slot, QThread
from PySide6.QtGui import QIcon, QAction, QActionGroup
from PySide6.QtWidgets import (QApplication, QFileDialog, QMainWindow,
                               QMessageBox)

from guiutils.helpDialog import HelpDialog
from guiutils.ui_mainwindow import Ui_MainWindow
from logutils import MODULE_ADDLOG, MODULE_SUBFUNCTIONS, BasicLog, LogAnalyzer


try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'AEPL.ATCU.LogPy.1'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass


class EmittingStream(QObject):
    textWritten = Signal(str)
    progress = Signal(int)
    def write(self, text):
        self.textWritten.emit(text)

    def set_progress(self, value):
        self.progress.emit(value)

    def flush(self):
        pass

class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)

# class Worker(QObject):
class Worker(QRunnable):
    def __init__(self, args):
        super(Worker, self).__init__()
        self.p = args
        # self.p.disable_progresslive = True #temp
        self.p.GUI=True# temp
        self.signals = WorkerSignals()

    def AnalyzeLogs(self, p, progress_callback):
        log_analyzer = LogAnalyzer(p)

        if p.module is None:
            p.all = True
        if p.all:
            for add_logs in MODULE_ADDLOG.values():
                for f in add_logs.values():
                    f(log_analyzer, p)
        else:
            for module, subfuncs in MODULE_SUBFUNCTIONS.items():
                if p.module == module:
                    all_funt = True
                    for subfunc in subfuncs:
                        if getattr(p, subfunc):
                            MODULE_ADDLOG[module][subfunc](log_analyzer, p)
                            all_funt = False
                    if all_funt:
                        for f in MODULE_ADDLOG[module].values():
                            f(log_analyzer, p)
        
        for kw in p.keywords:
            log_analyzer.add_log_type(BasicLog(kw, kw, ignore_case=p.ignore_case))
        
        log_analyzer.analyze(progress_callback)
        return log_analyzer.print_summary(p.show_empty)

    @Slot() # comment if using QObject
    def run(self):

        try:
           output = self.AnalyzeLogs(self.p, self.signals.progress)
            # output = self.fn(self.p, self.signals.progress)
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

        self.initUI()
        self.initArgs()
        self.add_menus()
        self.link_actions()
        self.threadpool = QThreadPool()

    def initUI(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
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

    def add_menus(self):
        menu = self.ui.menuModule
        group = QActionGroup(self)

        action = QAction("All", self)
        action.setCheckable(True)
        action.setActionGroup(group)
        menu.addAction(action)
        menu.addSeparator()

        for k,v in MODULE_SUBFUNCTIONS.items():
            action = QAction(k.title(), self)
            action.setCheckable(True)
            action.setActionGroup(group)
            menu.addAction(action)
            menu.addSeparator()
            for subfunc in v:
                self.args[subfunc] = None

    def link_actions(self):

        self.ui.actionOpen.triggered.connect(self.open)
        self.ui.actionExit.triggered.connect(self.close)

        self.ui.actionIgnore_Case.triggered.connect(self.settings("ignore_case"))
        self.ui.actionShow_Empty_Values.triggered.connect(self.settings("show_empty"))
        self.ui.actionClear_Output.triggered.connect(self.clear_output_textedit)
        self.ui.actionTheme.triggered.connect(self.changetheme)

        self.ui.actionREADME.triggered.connect(self.showREADME)

        self.ui.ignore_case_checkbox.clicked.connect(self.settings("ignore_case"))
        self.ui.show_empty_checkbox.clicked.connect(self.settings("show_empty"))

        self.ui.log_file_button.clicked.connect(self.open)
        self.ui.out_file_button.clicked.connect(self.open)

        self.ui.start_button.clicked.connect(self.start)

    def settings(self, setting):
        settings = {"ignore_case": (self.ui.ignore_case_checkbox, self.ui.actionIgnore_Case),
                    "show_empty": (self.ui.show_empty_checkbox, self.ui.actionShow_Empty_Values)}
        def func(arg):
            settings[setting][0].setChecked(arg)
            settings[setting][1].setChecked(arg)
            self.args[setting] = arg
        
        return func

    def showREADME(self):
        readme_path = Path("README.md")
        if not osp.exists(readme_path):
            QMessageBox.warning(self, "Error", "README.md not found")
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
        # self.ui.output_textedit.setText(s)
        self.ui.output_textedit.append(s)

    def clear_output_textedit(self):
        self.ui.output_textedit.clear()

    def finished(self):
        # QMessageBox.about(self, "Finished", "Log Analysis Finished")
        button = QMessageBox.question(self, "Finished", "Log Analysis Finished\nDo you want to open the output file?", QMessageBox.Yes | QMessageBox.No)
        if button == QMessageBox.Yes:
            notepad_plus_plus_paths = [r'C:\Program Files\Notepad++\notepad++.exe', r'C:\Program Files (x86)\Notepad++\notepad++.exe']
            if osp.exists(notepad_plus_plus_paths[0]):
                subprocess.run([notepad_plus_plus_paths[0], self.args.out_file])
            elif osp.exists(notepad_plus_plus_paths[1]):
                subprocess.run([notepad_plus_plus_paths[1], self.args.out_file])             
            else:
                startfile(self.args.out_file)

    def open(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Log File", "", "Log Files (*.log);;All Files (*)", options=options
        )
        if file_name:
            self.ui.log_file_lineedit.setText(file_name)
            self.ui.out_file_lineedit.clear()

    def get_args(self):
        log_file_path = self.ui.log_file_lineedit.text()
        if len(log_file_path) == 0:
            QMessageBox.critical(self, "Error", "No log file selected")
            return False
        if not osp.exists(log_file_path):
            messagebox = QMessageBox.warning(self, "File Error", "Log file not found. \nPlease select a valid log file")
            return False

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

        for action in self.ui.menuModule.actions():
            if action.isChecked():
                self.args.module = action.text().lower()
                break
        
        if self.args.module == "all":
            self.args.module = None

        return True

    @Slot()
    def start(self):
        if not self.get_args():
            return
        # self.ui.start_button.setEnabled(False)
        # self.thread = QThread()
        self.worker = Worker(self.args) 
        # self.worker.moveToThread(self.thread) #incase if Worker is QObject
        self.worker.signals.result.connect(self.showOuput)
        self.worker.signals.finished.connect(self.finished)
        self.worker.signals.progress.connect(self.setProgress)

        self.threadpool.start(self.worker)
        # if using QThread
        # self.thread.started.connect(self.worker.run)
        # self.thread.finished.connect(self.thread.quit)
        # self.worker.start()

def gui():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(osp.join(osp.dirname(__file__),"icons/results-icon.ico")))
    window = LogPyGUI()
    qdarktheme.setup_theme()
    # apply_stylesheet(app, theme='dark_amber.xml')
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    gui()