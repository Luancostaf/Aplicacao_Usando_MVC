from flask import Flask
from database import db
from controllers.usuario_controller import usuario_bp
from controllers.chamado_controller import chamado_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///helpdesk.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(usuario_bp)
app.register_blueprint(chamado_bp)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)