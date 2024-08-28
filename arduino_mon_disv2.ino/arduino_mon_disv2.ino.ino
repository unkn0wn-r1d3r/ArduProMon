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

void setup() {
  Serial.begin(115200);
  pinMode(TFT_LED, OUTPUT);
  digitalWrite(TFT_LED, HIGH);

  tft.begin();
  tft.setRotation(1);
  tft.fillScreen(ILI9341_BLACK);
  displayStandbyText();
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
      tft.fillScreen(ILI9341_BLACK);
      displayProcessInfo(data);
    }
  }
}

void displayProcessInfo(String data) {
  tft.setTextColor(ILI9341_WHITE);
  tft.setFont(&FreeSansBold12pt7b);

  // Split the data into lines
  int y = 0;
  int lineHeight = 16; // Adjust if needed
  String line = "";
  int maxWidth = tft.width();
  int maxHeight = tft.height();
  
  // Split data into lines
  for (int i = 0; i < data.length(); i++) {
    char c = data[i];
    if (c == '\n') {
      // Center the line horizontally
      int textWidth = getTextWidth(line);
      int x = (maxWidth - textWidth) / 2;
      
      tft.setCursor(x, y);
      tft.println(line);
      y += lineHeight;
      
      line = "";
      if (y >= maxHeight) {
        // Clear and reset if the text goes out of bounds
        tft.fillScreen(ILI9341_BLACK);
        y = 0;
      }
    } else {
      line += c;
    }
  }
  
  if (line.length() > 0) {
    // Center the last line horizontally
    int textWidth = getTextWidth(line);
    int x = (maxWidth - textWidth) / 2;
    
    tft.setCursor(x, y);
    tft.println(line);
  }
}

int getTextWidth(String text) {
  int16_t x, y;
  uint16_t w, h;
  tft.getTextBounds(text.c_str(), 0, 0, &x, &y, &w, &h);
  return w;
}

void displayStandbyText() {
  tft.setTextColor(ILI9341_WHITE);
  tft.setCursor(0, 0);
  tft.setRotation(3);
  tft.setFont(&FreeSansBold18pt7b);

  // Center the text horizontally and vertically
  String line1 = "Tukzo.com";
  String line2 = "Scan For Invoice";
  
  int line1Width = getTextWidth(line1);
  int line2Width = getTextWidth(line2);
  
  int centerX = tft.width() / 2;
  int centerY = tft.height() / 2;

  // Calculate vertical position
  int line1Y = centerY - 30;
  int line2Y = centerY + 10;

  tft.setCursor(centerX - line1Width / 2, line1Y);
  tft.println(line1);
  tft.setCursor(centerX - line2Width / 2, line2Y);
  tft.println(line2);
}
