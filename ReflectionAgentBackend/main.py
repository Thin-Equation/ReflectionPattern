"""
Main entry point for the Reflection Agent Backend.
"""
import uvicorn
import socket
from src.config.settings import PORT, HOST, DEBUG, SSL_CERT, SSL_KEY

def is_port_in_use(port, host="localhost"):
    """Check if a port is already in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

def find_available_port(start_port, max_attempts=10):
    """Find an available port starting from start_port"""
    port = start_port
    attempts = 0
    
    while is_port_in_use(port) and attempts < max_attempts:
        port += 1
        attempts += 1
        
    if attempts >= max_attempts:
        raise RuntimeError(f"Could not find an available port after {max_attempts} attempts")
        
    return port

if __name__ == "__main__":
    # Check if the preferred port is available, otherwise find an alternative
    if is_port_in_use(PORT):
        print(f"Port {PORT} is already in use. Trying to find an available port...")
        port = find_available_port(PORT + 1)
        print(f"Found available port: {port}")
    else:
        port = PORT
        
    print(f"Starting server on port {port}")
    
    # Use uvicorn to run the FastAPI app
    uvicorn.run(
        "src.api.app:app", 
        host=HOST, 
        port=port, 
        reload=DEBUG,
        ssl_keyfile=SSL_KEY,
        ssl_certfile=SSL_CERT,
    )