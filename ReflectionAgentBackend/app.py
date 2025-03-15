from flask import Flask, request, jsonify
from flask_cors import CORS
from reflection_agent import ReflectionPatternAgent
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app=app)  # Enable Cross-Origin Resource Sharing (CORS)

# Initialize the ReflectionPatternAgent
agent = ReflectionPatternAgent(
    google_api_key= os.environ.get("GEMINI_API_KEY", "your_api_key_here"),  # Replace with your Google API key
    verbose=True  # Set to True for debugging/logging agent activity
)

@app.route('/api/query', methods=['POST'])
def query_agent():
    """
    Endpoint to handle queries sent by the frontend.
    """
    data = request.json  # Parse JSON data from the request
    query = data.get('query', '')  # Extract the query string from the request

    if not query:
        return jsonify({"error": "No query provided"}), 400

    try:
        # Run the agent with the provided query
        result = agent.run(query)

        # Format messages for frontend display
        formatted_messages = []
        for msg in result.get('messages', []):
            if hasattr(msg, 'type'):
                msg_type = msg.type
            else:
                # Determine message type based on class name
                if 'SystemMessage' in str(type(msg)):
                    msg_type = 'system'
                elif 'HumanMessage' in str(type(msg)):
                    msg_type = 'human'
                elif 'AIMessage' in str(type(msg)):
                    msg_type = 'ai'
                else:
                    msg_type = 'unknown'

            formatted_messages.append({
                'type': msg_type,
                'content': msg.content if hasattr(msg, 'content') else str(msg)
            })

        # Return the response to the frontend
        return jsonify({
            'response': result.get('response', ''),
            'iterations': result.get('iterations', 0),
            'messages': formatted_messages
        })

    except Exception as e:
        # Handle errors gracefully and return an error message
        return jsonify({
            "error": f"Error processing query: {str(e)}"
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify server status.
    """
    return jsonify({"status": "Server is running"}), 200


if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc')
