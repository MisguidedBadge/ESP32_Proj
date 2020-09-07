
from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QListWidget, QTableWidgetItem)
from PyQt5.QtGui import QIntValidator
# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *
import serial
import serial.tools.list_ports

def ScanCOMPorts():
    portlist = serial.tools.list_ports.comports()
    return portlist

baudrate_lists = ['9600', '19200', '38400', '57600', '115200']
parity_lists = ['None', 'Even', 'Odd', 'Mark', 'Space']
stopbits_lists = ['1', '2']
databits_lists = ['6', '7', '8']
conn_ov_list = ['COM Port', 'Baud Rate', 'Parity', 'Stop Bits', 'Data Bits']
PARITY_NAMES_REV = {
    'None': 'N',
    'Even': 'E',
    'Odd': 'O',
    'Mark': 'M',
    'Space': 'S',
}
ser = serial.Serial()
# GUI Stuff
class WidgetGallery(QDialog):
    # Serial Parameters ##
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)
        self.COMPORT = 'N/A'
        self.parity = 'none'
        self.baudrate = '9600'
        self.stopbits = '1'
        self.databits = '8'
        # Create Palette that can be changed
        self.Palette = QApplication.palette()
        # Create Sub Division
        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createBottomLeftGroupBox()
        self.createBottomRightGroupBox()
        self.createBottomRightRGroupBox()
        # Layout for division
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.topLeftGroupBox, 0, 2, 1, 2)
        mainLayout.addWidget(self.topRightGroupBox, 1, 0, 1, 1)
        mainLayout.addWidget(self.bottomLeftGroupBox, 0, 0, 1, 2)
        mainLayout.addWidget(self.bottomRightGroupBox, 1, 1, 1, 1)
        mainLayout.addWidget(self.bottomRightRGroupBox, 1, 2, 1, 1)
        self.setLayout(mainLayout)
        # Initial Setup
        self.baudrate = self.baud_set.currentText()
        self.parity = self.parity_set.currentText()
        self.stopbits = self.stopbits_set.currentText()
        self.databits = self.databits_set.currentText()
        self.connection_overview.setItem(0,0, QTableWidgetItem(self.COMPORT))
        self.connection_overview.setItem(0,1, QTableWidgetItem(self.baudrate))
        self.connection_overview.setItem(0,2, QTableWidgetItem(self.parity))
        self.connection_overview.setItem(0,3, QTableWidgetItem(self.stopbits))
        self.connection_overview.setItem(0, 4, QTableWidgetItem(self.databits))
        # Interactions ##
        self.scanport.clicked.connect(self.ListPorts)
        self.baud_set.currentIndexChanged.connect(self.SetBaudRate)
        self.parity_set.currentIndexChanged.connect(self.SetParity)
        self.stopbits_set.currentIndexChanged.connect(self.SetStopBits)
        self.databits_set.currentIndexChanged.connect(self.SetDataBits)
        self.comlist.currentItemChanged.connect(self.SetCOMPort)
        self.connect_button.clicked.connect(self.ConnectFunc)
########################## METHODS ##########################
    def ListPorts(self):
        portslist = ScanCOMPorts()
        self.comlist.clear()
        for index in range(len(portslist)):
            self.comlist.addItem(portslist[index].device)
    def SetCOMPort(self):
        self.COMPORT = self.comlist.currentItem().text()
        self.connection_overview.setItem(0,0, QTableWidgetItem(self.COMPORT))
    def SetBaudRate(self):
        self.baudrate = self.baud_set.currentText()
        self.connection_overview.setItem(0, 1, QTableWidgetItem(self.baudrate))
    def SetParity(self):
        self.parity = self.parity_set.currentText()
        self.connection_overview.setItem(0, 2, QTableWidgetItem(self.parity))
    def SetStopBits(self):
        self.stopbits = self.stopbits_set.currentText()
        self.connection_overview.setItem(0, 3, QTableWidgetItem(self.stopbits))
    def SetDataBits(self):
        self.databits = self.databits_set.currentText()
        self.connection_overview.setItem(0, 4, QTableWidgetItem(self.databits))
    def ConnectFunc(self):
        if(self.COMPORT == 'N/A'):
            self.receive_stream.setText('Invalid COM Port')
        else:
            """         serial.Serial.port = self.COMPORT
            serial.Serial.baudrate = int(self.baudrate)
            serial.Serial.parity = self.parity
            serial.Serial.stopbits = int(self.stopbits)
            serial.Serial.databits = int(self.databits) """

            ser = serial.Serial(port = self.COMPORT, baudrate = int(self.baudrate),stopbits = int(self.stopbits), 
            parity = PARITY_NAMES_REV[self.parity], bytesize = int(self.databits))
            self.receive_stream.setText('Read \n')

########################## Divisions ########################
    # Top left box subdivision To 
    def createTopLeftGroupBox(self):
        # Create group box object
        self.topLeftGroupBox = QGroupBox("Available Ports") 
        # Widget Declaration
        self.scanport = QPushButton("Scan COM Ports")
        self.scanport.setDefault(True)
        self.comlist = QListWidget()
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.scanport)
        layout.addWidget(self.comlist)
        self.topLeftGroupBox.setLayout(layout)
    # Top Right
    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("Connection Settings")
        # Widgets
        self.baud_set_label = QLabel("Baud Rate")
        self.baud_set = QComboBox()
        self.baud_set.addItems(baudrate_lists)
        self.parity_set_label = QLabel("Parity")
        self.parity_set = QComboBox()
        self.parity_set.addItems(parity_lists)
        self.stopbits_set_label = QLabel("Stop Bits")
        self.stopbits_set = QComboBox()
        self.stopbits_set.addItems(stopbits_lists)
        self.databits_set_label = QLabel("Data Bits")
        self.databits_set = QComboBox()
        self.databits_set.addItems(databits_lists)
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.baud_set_label)
        layout.addWidget(self.baud_set)
        layout.addWidget(self.parity_set_label)
        layout.addWidget(self.parity_set)
        layout.addWidget(self.stopbits_set_label)
        layout.addWidget(self.stopbits_set)
        layout.addWidget(self.databits_set_label)
        layout.addWidget(self.databits_set)
        #layout.addStretch(1)

        self.topRightGroupBox.setLayout(layout)
    def createBottomLeftGroupBox(self):
        self.bottomLeftGroupBox = QGroupBox("Connection Setup")
        # Widgets
        self.connection_overview_label = QLabel("Connection Settings Overview")
        self.connection_overview = QTableWidget(1, 5)
        self.connection_overview.setHorizontalHeaderLabels(conn_ov_list)
        self.connect_button = QPushButton('Connect')
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.connection_overview_label)
        layout.addWidget(self.connection_overview)
        layout.addWidget(self.connect_button)
        self.bottomLeftGroupBox.setLayout(layout)
    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox("Send Stream")
        # Widgets
        self.sendstream = QTextEdit()
        self.sendbutton = QPushButton('Send')

        #self.sendstream.setMax(100)
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.sendstream)
        layout.addWidget(self.sendbutton)
        self.bottomRightGroupBox.setLayout(layout)
    def createBottomRightRGroupBox(self):
        self.bottomRightRGroupBox = QGroupBox("Received Stream")
        #Widgets
        self.receive_stream = QTextEdit()

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.receive_stream)
        self.bottomRightRGroupBox.setLayout(layout)
########################## END GUI ##########################

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.setStyle('Oxygen')
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec_())
    serial.close() 



