from flask import Flask, render_template
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' # TODO CHANGE THIS LATER

UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'
mail = Mail(app)

from database import init_db
from routes.auth import auth_bp
from routes.teams import teams_bp
from routes.profile import profile_bp
from routes.facilities import facilities_bp
from routes.matches import matches_bp
from routes.invites import invites_bp
from routes.players import players_bp
from routes.settings import settings_bp

@app.route('/')
def home():
    return render_template('home.html')

app.register_blueprint(auth_bp)
app.register_blueprint(teams_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(facilities_bp)
app.register_blueprint(matches_bp)
app.register_blueprint(invites_bp)
app.register_blueprint(players_bp)
app.register_blueprint(settings_bp)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)