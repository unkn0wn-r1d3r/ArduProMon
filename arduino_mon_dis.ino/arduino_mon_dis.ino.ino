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
  Serial.begin(9600);
  tft.begin();
  tft.setRotation(3);  // Adjust the rotation as needed
  tft.fillScreen(ILI9341_BLACK);
  tft.setTextColor(ILI9341_WHITE);
  tft.setTextSize(1);
}

void loop() {
  if (Serial.available()) {
    String data = "";
    while (Serial.available()) {
      char c = Serial.read();
      data += c;
      delay(10); // Adjust delay as needed
    }

    tft.fillScreen(ILI9341_BLACK);
    tft.setCursor(0, 0);
    tft.setTextSize(1);
    tft.print(data);
  }
}
