from application import app
from flask_cors import CORS

CORS(app)

if __name__ == '__main__':
    # Run the Flask application
    app.run(debug=True, port=2000, host='0.0.0.0')
