from app import create_app
from app.config import Configuration

# export FLASK_APP=run.py:app

app = create_app(Configuration)

if __name__ == "__main__":
    app.run(debug=True)
