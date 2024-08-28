import sys
import psutil
import serial
import platform
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class ProcessMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.serial_port = serial.Serial('COM3', 9600)  # Update with your Arduino serial port
        self.update_process_info()

    def initUI(self):
        self.setWindowTitle('Process Monitor')
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()

        self.os_label = QLabel()
        self.process_label = QLabel()
        self.ram_label = QLabel()

        self.os_label.setFont(QFont('Arial', 12))
        self.process_label.setFont(QFont('Arial', 12))
        self.ram_label.setFont(QFont('Arial', 12))

        layout.addWidget(self.os_label)
        layout.addWidget(self.process_label)
        layout.addWidget(self.ram_label)

        self.setLayout(layout)

    def update_process_info(self):
        # Detect OS
        os_name = platform.system()
        self.os_label.setText(f"Operating System: {os_name}")

        # Update Process Info
        process_info = self.get_process_info()
        self.process_label.setText(f"Processes: {process_info}")

        # Send to Arduino
        self.send_to_arduino(process_info)

    def get_process_info(self):
        process_info = ""
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                process_info += f"{proc.info['name']}: CPU: {proc.info['cpu_percent']}%, RAM: {proc.info['memory_info'].rss / (1024 * 1024):.2f}MB\n"
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return process_info

    def send_to_arduino(self, data):
        if self.serial_port.is_open:
            self.serial_port.write(data.encode())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProcessMonitor()
    window.show()
    sys.exit(app.exec())
