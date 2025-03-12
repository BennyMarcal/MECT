#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <SPI.h>
#include <SD.h>
#include <Adafruit_NeoPixel.h>
#include <WiFi.h>
#include <WebServer.h>

#define BME280_I2C_ADDRESS 0x76 // Default I2C address for BME280
#define SD_CS_PIN 5
#define LED_PIN 14
#define NUMPIXELS 1
#define WIFI_SSID "yourSSID"
#define WIFI_PASSWORD "yourPASSWORD"

Adafruit_BME280 bme; // I2C
File dataFile;
Adafruit_NeoPixel pixels(NUMPIXELS, LED_PIN, NEO_GRB + NEO_KHZ800);
WebServer server(80);
WebSocketsServer webSocket = WebSocketsServer(81);

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22); // SDA, SCL
  if (!bme.begin(BME280_I2C_ADDRESS)) {
    Serial.println("Could not find a valid BME280 sensor, check wiring!");
    while (1);
  }

  if (!SD.begin(SD_CS_PIN)) {
    Serial.println("SD card initialization failed!");
    return;
  }

  pixels.begin();

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected.");

  server.on("/", HTTP_GET, handleRoot);
  server.on("/data", HTTP_GET, handleDataRequest);
  server.begin();
  Serial.println("HTTP server started.");

  webSocket.begin();
  webSocket.onEvent(webSocketEvent);
  Serial.println("WebSocket server started.");
}

void loop() {
  logData();
  displayData();
  server.handleClient();
  webSocket.loop();
  delay(10000);
}

void logData() {
  float temperature = bme.readTemperature();
  float humidity = bme.readHumidity();
  float pressure = bme.readPressure() / 100.0F;

  dataFile = SD.open("datalog.txt", FILE_WRITE);
  if (dataFile) {
    dataFile.print("Temperature: ");
    dataFile.print(temperature);
    dataFile.print(" *C, Humidity: ");
    dataFile.print(humidity);
    dataFile.print(" %, Pressure: ");
    dataFile.print(pressure);
    dataFile.println(" hPa");
    dataFile.close();
  } else {
    Serial.println("Error opening datalog.txt");
  }

  String jsonData = "{\"temperature\":" + String(temperature) + ",\"humidity\":" + String(humidity) + ",\"pressure\":" + String(pressure) + "}";
  webSocket.broadcastTXT(jsonData);

  if (temperature > 30) {
    pixels.setPixelColor(0, pixels.Color(255, 0, 0)); // Red for high temp
  } else if (pressure < 1000) {
    pixels.setPixelColor(0, pixels.Color(0, 0, 255)); // Blue for low pressure
  } else {
    pixels.setPixelColor(0, pixels.Color(0, 255, 0)); // Green for normal conditions
  }
  pixels.show();
}

void displayData() {
  float temperature = bme.readTemperature();
  float humidity = bme.readHumidity();
  float pressure = bme.readPressure() / 100.0F;

  String html = "<!DOCTYPE html><html><head><title>Weather Station</title>"
                "<style>body { font-family: Arial, sans-serif; text-align: center; }"
                "#data { display: flex; justify-content: center; }"
                "#chart { width: 100%; max-width: 600px; height: 400px; }"
                "</style>"
                "<script src='https://cdn.jsdelivr.net/npm/chart.js'></script>"
                "<script>"
                "var ws = new WebSocket('ws://' + window.location.hostname + ':81');"
                "ws.onmessage = function(event) {"
                "  var data = JSON.parse(event.data);"
                "  updateChart(data);"
                "};"
                "var temperatureData = [], humidityData = [], pressureData = [], labels = [];"
                "function updateChart(data) {"
                "  var now = new Date();"
                "  labels.push(now.toLocaleTimeString());"
                "  if (labels.length > 20) { labels.shift(); }"
                "  temperatureData.push(data.temperature);"
                "  if (temperatureData.length > 20) { temperatureData.shift(); }"
                "  humidityData.push(data.humidity);"
                "  if (humidityData.length > 20) { humidityData.shift(); }"
                "  pressureData.push(data.pressure);"
                "  if (pressureData.length > 20) { pressureData.shift(); }"
                "  chart.update();"
                "}"
                "window.onload = function() {"
                "  var ctx = document.getElementById('chart').getContext('2d');"
                "  window.chart = new Chart(ctx, {"
                "    type: 'line',"
                "    data: {"
                "      labels: labels,"
                "      datasets: [{ label: 'Temperature (°C)', data: temperatureData, borderColor: 'red', fill: false },"
                "                 { label: 'Humidity (%)', data: humidityData, borderColor: 'blue', fill: false },"
                "                 { label: 'Pressure (hPa)', data: pressureData, borderColor: 'green', fill: false }]"
                "    },"
                "    options: { scales: { x: { type: 'time', time: { unit: 'second' } }, y: { beginAtZero: false } } }"
                "  });"
                "};"
                "</script></head><body>"
                "<h1>Weather Station</h1>"
                "<div id='data'>"
                "<canvas id='chart'></canvas>"
                "</div>"
                "</body></html>";
  
  server.send(200, "text/html", html);
}

void handleDataRequest() {
  float temperature = bme.readTemperature();
  float humidity = bme.readHumidity();
  float pressure = bme.readPressure() / 100.0F;

  String jsonData = "{\"temperature\":" + String(temperature) + ",\"humidity\":" + String(humidity) + ",\"pressure\":" + String(pressure) + "}";
  server.send(200, "application/json", jsonData);
}


