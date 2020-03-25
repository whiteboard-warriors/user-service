from users.app import create_app
from users.models import UserModel

if __name__ == '__main__':
    app = create_app()
    app.app_context().push()
    app.db.drop_all()
    app.db.create_all()
