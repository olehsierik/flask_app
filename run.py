from app import app
from app.event import views
from app.user import views
from app.main import views


if __name__ == '__main__':
    app.run(port=app.config.get("PORT"), debug=app.config.get("DEBUG"))
