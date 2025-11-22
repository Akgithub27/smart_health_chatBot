from app.routes import app

if __name__ == "__main__":
    print("=" * 50)
    print("Smart Healthcare Chatbot - Starting...")
    print("=" * 50)
    print("Access the application at: http://127.0.0.1:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    app.run(debug=True, host='127.0.0.1', port=5000)