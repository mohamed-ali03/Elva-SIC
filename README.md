# Elva Smart Elevator System

This project implements a **smart elevator system** using **Raspberry Pi**, sensors, and IoT integration. It combines **ultrasonic distance measurement**, **DHT22 temperature/humidity sensing**, **motor control**, and **real-time dashboard updates** via MQTT and Adafruit IO.

---

## Features

- Detects **people waiting at floors** using an ultrasonic sensor.  
- Moves the elevator automatically between floors using **DC motors**.  
- Opens and closes the **elevator door** using a servo motor.  
- Reads **temperature and humidity** with a DHT22 sensor.  
- Publishes system data to **MQTT** and **Adafruit IO dashboard**.  
- Multi-threaded architecture for **simultaneous operations**.  

---

## Hardware Components

- **Raspberry Pi** (main controller)  
- **Ultrasonic sensor** (HC-SR04) – distance measurement to detect floors  
- **DC Motor + Motor Driver** – moves the elevator  
- **Servo Motor** – controls door opening/closing  
- **DHT22 Sensor** – temperature and humidity sensing  

---

## Software Components

- Python 3  
- Libraries:
  - `Adafruit_DHT` – for DHT22 sensor  
  - `threading` – for multi-threading  
  - `time` – for delays  
  - `MQTT Publisher` – for IoT messaging  
  - `Adafruit IO` – cloud dashboard integration  

---

## Code Structure

### Import Section
- Imports all modules for sensors, motors, MQTT, and dashboard.  

### Global Variables
- **Pin configuration:** GPIO pins for sensors and motors.  
- **Locks:** Threading locks to avoid race conditions.  
- **Elevator motion variables:** `currentfloor`, `desiredfloors`, `ultradistance`.  
- **DHT variables:** `temperature`, `humidity`.  
- **MQTT and Dashboard objects:** `mqttPUB`, `dashboard`.  

### Supported Functions

- `getDesiredDoorNumber(distance)` – maps ultrasonic distance to a floor number.  

### Thread Functions

1. **`getDoors()`**  
   - Continuously reads the ultrasonic sensor.  
   - Determines the floor number based on distance.  
   - Adds the floor to `desiredfloors` if it’s not already in the list.  
   - Uses `desiredfloorsLock` to avoid race conditions.  

2. **`moveElevator()`**  
   - Moves the elevator to the next floor in `desiredfloors`.  
   - Controls **DC motor** for movement and **servo motor** for door.  
   - Updates `currentfloor` after reaching a floor.  
   - Thread-safe with locks.  

3. **`getTempHumid()`**  
   - Continuously reads temperature and humidity from the DHT22 sensor.  
   - Uses `humidityTemperatureLock` for thread safety.  

4. **`pubMQTTMasseg()`**  
   - Publishes current elevator status to MQTT topic.  

5. **`pubAdafruitDashboard()`**  
   - Sends temperature, humidity, and floor information to Adafruit IO dashboard.  

---

## Main Execution

- Starts threads for:
  - `getDoors()` – floor detection  
  - `moveElevator()` – elevator movement  
  - `getTempHumid()` – sensor reading  
  - `pubMQTTMasseg()` – MQTT publishing  
  - `pubAdafruitDashboard()` – dashboard updates  
- Joins all threads to keep the program running continuously.  

---

## Notes

- The system uses **locks** to prevent race conditions in shared resources (`desiredfloors`, `currentfloor`, `temperature`, `humidity`, `doorstatus`).  
- The elevator movement loop dynamically handles new floor requests in real-time.  
- The door opens for **15 seconds** and closes automatically.  

---

## Contributors

- **Mohamed Ali**  
- **Maram Mohab**  
- **Tawfiq**
- **Sarah Gamal**
---
