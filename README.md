# 🚀 FastAPI WebSocket Private Chat (POC)

This project is a simple **WebSocket-based private messaging system** built using FastAPI.

It supports:

* 🔌 Real-time WebSocket connections
* 👥 Multiple clients
* 📩 Direct (user-to-user) messaging
* 📢 Optional broadcast messaging

---

## 📦 Requirements

* Python 3.10+
* pip

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

---

### 2. Create virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

---

### 3. Install dependencies

```bash
pip install fastapi uvicorn[standard]
```

---

## ▶️ Running the server

```bash
uvicorn main:app --reload
```

Server will start at:

```
http://127.0.0.1:8000
```

---

## 🧪 Testing WebSocket (Browser Console)

Open **3 browser tabs** → open DevTools → Console

---

### 👤 User 1

```js
let ws1 = new WebSocket("ws://localhost:8000/ws/1");

ws1.onmessage = (e) => console.log("User1:", e.data);
```

---

### 👤 User 2

```js
let ws2 = new WebSocket("ws://localhost:8000/ws/2");

ws2.onmessage = (e) => console.log("User2:", e.data);
```

---

### 👤 User 3

```js
let ws3 = new WebSocket("ws://localhost:8000/ws/3");

ws3.onmessage = (e) => console.log("User3:", e.data);
```

---

## 📩 Sending Messages (Private Chat)

### Send from User 1 → User 2

```js
ws1.send(JSON.stringify({
    to: 2,
    message: "Hello User 2!"
}));
```

---

## ✅ Expected Behavior

| Sender | Receiver | Output                    |
| ------ | -------- | ------------------------- |
| User 1 | User 2   | Receives message          |
| User 1 | User 1   | Sees confirmation         |
| User 3 | ❌        | Does NOT receive anything |

---

## 📡 Message Format

All messages must be JSON:

```json
{
  "to": <client_id>,
  "message": "your message"
}
```

---

## ⚠️ Notes

* If target user is not connected → message is ignored
* Multiple connections per user are not handled (POC limitation)
* No authentication enabled (can be added later)

---

## 🧠 Tech Stack

* FastAPI
* WebSockets
* Uvicorn

---

## 👨‍💻 Author

Built as a Proof of Concept for real-time communication.

---
