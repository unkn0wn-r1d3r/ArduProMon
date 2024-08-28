import sys
import serial
import serial.tools.list_ports
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

class SerialConnector(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.serial_port = None

    def initUI(self):
        self.setWindowTitle('Serial Port Connector')
        self.setGeometry(100, 100, 300, 200)
        
        # Layout
        layout = QVBoxLayout()
        
        # Port selection
        self.port_selector = QComboBox()
        self.refresh_ports()
        self.port_selector.currentIndexChanged.connect(self.on_port_selected)
        layout.addWidget(self.port_selector)
        
        # Connection button
        self.connect_button = QPushButton('Connect')
        self.connect_button.clicked.connect(self.toggle_connection)
        layout.addWidget(self.connect_button)
        
        # Status label
        self.status_label = QLabel('Status: Disconnected')
        self.status_label.setFont(QFont('Arial', 12))
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)

    def refresh_ports(self):
        ports = [p.device for p in serial.tools.list_ports.comports()]
        self.port_selector.clear()
        self.port_selector.addItems(ports)

    def on_port_selected(self):
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        self.connect_button.setText('Connect')
        self.status_label.setText('Status: Disconnected')

    def toggle_connection(self):
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            self.connect_button.setText('Connect')
            self.status_label.setText('Status: Disconnected')
        else:
            port = self.port_selector.currentText()
            try:
                self.serial_port = serial.Serial(port, 115200, timeout=1)
                self.connect_button.setText('Disconnect')
                self.status_label.setText(f'Status: Connected to {port}')
            except Exception as e:
                self.status_label.setText(f'Error: {str(e)}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SerialConnector()
    window.show()
    sys.exit(app.exec())
