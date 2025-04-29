# 💡 IoT Light Scheduler

A smart, browser-based light automation system that blends **WebSocket** and **MQTT** technologies for reliable, real-time scheduling. Designed to work seamlessly with **Arduino UNO** and a **relay module**, this setup puts control right at your fingertips.

---

## ✨ Key Features

- ⚡ **Modern, Responsive Interface** – Built with Tailwind CSS for a smooth and mobile-friendly experience  
- 🌐 **Real-Time Communication** – Uses WebSocket to manage and broadcast scheduling commands  
- 📱 **MQTT Integration** – Light control that's perfectly timed and scalable for IoT environments  
- 🔌 **Hardware Control** – Lights switch via Arduino UNO and a relay module for a practical, hands-on setup  

---

## 💪 Getting Started

### 🔧 Arduino Hardware Configuration

1. **Wiring the Relay Module:**
   - **VCC → 5V**
   - **GND → GND**
   - **IN → Pin 8 on Arduino**
   - Connect your **light's live wire** between **COM and NO** on the relay. Use proper insulation ⚠️

2. **Uploading the Code to Arduino:**

```cpp
int relayPin = 8;

void setup() {
  Serial.begin(9600);
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, HIGH); // Light OFF at startup
}

void loop() {
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    if (cmd == "ON") {
      digitalWrite(relayPin, LOW);  // Light ON
    } else if (cmd == "OFF") {
      digitalWrite(relayPin, HIGH); // Light OFF
    }
  }
}
```

---

## 🚀 How It Works

- The **WebSocket server** handles schedule logic and user input from the frontend.
- Upon a triggered schedule, it sends a signal via **MQTT** to the connected Arduino device.
- The **Arduino**, listening through the serial connection, interprets "ON" or "OFF" commands to toggle the relay—and your light.

---

## ⚙️ Future Enhancements

- Add authentication and user profiles 🛡️  
- Integrate a real-time clock (RTC) for offline scheduling support 🕒  
- Expand to multiple relays for room-by-room control 🏠
