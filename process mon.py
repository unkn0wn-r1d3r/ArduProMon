import sys
import serial
import serial.tools.list_ports
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QListWidget
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
import psutil  # To get process information

class SerialConnector(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.serial_port = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_process_info)
        self.processes = []  # To store process info for later use
        self.view_mode = False  # To track view mode state

    def initUI(self):
        self.setWindowTitle('ArduProMon')
        self.setGeometry(100, 100, 400, 300)
        
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

        # View processes button
        self.view_button = QPushButton('View Processes')
        self.view_button.clicked.connect(self.toggle_view_processes)
        layout.addWidget(self.view_button)
        
        # List widget for processes
        self.process_list = QListWidget()
        self.process_list.itemDoubleClicked.connect(self.send_process_info)
        layout.addWidget(self.process_list)
        
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
            self.timer.stop()
        else:
            port = self.port_selector.currentText()
            try:
                self.serial_port = serial.Serial(port, 115200, timeout=1)
                self.connect_button.setText('Disconnect')
                self.status_label.setText(f'Status: Connected to {port}')
                self.timer.start(2000)  # Update every 2 seconds
            except Exception as e:
                self.status_label.setText(f'Error: {str(e)}')

    def update_process_info(self):
        if self.serial_port and self.serial_port.is_open:
            process_info = self.get_process_info()
            if process_info:
                for info in process_info:
                    # Format: <Program Name> <RAM Usage> <CPU Usage>
                    message = f"{info['name']:<20} {info['ram']:<8} {info['cpu']:<4}"
                    self.serial_port.write((message + '\n').encode())

    def get_process_info(self):
        process_info = []
        for proc in psutil.process_iter(['name', 'memory_info', 'cpu_percent']):
            try:
                name = proc.info['name']
                ram = proc.info['memory_info'].rss // (1024 * 1024)  # Convert bytes to MB
                cpu = proc.info['cpu_percent'] if proc.info['cpu_percent'] > 0 else 0.1  # Avoid showing zero for active processes
                process_info.append({
                    'name': name,
                    'ram': f"{ram}MB",
                    'cpu': f"{cpu}%"
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return process_info

    def toggle_view_processes(self):
        if self.view_mode:
            self.process_list.clear()
            self.view_button.setText('View Processes')
            self.view_mode = False
        else:
            self.show_processes()
            self.view_button.setText('Hide Processes')
            self.view_mode = True

    def show_processes(self):
        self.process_list.clear()
        self.processes = self.get_process_info()  # Fetch process info
        for proc in self.processes:
            display_text = f"{proc['name']:<20} {proc['ram']:<8} {proc['cpu']:<4}"
            self.process_list.addItem(display_text)

    def send_process_info(self, item):
        if self.serial_port and self.serial_port.is_open:
            index = self.process_list.row(item)
            if index < len(self.processes):
                proc = self.processes[index]
                message = f"{proc['name']:<20} {proc['ram']:<8} {proc['cpu']:<4}"
                self.serial_port.write((message + '\n').encode())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SerialConnector()
    window.show()
    sys.exit(app.exec())
