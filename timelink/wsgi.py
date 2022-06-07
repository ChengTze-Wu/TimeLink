# separate file for Gunicorn to run
from app import app

if __name__ == "__main__":
    app.run(port=3000, debug=True)