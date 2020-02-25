from users.app import create_app
from users.db import db, db_config

app = create_app(db, db_config)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
