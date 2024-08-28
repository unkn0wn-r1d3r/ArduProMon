import sys
import serial
import serial.tools.list_ports
import psutil
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox
from PySide6.QtCore import QTimer
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
        
        # Timer to periodically send process info
        self.timer = QTimer()
        self.timer.timeout.connect(self.send_process_info)
        
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
            self.timer.stop()
        else:
            port = self.port_selector.currentText()
            try:
                self.serial_port = serial.Serial(port, 115200, timeout=1)
                self.connect_button.setText('Disconnect')
                self.status_label.setText(f'Status: Connected to {port}')
                self.timer.start(5000)  # Send process info every 5 seconds
            except Exception as e:
                self.status_label.setText(f'Error: {str(e)}')

    def send_process_info(self):
        if self.serial_port and self.serial_port.is_open:
            process_info = self.get_process_info()
            self.serial_port.write(f"INFO:{process_info}\n".encode())

    def get_process_info(self):
        processes = psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent'])
        info = ""
        for proc in processes:
            info += f"{proc.info['name']} PID:{proc.info['pid']} RAM:{proc.info['memory_info'].rss / (1024 * 1024):.2f}MB CPU:{proc.info['cpu_percent']}%\n"
        return info

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SerialConnector()
    window.show()
    sys.exit(app.exec())
