
from flask import Flask, render_template, request, redirect, url_for, flash
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hello'
password_reset_tokens = {}

# Dummy product data (replace with a database in a real application)
products = [
    {'id': 1, 'name': 'Product 1', 'price': 10.99},
    {'id': 2, 'name': 'Product 2', 'price': 19.99},
    {'id': 3, 'name': 'Product 3', 'price': 29.99},
]

# In-memory user data (replace with a database in a real application)
users = {
    'user1': {'username': 'user1', 'password': 'password1', 'email': 'user1@example.com'},
    'user2': {'username': 'user2', 'password': 'password2', 'email': 'user2@example.com'},
}

# Dummy shopping cart (replace with a database in a real application)
cart = []

@app.route('/')
def home():
    return render_template('index.html' , products=products)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = users.get(username)

        if user and user['password'] == password:
            # Log in the user (you may want to use Flask-Login for this)
            flash('Login successful!', 'success')
            return redirect(url_for('catalog'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')

@app.route('/catalog')
def catalog():
    return render_template('catalog.html')

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        cart.append(product)
    return redirect('/')

@app.route('/cart')
def view_cart():
    total_price = sum(product['price'] for product in cart)
    return render_template('cart.html', cart=cart, total_price=total_price)


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = next((user for user in users.values() if user['email'] == email), None)

        if user:
            token = generate_random_token()
            password_reset_tokens[token] = user['username']

            # In a real application, you would send an email with the reset link
            flash(f'Reset link sent to {email}', 'success')
        else:
            flash('Email not found', 'error')

    return render_template('forgot_password.html')

def generate_random_token():
    return secrets.token_hex()

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    username = password_reset_tokens.get(token)

    if not username:
        flash('Invalid or expired reset link', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_password = request.form.get('new_password')
        users[username]['password'] = new_password

        # In a real application, you might want to invalidate the token after use
        del password_reset_tokens[token]

        flash('Password reset successful!', 'success')
        return redirect(url_for('login'))

    return render_template('reset_password.html', token=token)


if __name__ == '__main__':
    app.run(debug=True)
