from app import app
from model.user_model import user_model

user_obj=user_model()

@app.route("/user")
def user():
    return user_model.user()