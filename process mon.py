import sys
import psutil
import serial
import platform
import time

def get_process_info():
    process_info = ""
    for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_info']):
        try:
            process_info += f"{proc.info['name']}: CPU: {proc.info['cpu_percent']}%, RAM: {proc.info['memory_info'].rss / (1024 * 1024):.2f}MB\n"
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return process_info

def main():
    ser = serial.Serial('COM4', 115200)  # Update with your Arduino serial port
    while True:
        os_name = platform.system()
        process_info = get_process_info()
        data = f"OS: {os_name}\n{process_info}"
        print("Sending data to Arduino...")
        print(data)  # Print data for debugging
        ser.write((data + "\n").encode())  # Ensure newline at the end of data
        time.sleep(5)  # Send data every 5 seconds

if __name__ == "__main__":
    main()
