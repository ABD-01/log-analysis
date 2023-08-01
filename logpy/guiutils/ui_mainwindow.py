# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QLabel, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QProgressBar, QPushButton, QSizePolicy,
    QTextBrowser, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionNetwork = QAction(MainWindow)
        self.actionNetwork.setObjectName(u"actionNetwork")
        self.actionNetwork.setCheckable(True)
        self.actionSleep = QAction(MainWindow)
        self.actionSleep.setObjectName(u"actionSleep")
        self.actionSleep.setCheckable(True)
        self.actionTCP = QAction(MainWindow)
        self.actionTCP.setObjectName(u"actionTCP")
        self.actionTCP.setCheckable(True)
        self.actionMQTT = QAction(MainWindow)
        self.actionMQTT.setObjectName(u"actionMQTT")
        self.actionMQTT.setCheckable(True)
        self.actionIgnition = QAction(MainWindow)
        self.actionIgnition.setObjectName(u"actionIgnition")
        self.actionIgnition.setCheckable(True)
        self.actionSleep_Cycle = QAction(MainWindow)
        self.actionSleep_Cycle.setObjectName(u"actionSleep_Cycle")
        self.actionSleep_Cycle.setCheckable(True)
        self.actionIgnore_Case = QAction(MainWindow)
        self.actionIgnore_Case.setObjectName(u"actionIgnore_Case")
        self.actionIgnore_Case.setCheckable(True)
        self.actionShow_Empty_Values = QAction(MainWindow)
        self.actionShow_Empty_Values.setObjectName(u"actionShow_Empty_Values")
        self.actionShow_Empty_Values.setCheckable(True)
        self.actionREADME = QAction(MainWindow)
        self.actionREADME.setObjectName(u"actionREADME")
        self.actionClear_Output = QAction(MainWindow)
        self.actionClear_Output.setObjectName(u"actionClear_Output")
        self.actionClear_Output.setShortcutContext(Qt.ApplicationShortcut)
        self.actionClear_Output.setShortcutVisibleInContextMenu(True)
        self.actionTheme = QAction(MainWindow)
        self.actionTheme.setObjectName(u"actionTheme")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.log_file_label = QLabel(self.centralwidget)
        self.log_file_label.setObjectName(u"log_file_label")

        self.gridLayout.addWidget(self.log_file_label, 0, 0, 1, 1)

        self.log_file_lineedit = QLineEdit(self.centralwidget)
        self.log_file_lineedit.setObjectName(u"log_file_lineedit")

        self.gridLayout.addWidget(self.log_file_lineedit, 1, 0, 1, 2)

        self.log_file_button = QPushButton(self.centralwidget)
        self.log_file_button.setObjectName(u"log_file_button")

        self.gridLayout.addWidget(self.log_file_button, 1, 2, 1, 1)

        self.out_file_label = QLabel(self.centralwidget)
        self.out_file_label.setObjectName(u"out_file_label")

        self.gridLayout.addWidget(self.out_file_label, 2, 0, 1, 1)

        self.out_file_lineedit = QLineEdit(self.centralwidget)
        self.out_file_lineedit.setObjectName(u"out_file_lineedit")

        self.gridLayout.addWidget(self.out_file_lineedit, 3, 0, 1, 2)

        self.out_file_button = QPushButton(self.centralwidget)
        self.out_file_button.setObjectName(u"out_file_button")

        self.gridLayout.addWidget(self.out_file_button, 3, 2, 1, 1)

        self.keywords_label = QLabel(self.centralwidget)
        self.keywords_label.setObjectName(u"keywords_label")

        self.gridLayout.addWidget(self.keywords_label, 4, 0, 1, 2)

        self.keywords_lineedit = QLineEdit(self.centralwidget)
        self.keywords_lineedit.setObjectName(u"keywords_lineedit")

        self.gridLayout.addWidget(self.keywords_lineedit, 5, 0, 1, 3)

        self.ignore_case_checkbox = QCheckBox(self.centralwidget)
        self.ignore_case_checkbox.setObjectName(u"ignore_case_checkbox")

        self.gridLayout.addWidget(self.ignore_case_checkbox, 6, 0, 1, 1)

        self.show_empty_checkbox = QCheckBox(self.centralwidget)
        self.show_empty_checkbox.setObjectName(u"show_empty_checkbox")

        self.gridLayout.addWidget(self.show_empty_checkbox, 6, 1, 1, 1)

        self.start_button = QPushButton(self.centralwidget)
        self.start_button.setObjectName(u"start_button")

        self.gridLayout.addWidget(self.start_button, 7, 0, 1, 3)

        self.progress_bar = QProgressBar(self.centralwidget)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setValue(24)

        self.gridLayout.addWidget(self.progress_bar, 8, 0, 1, 3)

        self.output_textedit = QTextBrowser(self.centralwidget)
        self.output_textedit.setObjectName(u"output_textedit")
        self.output_textedit.setStyleSheet(u"background:black;\n"
"font: 10pt \"Terminal\";\n"
"color:white;")
        self.output_textedit.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.output_textedit, 9, 0, 1, 3)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuModule = QMenu(self.menubar)
        self.menuModule.setObjectName(u"menuModule")
        self.menuAll = QMenu(self.menuModule)
        self.menuAll.setObjectName(u"menuAll")
        self.menuNetwork = QMenu(self.menuModule)
        self.menuNetwork.setObjectName(u"menuNetwork")
        self.menuSleep = QMenu(self.menuModule)
        self.menuSleep.setObjectName(u"menuSleep")
        self.menuSettings = QMenu(self.menubar)
        self.menuSettings.setObjectName(u"menuSettings")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        QWidget.setTabOrder(self.log_file_lineedit, self.log_file_button)
        QWidget.setTabOrder(self.log_file_button, self.out_file_lineedit)
        QWidget.setTabOrder(self.out_file_lineedit, self.out_file_button)
        QWidget.setTabOrder(self.out_file_button, self.keywords_lineedit)
        QWidget.setTabOrder(self.keywords_lineedit, self.ignore_case_checkbox)
        QWidget.setTabOrder(self.ignore_case_checkbox, self.show_empty_checkbox)
        QWidget.setTabOrder(self.show_empty_checkbox, self.start_button)
        QWidget.setTabOrder(self.start_button, self.output_textedit)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuModule.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionExit)
        self.menuModule.addAction(self.menuAll.menuAction())
        self.menuModule.addSeparator()
        self.menuModule.addAction(self.menuNetwork.menuAction())
        self.menuModule.addAction(self.menuSleep.menuAction())
        self.menuAll.addAction(self.actionNetwork)
        self.menuAll.addAction(self.actionSleep)
        self.menuNetwork.addAction(self.actionTCP)
        self.menuNetwork.addAction(self.actionMQTT)
        self.menuSleep.addAction(self.actionIgnition)
        self.menuSleep.addAction(self.actionSleep_Cycle)
        self.menuSettings.addAction(self.actionIgnore_Case)
        self.menuSettings.addAction(self.actionShow_Empty_Values)
        self.menuSettings.addAction(self.actionClear_Output)
        self.menuSettings.addAction(self.actionTheme)
        self.menuHelp.addAction(self.actionREADME)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Log Analysis", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionNetwork.setText(QCoreApplication.translate("MainWindow", u"Network", None))
        self.actionSleep.setText(QCoreApplication.translate("MainWindow", u"Sleep", None))
        self.actionTCP.setText(QCoreApplication.translate("MainWindow", u"TCP", None))
        self.actionMQTT.setText(QCoreApplication.translate("MainWindow", u"MQTT", None))
        self.actionIgnition.setText(QCoreApplication.translate("MainWindow", u"Ignition", None))
        self.actionSleep_Cycle.setText(QCoreApplication.translate("MainWindow", u"Sleep Cycle", None))
        self.actionIgnore_Case.setText(QCoreApplication.translate("MainWindow", u"Ignore Case", None))
        self.actionShow_Empty_Values.setText(QCoreApplication.translate("MainWindow", u"Show Empty Values", None))
        self.actionREADME.setText(QCoreApplication.translate("MainWindow", u"README", None))
        self.actionClear_Output.setText(QCoreApplication.translate("MainWindow", u"Clear Output", None))
