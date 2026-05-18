# AI Behavioral Surveillance System

## Overview

AI Behavioral Surveillance System is a real-time intelligent surveillance platform built using YOLOv8, ByteTrack, FastAPI, and React.

The system performs:

* Real-time human detection
* Persistent multi-person tracking
* Behavioral threat scoring
* Loitering detection
* Live surveillance streaming
* Incident generation
* Dynamic threat visualization dashboard

Unlike traditional object detection systems, this project focuses on behavioral analytics and suspicious activity monitoring.

---

# Features

## Real-Time Human Detection

* Detects only humans using YOLOv8
* Filters out unnecessary object detections
* Optimized for surveillance environments

---

## Persistent Person Tracking

* Uses ByteTrack for ID-based tracking
* Assigns unique IDs to detected individuals
* Tracks movement continuously across frames

---

## Behavioral Threat Analysis

Each tracked person receives a dynamic threat score based on:

* Duration in monitored zone
* Loitering behavior
* Continuous presence
* Behavioral escalation logic

Threat levels:

* LOW
* MEDIUM
* HIGH

---

## Loitering Detection

The system identifies suspicious lingering behavior.

Example:

* Standing in the same area for extended duration
* Repeated presence inside monitored zones

Generated activities:

* NORMAL
* LOITERING
* SUSPICIOUS

---

## Live Threat Dashboard

Interactive React-based dashboard displaying:

* Live surveillance feed
* Threat overlays
* Incident logs
* Real-time risk analytics
* Behavioral alerts

---

# Tech Stack

## Frontend

* React
* Vite
* JavaScript

## Backend

* FastAPI
* OpenCV
* NumPy

## AI / Vision

* YOLOv8
* ByteTrack
* Ultralytics

---

# Project Architecture

Screen Share Stream
↓
Frontend Frame Capture
↓
FastAPI Backend
↓
YOLOv8 Person Detection
↓
ByteTrack Multi-Object Tracking
↓
Behavioral Threat Analysis
↓
Incident Generation
↓
Live Dashboard Visualization

---

# Folder Structure

```bash
Video-Surveillance/
│
├── backend/
│   ├── detector/
│   │   ├── inference.py
│   │   └── threat_analysis.py
│   │
│   ├── app.py
│   ├── shared_frame.py
│   └── threat_state.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── StatsCard.jsx
│   │   │   └── EventLog.jsx
│   │   │
│   │   └── App.jsx
│
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone <your-repository-url>
cd Video-Surveillance
```

---

# Backend Setup

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Virtual Environment

### Windows

```bash
venv\\Scripts\\activate
```

---

## Install Dependencies

```bash
pip install fastapi uvicorn ultralytics opencv-python numpy python-multipart
```

---

## Run Backend

```bash
uvicorn app:app --reload
```

Backend runs on:

```bash
http://127.0.0.1:8000
```

---

# Frontend Setup

## Install Dependencies

```bash
npm install
```

---

## Run Frontend

```bash
npm run dev
```

Frontend runs on:

```bash
http://localhost:5173
```

---

# Usage

1. Start backend server
2. Start frontend server
3. Open dashboard in browser
4. Click "Share Screen"
5. Select screen/window to monitor
6. Observe:

   * Live tracking
   * Threat scoring
   * Behavioral alerts
   * Incident generation

---

# Threat Scoring Logic

Threat score increases based on:

* Loitering duration
* Persistent presence
* Behavioral escalation

Example:

* NORMAL → LOW RISK
* LOITERING → MEDIUM RISK
* SUSPICIOUS → HIGH RISK

---

# Future Enhancements

* Pose estimation
* Violence detection
* Weapon detection
* Restricted zone intrusion
* Running detection
* Crowd anomaly analysis
* Theft behavior analysis
* Multi-camera support
* Database integration
* Alert notifications

---

# Research Applications

* Smart surveillance
* Security analytics
* Behavioral AI systems
* Crowd monitoring
* Threat detection systems
* Public safety systems

---

# Disclaimer

This project is a prototype research and educational surveillance system intended for academic and learning purposes.

Threat scores are heuristic-based and designed for demonstration purposes.

---

# Authors

Developed as an AI-powered behavioral surveillance research project using computer vision and real-time analytics.
