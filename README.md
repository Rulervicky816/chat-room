# Chat Room Project

A complete chat room solution with both **socket-based** (terminal) and **web-based** (browser) applications.

## 🚀 Quick Start

### **Option 1: Web-based Chat (Recommended)**

1. **Install dependencies:**
   ```bash
   py -m pip install flask flask-socketio
   ```

2. **Start the web server:**
   ```bash
   py web_chat_app.py
   ```

3. **Open your browser:**
   - Go to: `http://localhost:5000`
   - Enter a username and start chatting!

### **Option 2: Socket-based Chat (Terminal)**

1. **Start the server:**
   ```bash
   py server.py
   ```

2. **Open multiple terminals and run clients:**
   ```bash
   py client.py
   ```

## 📁 Project Structure

```
chat-room-project/
├── server.py          # Socket-based chat server
├── client.py          # Socket-based chat client  
├── web_chat_app.py    # Web-based chat application
├── templates/         # HTML templates for web chat
│   ├── login.html     # Login page
│   └── chat.html      # Chat interface
└── README.md          # This file
```

## 🌐 Web-based Chat Features

- ✅ **Modern web interface** - works in any browser
- ✅ **Real-time messaging** using WebSockets
- ✅ **Multiple chat rooms** (General, Random, Help)
- ✅ **User presence indicators** (who's online)
- ✅ **Mobile responsive** - works on phones/tablets
- ✅ **Message history** (last 100 messages per room)
- ✅ **Cross-platform** - works on any device with a browser

### **Web Chat Usage:**
1. Start: `py web_chat_app.py`
2. Open: `http://localhost:5000`
3. Enter username and join any room
4. Chat with other users in real-time!

## 💻 Socket-based Chat Features

- ✅ **Lightweight and fast** - minimal resource usage
- ✅ **Terminal-based** - works in any terminal
- ✅ **Real-time messaging** using TCP sockets
- ✅ **Multiple clients** can connect simultaneously
- ✅ **Username support** - each user has a unique name
- ✅ **Graceful disconnection** - clean shutdown

### **Socket Chat Usage:**
1. Start server: `py server.py`
2. Open multiple terminals
3. Run clients: `py client.py`
4. Enter usernames and start chatting!

## 🔧 Installation

### **Requirements:**
- Python 3.7 or higher
- For web chat: Flask and Flask-SocketIO

### **Install Dependencies:**
```bash
# For web chat
py -m pip install flask flask-socketio

# For socket chat (no additional dependencies needed)
# Uses only Python standard library
```

## 🎯 Usage Examples

### **Web Chat Example:**
```bash
# Start web server
py web_chat_app.py

# Open browser tabs:
# Tab 1: http://localhost:5000 (username: Alice)
# Tab 2: http://localhost:5000 (username: Bob)
# Tab 3: http://localhost:5000 (username: Charlie)
```

### **Socket Chat Example:**
```bash
# Terminal 1 - Start server
py server.py

# Terminal 2 - Client 1
py client.py
# Enter username: Alice

# Terminal 3 - Client 2  
py client.py
# Enter username: Bob

# Terminal 4 - Client 3
py client.py
# Enter username: Charlie
```

## 🌍 Deployment

### **Web Chat Deployment:**
The web chat can be deployed online using:
- **Railway** (recommended - free & easy)
- **Heroku**
- **DigitalOcean/AWS/VPS**

### **Socket Chat Deployment:**
For online access, you need:
- A server with public IP
- Port forwarding (default: 55555)
- Update client.py with server IP

## 🔒 Security Notes

- **Web Chat**: Uses Flask sessions, change SECRET_KEY for production
- **Socket Chat**: Basic implementation, add encryption for production use
- **Both**: Consider adding authentication for public deployment

## 🛠️ Troubleshooting

### **Web Chat Issues:**
- **"Module not found"**: Run `py -m pip install flask flask-socketio`
- **"Port already in use"**: Change port in web_chat_app.py
- **WebSocket errors**: Check browser console (F12)

### **Socket Chat Issues:**
- **"Connection refused"**: Make sure server is running first
- **"Address already in use"**: Wait or change port in server.py
- **Messages not appearing**: Check all clients are connected

## 📱 Comparison

| Feature | Web Chat | Socket Chat |
|---------|----------|-------------|
| **Interface** | Browser | Terminal |
| **Setup** | Install Flask | No dependencies |
| **Deployment** | Easy online | Requires server |
| **Mobile** | ✅ Yes | ❌ No |
| **UI** | Modern | Basic |
| **Speed** | Good | Very Fast |
| **Resources** | Higher | Lower |

## 🎉 Getting Started

1. **Choose your preferred method:**
   - **Web Chat**: Modern, browser-based, easy to deploy
   - **Socket Chat**: Lightweight, terminal-based, fast

2. **Follow the Quick Start guide above**

3. **Test with multiple users** to see real-time messaging

4. **Deploy online** if you want internet access

Both applications provide real-time chat functionality - choose based on your needs! 🚀 
