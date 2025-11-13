# 📱 QR-Based Smart Queue Management System

This project is a digital solution designed to replace traditional physical queuing methods. It allows users to join queues remotely via QR codes, track their status in real-time, and receive notifications, significantly reducing physical overcrowding and wait times.

## 🎯 Objectives
* **Real-time Updates:** Inform users of their position and estimated wait time.
* **Remote Joining:** Users scan a QR code to join the queue without being physically present.
* **Predictive Analytics:** Analyze historical data to forecast peak hours and service loads.

## ⚙️ System Architecture

The system follows a **Spiral Model** development lifecycle and operates in three layers:
1.  **Frontend:** User interface for scanning and status tracking (HTML/CSS/JS).
2.  **Backend:** Manages queue logic, assigns tokens, and serves APIs (Python/Flask).
3.  **Database:** Stores timestamps, service history, and analytics (SQLite).

## 🛠️ Tech Stack

* **Languages:** Python, JavaScript, HTML, CSS.
* **Framework:** Flask.
* **Database:** SQLite.
* **Libraries:** `qrcode.js` (Frontend generation), Pandas & Scikit-learn (Backend analytics).
* **Algorithms:** Linear Regression & Time Series for wait-time prediction.

## 📊 Results
* **Wait Time Reduction:** Estimated 52% reduction in average waiting time.
* **Prediction Accuracy:** Achieved ~92% accuracy in queue forecasting.

## 🚀 Usage
1.  User scans the displayed QR code.
2.  Web app opens showing the current queue status.
3.  User clicks "Join Queue" and receives a digital token.
4.  Real-time updates are pushed to the user's device until their turn arrives.
