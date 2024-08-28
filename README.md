<h1>ArduProMon</h1>

![image](https://github.com/user-attachments/assets/063d095f-81ef-4b94-a740-2f26b6f85c33)

<p>A project Developed using pyside6 ,python, arduino nano and 2.8TFT Color Display to show background process to the display realtime and show color based warning if program utilize over resources.</p>
<h3>Compactable OS</h3>
 <ol>
  <li>Windows (Tested ,working)</li>
  <li>Linux</li>
  <li>Mac</li>
</ol> 

<h3>Dependency</h3>
<p> Application : python 3 ,pip install pyserial psutil pyside6 </p>
<p>Hardware : Arduino nano ,2.8 inch SPI Screen Module TFT Interface 240 x 320 without Touch , usb cable to connect. </p>

<p>Arduino Libraries</p> 
<p>Adafruit GFX Library:  Provides core graphics functions for drawing on the display.</p>
<p>Adafruit ILI9341 Library: Specific driver for the ILI9341 TFT display.</p>

<h2>TFT Display Pin Layout</h2>
    <table>
        <thead>
            <tr>
                <th>Pin Name</th>
                <th>Arduino Nano Pin</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>TFT_CS (Chip Select)</td>
                <td>9</td>
                <td>Selects the TFT display for communication</td>
            </tr>
            <tr>
                <td>TFT_DC (Data/Command)</td>
                <td>8</td>
                <td>Indicates whether the data being sent is a command or data</td>
            </tr>
            <tr>
                <td>TFT_RST (Reset)</td>
                <td>7</td>
                <td>Resets the TFT display</td>
            </tr>
            <tr>
                <td>TFT_LED (Backlight)</td>
                <td>6</td>
                <td>Controls the backlight of the TFT display</td>
            </tr>
        </tbody>
    </table>
<h3>Serial Communication</h3>

<p> Linux: Serial communication generally works well on Linux, but the serial device names are different. On Linux, serial devices are usually located at /dev/ttyUSB0, /dev/ttyS0, etc. </p>
<p>macOS: On macOS, serial devices are typically found at /dev/tty.usbserial-*, /dev/tty.usbmodem-*, etc. </p>