#if QT_CONFIG(shortcut)
        self.actionClear_Output.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+L", None))
#endif // QT_CONFIG(shortcut)
        self.actionTheme.setText(QCoreApplication.translate("MainWindow", u"Toggle Theme", None))
        self.log_file_label.setText(QCoreApplication.translate("MainWindow", u"Log File:", None))
        self.log_file_button.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.out_file_label.setText(QCoreApplication.translate("MainWindow", u"Output File:", None))
        self.out_file_button.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.keywords_label.setText(QCoreApplication.translate("MainWindow", u"Keywords (separated by ';'):", None))
        self.ignore_case_checkbox.setText(QCoreApplication.translate("MainWindow", u"Ignore Case", None))
        self.show_empty_checkbox.setText(QCoreApplication.translate("MainWindow", u"Show Empty Values", None))
        self.start_button.setText(QCoreApplication.translate("MainWindow", u"Start Analysis", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuModule.setTitle(QCoreApplication.translate("MainWindow", u"Module", None))
        self.menuAll.setTitle(QCoreApplication.translate("MainWindow", u"Select Module", None))
        self.menuNetwork.setTitle(QCoreApplication.translate("MainWindow", u"Network", None))
        self.menuSleep.setTitle(QCoreApplication.translate("MainWindow", u"Sleep", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

