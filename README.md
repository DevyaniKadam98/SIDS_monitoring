# 🍼 SIDS Monitoring System (Bachelor of Engineering Final Year Project)

This repository contains the code and documentation for my **Final Year BE Project**:  
**Real-Time Sudden Infant Death Syndrome (SIDS) Monitoring using Image Processing**.

The goal of this project is to **monitor infant breathing movements** using computer vision, and raise alerts if no breathing is detected.

---

## 📌 Overview
Sudden Infant Death Syndrome (SIDS) is the sudden, unexplained death of an infant, often during sleep. Our project proposes a prototype system that continuously monitors the baby using a camera and simple computer vision techniques.

The approach:
- Capture **real-time video** using webcam (or Raspberry Pi camera).
- Perform **frame differencing** and **pixel variation analysis**.
- Detect subtle breathing movements.
- Show results in a **Tkinter GUI**.
- Potential for integration with **alerts (buzzer, GSM, Wi-Fi)**.

---

## ⚡ Features
- GUI made with **Tkinter**.
- Two modes:
  - **Breath Detection from Images** (compare two still images).
  - **Live Breath Detection from Webcam** (real-time).
- Pixel difference method to estimate movement (breathing).
- Extendable for Raspberry Pi, GSM, buzzer alerts.

---
## Hardware 

This project was tested with:

Raspberry Pi 3B+

HDR Camera (Logitech C270 / C920)

GSM module (for SMS alerts)

Buzzer (local alarm)
