from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import string ,random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(500), nullable=False)
    short_url = db.Column(db.String(10), unique=True, nullable=False)

    
    def generate_short_url(length=10):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_url = URL.generate_short_url()
        
        # Check if short_url already exists
        while URL.query.filter_by(short_url=short_url).first() is not None:
            short_url = URL.generate_short_url()
        
        new_url = URL(long_url=long_url, short_url=short_url)
        db.session.add(new_url)
        db.session.commit()
        return render_template('home.html', short_url=short_url)
    return render_template('home.html')

@app.route('/<short_url>')
def redirect_to_url(short_url):
    url_data = URL.query.filter_by(short_url=short_url).first()
    if url_data:
        return redirect(url_data.long_url)
    return 'URL not found'

if __name__ == '__main__':
    app.run(debug=True)
    @app.route('/', methods=['GET', 'POST'])
    def home():
        if request.method == 'POST':
            long_url =request.form['long_url']
            short_url = generate_short_url()
            new_url = URL(long_url=long_url, short_url=short_url)
            db.session.add(new_url)
            db.session.commit()
            return f"Shortened URL: {request.host}/{short_url}"             
        return render_template('home.html')

    @app.route('/<short_url>')
    def redirect_to_url(short_url):
        url_entry = URL.query.filter_by(short_url=short_url).first()
        if url_entry:
            return redirect(url_entry.long_url)
        else:
            return "URL not found", 404

    if __name__ == '__main__':
        app.run(debug=True)