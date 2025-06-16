#include <WiFi.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>

#define SSID "TOPNET_VSKC"
#define PASSWORD "a47qhmlwxy"

AsyncWebServer server(80);
AsyncWebSocket ws("/ws");

unsigned long lastTime = 0;
unsigned long timerDelay = 500;

void handle_recieved_msg(String message){
  Serial.println(message);
}

void initWiFi(char* ssid, char* password) {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi ..");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(1000);
  }
  Serial.println(WiFi.localIP());
}

void onEvent(AsyncWebSocket *server, AsyncWebSocketClient *client, AwsEventType type, void *arg, uint8_t *data, size_t len){
  switch (type)
  {
  case WS_EVT_CONNECT:
    Serial.printf("WebSocket client #%u connected\n", client->id());
    break;
  case WS_EVT_DISCONNECT:
    Serial.printf("WebSocket client #%u disconnected\n", client->id());
    break;
  case WS_EVT_DATA:
    AwsFrameInfo *info = (AwsFrameInfo *)arg;
    if (info->final && info->index == 0 && info->len == len && info->opcode == WS_TEXT)
    {
      data[len] = 0;
      String message = (char*)data;
      handle_recieved_msg(message);
    }
    break;
  }
}

void send_msg(String msg){
    ws.textAll(msg);
}

void setup()
{
  Serial.begin(115200);
  initWiFi(SSID, PASSWORD);
  ws.onEvent(onEvent);
  server.addHandler(&ws);

  server.begin();
}

void loop()
{
  ws.cleanupClients();
}