#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ILI9341.h>
#include <Fonts/FreeSansBold18pt7b.h>
#include <Fonts/FreeSansBold12pt7b.h>

#define TFT_CS   9
#define TFT_DC   8
#define TFT_RST  7
#define TFT_LED  6

Adafruit_ILI9341 tft = Adafruit_ILI9341(TFT_CS, TFT_DC, TFT_RST);

// Define thresholds for highlighting
#define RAM_THRESHOLD 10000000 // 10 MB
#define CPU_THRESHOLD 80 // 80%

unsigned long lastUpdateTime = 0; // To track when to update
const unsigned long updateInterval = 2000; // 2 seconds

void setup() {
  Serial.begin(115200);
  pinMode(TFT_LED, OUTPUT);
  digitalWrite(TFT_LED, HIGH);

  tft.begin();
  tft.setRotation(3);
  tft.fillScreen(ILI9341_BLACK);
  displayTableHeader();
  Serial.println("READY");
}

void loop() {
  checkSerial();
}

void checkSerial() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    data.trim();

    if (data.length() > 0) {
      unsigned long currentTime = millis();
      if (currentTime - lastUpdateTime >= updateInterval) {
        tft.fillRect(0, 20, tft.width(), tft.height() - 20, ILI9341_BLACK); // Clear table area
        updateProcessInfo(data);
        lastUpdateTime = currentTime; // Update the last update time
      }
    }
  }
}

void displayTableHeader() {
  tft.setTextColor(ILI9341_WHITE);
  tft.setFont(&FreeSansBold12pt7b);
  
  tft.setCursor(10, 20);
  tft.print("Program| RAM| CPU");
  tft.drawLine(10, 30, tft.width() - 10, 30, ILI9341_WHITE); // Draw line under header
}

void updateProcessInfo(String data) {
  tft.setFont(&FreeSansBold12pt7b);
  int y = 40;
  int lineHeight = 16; // Adjust if needed

  // Split data into lines and update
  int startIndex = 0;
  while (startIndex < data.length()) {
    int endIndex = data.indexOf('\n', startIndex);
    if (endIndex == -1) endIndex = data.length();
    
    String line = data.substring(startIndex, endIndex);
    startIndex = endIndex + 1;

    // Parse line
    int nameEnd = line.indexOf(' ');
    String name = line.substring(0, nameEnd);
    String rest = line.substring(nameEnd + 1);
    
    int ramEnd = rest.indexOf(' ');
    String ram = rest.substring(0, ramEnd);
    String cpu = rest.substring(ramEnd + 1);

    // Set colors based on thresholds
    int ramValue = ram.toInt();
    int cpuValue = cpu.toInt();

    if (ramValue > RAM_THRESHOLD) {
      tft.setTextColor(ILI9341_RED); // Highlight RAM usage
    } else if (cpuValue > CPU_THRESHOLD) {
      tft.setTextColor(ILI9341_YELLOW); // Highlight CPU usage
    } else {
      tft.setTextColor(ILI9341_WHITE); // Default color
    }
    
    // Draw the text
    tft.setCursor(10, y);
    tft.print(name);
    tft.setCursor(150, y);
    tft.print(ram);
    tft.setCursor(210, y);
    tft.print(cpu);

    y += lineHeight;
    if (y >= tft.height()) {
      y = 40; // Reset position if it goes beyond screen
      tft.fillRect(0, 40, tft.width(), tft.height() - 40, ILI9341_BLACK); // Clear old text
    }
  }
}
