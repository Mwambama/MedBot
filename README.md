
# 💊 MedBot – Automated Medication Delivery System

![Technical Sketch](./Capture.PNG)

## 📦 Description

**MedBot** is a smart, autonomous medication delivery robot that reduces human error in hospitals. It autonomously navigates hallways, interacts with pharmacists and nurses, and delivers prescriptions directly to patients—reducing workload, saving time, and improving patient safety. It also features real-time location tracking through a Python GUI, and plays audio feedback upon task completion so staff know where it is, even if it’s not in sight.

---

## ⚙️ Features

* **Central MedBot Hub**
  Coordinates sensor input, navigation, and task execution.

* **Sensor Subsystems (IR & Bumpers)**
  Detect nearby objects, people, and emergency collisions.

* **Software Control Center**
  Processes sensor data and determines real-time movement and decisions.

* **UART Interface**
  Sends task updates and receives commands from external systems.

* **Obstacle Detection & Redirection Logic**
  Avoids people or objects using bumpers and ping sensors, and reroutes intelligently.

* **Pharmacy, Patients, and Navigation Zones**
  Recognizes zones by object size and structure, delivering medication accordingly.

* **Audio Feedback**
  Plays music/sounds to signal arrival or completion of a delivery.

* **Real-Time Python GUI**
  Displays MedBot’s current location and task status via sensor socket communication.

---

## 🧪 Usage Workflow

1. Start at the **Destination Zone**
2. Navigate to the **Pharmacy Pillar** using IR detection
3. Pharmacist inputs patient info via **LCD buttons**
4. Navigate through **hospital hallway**, avoiding obstacles
5. Identify **correct patient bed** via IR/Ping object sizing
6. Ask patient for medication confirmation using **LCD**
7. Deliver medication and play completion **sound**
8. Update **Python GUI** with MedBot’s location
9. Return to **Start Zone**

---

## 🎯 Motivation

Medication errors are one of the most preventable causes of harm in healthcare. MedBot reduces these risks by automating medication delivery—eliminating common issues like fatigue, miscommunication, and workload-induced mistakes.

---

## 📋 Problem Statement

Hospital staff are overworked and susceptible to errors in delivering medications. This problem leads to patient harm and emotional and legal consequences for staff. **MedBot reduces these risks** by automating the most error-prone tasks and freeing medical staff to focus on patient care.

---

## 🔧 Tools & Technologies

* **Tiva™ TM4C123GH6PM microcontroller**
* **UART Communication**
* **ADC for sensor input**
* **Timers for PWM motor control**
* **C Programming**
* **CPRE 288 Trainer Kit**
* **LCD Interface with button selection**
* **Ping & bumper sensors for obstacle detection**
* **Python GUI using sensor socket (TCP) for live MedBot location updates**
* **Audio module for feedback sounds**

---

## 🖼️ Architecture Overview

* **Central MedBot Hub**
* **IR/Ping Sensors & Bumpers**
* **UART + LCD interface**
* **Navigation Logic**
* **Zone Recognition: Pharmacy, Nurse, Patient Beds**
* **Python Sensor Socket GUI**

---

## 🛠️ Project Team

* \[PG-A3]
---

## 💎 Repository & Demo

* **Video Demo:** *Add YouTube link here*

