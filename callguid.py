import sys
import os
import ctypes
import win32process
import clipboard
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
        QMessageBox, QProgressBar, QDialog, QFileDialog, QGridLayout, QHBoxLayout,
        QLabel, QLineEdit, QMessageBox, QPushButton, QTextEdit, QVBoxLayout,
        QWidget)
import traceback
#sys.path.insert(0, 'D:/Python/PyWhatsapp/ui_gui.py')
from ui_guid import Ui_WhatsappAutomation
from PyWhatsapp import input_contacts, input_message, send_files, send_attachment, send_unsaved_contact_message, send_message, whatsapp_login, sender, scheduler

addcontacts=None
media = "no"
doc = "no"
fileName1 = None
fileName2 = None
fileName3 = None
class MainWindow(QMainWindow, Ui_WhatsappAutomation):
    # Maintain the list of browser windows so that they do not get garbage
    # collected.
    _window_list = []

    def __init__(self):
        super(MainWindow, self).__init__()

        MainWindow._window_list.append(self)

        global addcontacts
        addcontacts = []


        self.setupUi(self)

        # Qt Designer (at least to v4.2.1) can't handle arbitrary widgets in a
        # QToolBar - even though uic can, and they are in the original .ui
        # file.  Therefore we manually add the problematic widgets.
        #Contact Type
        self.unsaved.toggled.connect(lambda: self.processunsaved(self.unsaved))
        self.saved.toggled.connect(lambda: self.processsaved(self.saved))
        #Upload Contact File
        self.selectfilebutton.clicked.connect(self.processcontact)
        #Upload Media File
        self.addmedia.clicked.connect(self.processmedia)
        #upload Document File
        self.adddoc.clicked.connect(self.processdoc)
        #send message
        self.send.clicked.connect(self.processfinal)

    # Get the system clipboard contents

    def processunsaved(self, enabled):
            if enabled:
                self.radiovalue.setText("2")
            else:
                self.radiovalue.setText("1")
    def processsaved(self, enabled):
            if enabled:
                self.radiovalue.setText("1")
            else:
                self.radiovalue.setText("2")


    def processcontact(self):
        self.listWidget.clear()
        addcontacts.clear()
        global media, fileName1
        fileName1, _ = QFileDialog.getOpenFileName(self, "Select Contact File",
                                                  '', "Text Documents (*.txt);;CSV (Comma delimited) (*.csv);;All Files (*)")

        #model = QtGui.QStandardItemModel()
        #self.listView.setModel(model)
        if fileName1 != "":
          with open(fileName1, 'r') as contacts:
            self.selectfilebutton.setText(os.path.basename(fileName1))
            for line in contacts.readlines():
                line = line.rstrip()  # remove trailing '\n'
                if self.radiovalue.text() == "1":
                    addcontacts.append('"'+line+'"')
                    self.listWidget.addItem(line)
                    #item = QtGui.QStandardItem(line)
                    #model.appendRow(item)
                elif len(line) == 10:
                    addcontacts.append("91"+line)
                    self.listWidget.addItem(line)
                    #item = QtGui.QStandardItem(line)
                    #model.appendRow(item)
            self.contactsuploaded.setText("Contacts Uploaded ("+str(len(addcontacts))+")")

    def processmedia(self):

        global media,fileName2
        #input_contacts(self.radiovalue.text(), None, addcontacts, "no")
        fileName2, _ = QFileDialog.getOpenFileName(self, "Attach Media File",
                                                  '', "All Files (*)")
        fileName2 = fileName2.replace('/','\]')
        fileName2 = fileName2.replace(']','')

        if fileName2 == "":
         self.medialabel.setText(": Add Media")
         media = "no"
        else:
         self.medialabel.setText(os.path.basename(fileName2))
         media = "yes"

    def processdoc(self):

        global doc,fileName3
        fileName3, _ = QFileDialog.getOpenFileName(self, "Attach File",
                                                  '', "PDF (*.pdf);;Word Document (*.doc);;All Files (*)")
        fileName3 = fileName3.replace('/', '\]')
        fileName3 = fileName3.replace(']', '')
        if fileName3 == "":
            self.doclabel.setText(": Add Document")
            doc = "no"
        else:
            self.doclabel.setText(os.path.basename(fileName3))
            doc = "yes"

    def processfinal(self):
        self.send.setStyleSheet("background-color: green")
        input_contacts(self.radiovalue.text(), None, addcontacts, "no")
        input_message(self.messagebox.toPlainText())
        #sender(self.lineEdit_5.text(), self.lineEdit_6.text(), self.lineEdit_7.text())
        clipboard.copy(self.messagebox.toPlainText())
        whatsapp_login(media, doc)
        if media == "yes" and doc == "yes":
          sender(media, doc, fileName2, fileName3)
        elif media == "yes" and doc == "no":
          sender(media, doc, fileName2, fileName3)
        elif media == "no" and doc == "yes":
          sender(media, doc, fileName2, fileName3)
        elif media == "no" and doc == "no":
          sender(media, doc, fileName2, fileName3)

hwnd = ctypes.windll.kernel32.GetConsoleWindow()
if hwnd != 0:
    ctypes.windll.user32.ShowWindow(hwnd, 0)
    ctypes.windll.kernel32.CloseHandle(hwnd)
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    os.system('taskkill /PID ' + str(pid) + ' /f')

if __name__ == "__main__":
    a = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(a.exec_())