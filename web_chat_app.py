# web_chat_app.py
# Modern web-based chat application using Flask and WebSockets

from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
import os
from datetime import datetime
import uuid
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Store active users and their rooms
active_users = {}
chat_rooms = {
    'general': {
        'name': 'General Chat',
        'users': set(),
        'messages': []
    }
}

@app.route('/health')
def health_check():
    """Simple health check for Railway"""
    return jsonify({'status': 'ok', 'message': 'Chat app is running'})

@app.route('/')
def index():
    try:
        if 'username' in session:
            return redirect(url_for('chat'))
        return render_template('login.html')
    except Exception as e:
        logger.error(f"Error in index route: {e}")
        return f"Error: {str(e)}", 500

@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.form.get('username', '').strip()
        if not username:
            return render_template('login.html', error='Username is required')
        
        if username in active_users:
            return render_template('login.html', error='Username already taken')
        
        session['username'] = username
        session['user_id'] = str(uuid.uuid4())
        active_users[username] = {
            'id': session['user_id'],
            'room': 'general'
        }
        
        return redirect(url_for('chat'))
    except Exception as e:
        logger.error(f"Error in login route: {e}")
        return f"Error: {str(e)}", 500

@app.route('/logout')
def logout():
    try:
        if 'username' in session:
            username = session['username']
            if username in active_users:
                del active_users[username]
            session.clear()
        return redirect(url_for('index'))
    except Exception as e:
        logger.error(f"Error in logout route: {e}")
        return f"Error: {str(e)}", 500

@app.route('/chat')
def chat():
    try:
        if 'username' not in session:
            return redirect(url_for('index'))
        
        username = session['username']
        room = active_users.get(username, {}).get('room', 'general')
        
        return render_template('chat.html', 
                             username=username, 
                             room=room,
                             rooms=chat_rooms)
    except Exception as e:
        logger.error(f"Error in chat route: {e}")
        return f"Error: {str(e)}", 500

@socketio.on('connect')
def handle_connect():
    try:
        if 'username' in session:
            username = session['username']
            room = active_users.get(username, {}).get('room', 'general')
            join_room(room)
            chat_rooms[room]['users'].add(username)
            
            logger.info(f"User {username} connected to room {room}")
            
            # Send user joined message
            emit('user_joined', {
                'username': username,
                'timestamp': datetime.now().strftime('%H:%M'),
                'message': f'{username} joined the chat'
            }, room=room)
            
            # Send current users list
            emit('users_list', {
                'users': list(chat_rooms[room]['users'])
            }, room=room)
        else:
            logger.warning("Connection attempt without username in session")
    except Exception as e:
        logger.error(f"Error in handle_connect: {e}")

@socketio.on('disconnect')
def handle_disconnect():
    try:
        if 'username' in session:
            username = session['username']
            room = active_users.get(username, {}).get('room', 'general')
            
            if username in chat_rooms[room]['users']:
                chat_rooms[room]['users'].remove(username)
            
            if username in active_users:
                del active_users[username]
            
            logger.info(f"User {username} disconnected from room {room}")
            
            # Send user left message
            emit('user_left', {
                'username': username,
                'timestamp': datetime.now().strftime('%H:%M'),
                'message': f'{username} left the chat'
            }, room=room)
            
            # Update users list
            emit('users_list', {
                'users': list(chat_rooms[room]['users'])
            }, room=room)
    except Exception as e:
        logger.error(f"Error in handle_disconnect: {e}")

@socketio.on('send_message')
def handle_message(data):
    try:
        if 'username' not in session:
            logger.warning("Message attempt without username in session")
            return
        
        username = session['username']
        message = data.get('message', '').strip()
        room = active_users.get(username, {}).get('room', 'general')
        
        if not message:
            return
        
        # Create message object
        message_obj = {
            'username': username,
            'message': message,
            'timestamp': datetime.now().strftime('%H:%M'),
            'type': 'user_message'
        }
        
        # Store message in room history
        chat_rooms[room]['messages'].append(message_obj)
        
        # Keep only last 100 messages
        if len(chat_rooms[room]['messages']) > 100:
            chat_rooms[room]['messages'] = chat_rooms[room]['messages'][-100:]
        
        logger.info(f"Message from {username} in room {room}: {message[:50]}...")
        
        # Broadcast message to room
        emit('new_message', message_obj, room=room)
    except Exception as e:
        logger.error(f"Error in handle_message: {e}")

@socketio.on('join_room')
def handle_join_room(data):
    try:
        if 'username' not in session:
            logger.warning("Room join attempt without username in session")
            return
        
        username = session['username']
        new_room = data.get('room', 'general')
        
        # Leave current room
        current_room = active_users.get(username, {}).get('room', 'general')
        if current_room != new_room:
            leave_room(current_room)
            if username in chat_rooms[current_room]['users']:
                chat_rooms[current_room]['users'].remove(username)
        
        # Join new room
        if new_room not in chat_rooms:
            chat_rooms[new_room] = {
                'name': new_room.title(),
                'users': set(),
                'messages': []
            }
        
        join_room(new_room)
        chat_rooms[new_room]['users'].add(username)
        active_users[username] = {
            'id': session['user_id'],
            'room': new_room
        }
        
        logger.info(f"User {username} joined room {new_room}")
        
        # Send room info
        emit('room_changed', {
            'room': new_room,
            'room_name': chat_rooms[new_room]['name'],
            'users': list(chat_rooms[new_room]['users']),
            'messages': chat_rooms[new_room]['messages'][-50:]  # Last 50 messages
        })
    except Exception as e:
        logger.error(f"Error in handle_join_room: {e}")

if __name__ == '__main__':
    print("🚀 Starting Web Chat Application...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🌐 For online access, deploy this to a cloud server")
    print("📊 Logging enabled - check console for detailed information")
    
    try:
        port = int(os.environ.get('PORT', 5000))
        socketio.run(app, host='0.0.0.0', port=port, debug=True)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        print(f"❌ Error starting server: {e}") 
