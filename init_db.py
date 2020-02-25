from users.app import create_app
from users.db import db, db_config
from users.models import UserModel

if __name__ == '__main__':
    app = create_app(db, db_config)
    app.app_context().push()
    app.db.drop_all()
    app.db.create_all()
