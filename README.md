# 🎧 Video to MP3 Converter – Microservices Application

A distributed, cloud-native microservices project that allows users to upload videos and receive their converted MP3s. Built using Docker, Kubernetes, Flask, RabbitMQ, GridFS, and MySQL, the system ensures asynchronous processing, secure authentication, and efficient delivery of audio files.

---

## 🗺️ Architecture Overview

![Architecture Diagram](<img width="1703" height="849" alt="Screenshot 2025-07-28 at 4 36 49 pm" src="https://github.com/user-attachments/assets/00b509d0-7ba5-434e-ae1d-bb17f99b1af0" />
)

> All services run in a Kubernetes cluster and communicate via RabbitMQ and REST APIs.

---

## ⚙️ Tech Stack

| Layer           | Stack/Tool                         |
|----------------|-------------------------------------|
| API Framework   | Flask                               |
| Authentication  | JWT + MySQL                         |
| File Storage    | MongoDB + GridFS                    |
| Queue           | RabbitMQ (video & mp3 queues)       |
| Notification    | SMTP (e.g., Gmail/Mailtrap)         |
| Containerization| Docker                              |
| Orchestration   | Kubernetes via Minikube             |
| Gateway         | NGINX                               |
| DevOps          | K9s (for pod monitoring)            |

---

## 🚀 How It Works

1. The **client** uploads a video via the **API Gateway**.
2. The **API Gateway** forwards the request to the **Auth Service**, which:
   - Verifies the **JWT token**.
   - Checks credentials in the **MySQL database**.
   - Approves/rejects the request based on authentication result.
3. If authenticated, the **API Gateway** pushes the request to the **`video` queue** in RabbitMQ.
4. The **Converter Service** (consumer of the `video` queue):
   - Converts the video to MP3 using `ffmpeg`.
   - Uploads the MP3 to **MongoDB using GridFS**.
   - Extracts the MP3's **ObjectID** and pushes it to the **`mp3` queue**.
5. The **Notification Service** (consumer of the `mp3` queue):
   - Sends an email to the user containing the **GridFS ObjectID**.
6. The **User** takes this ObjectID and sends a **GET request** to the **API Gateway**.
   - The request is routed via **NGINX**.
   - The **Gateway** fetches the MP3 using the ObjectID from GridFS and returns it to the client.

---

## 🧱 Microservices Overview

### 📌 API Gateway
- Entry point for all user requests.
- Routes traffic to internal services using NGINX.
- Delegates authentication to the `auth-service`.
- Pushes jobs to RabbitMQ queues.
- Handles video upload and MP3 download logic.

### 🔐 Auth Service
- Responsible for **authentication and authorization**.
- Verifies user tokens and credentials.
- Interacts with the **MySQL** database.
- Used by the **API Gateway** to validate users.

### 🎥 Converter Service
- Consumes jobs from the **`video` queue**.
- Converts video to MP3 using `ffmpeg`.
- Uploads MP3 to **MongoDB (GridFS)**.
- Publishes a message to the **`mp3` queue** with the MP3's ObjectID.

### 📧 Notification Service
- Consumes jobs from the **`mp3` queue**.
- Sends an email containing the MP3's ObjectID.
- Email does **not** contain a direct download link, but an ID the user can use to fetch the MP3 later.

---

## 🛠️ Setup & Deployment

### 🔃 Prerequisites

- Docker
- Minikube
- kubectl
- Python 3.9+
- `ffmpeg` installed locally
- SMTP credentials (Gmail or Mailtrap recommended)

---

### 📦 Clone & Launch

```bash
git clone https://github.com/Abzaek/video_to_mp3.git
cd <repo-name>

# Start Minikube
minikube start

# Deploy all services
kubectl apply -f k8s/

# Monitor pods
k9s
