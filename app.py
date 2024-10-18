from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from datetime import datetime
import mysql.connector.pooling

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database configuration with connection pooling
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Password',
    'database': 'Cab_data'
}

cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool",
                                                      pool_size=5,
                                                      **db_config)

# Function to establish a database connection
def get_db_connection():
    try:
        return cnxpool.get_connection()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# # Pricing per adult
# PRICE_PER_ADULT = {
#     1: 2000,  # Price for 1 adult
#     2: 4000,  # Price for 2 adults (discounted for couples)
#     3: 5500,  # Price for 3 adults
#     4: 8000   # Price for 4 adults
# }

# Home Route
@app.route('/')
def home():
    return render_template('home.html')

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        mobile_number = request.form['mobile_number']

        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("INSERT INTO users (name, email, password, mobile_number) VALUES (%s, %s, %s, %s)",
                               (name, email, password, mobile_number))
                connection.commit()
                flash("Thanks for registering!", "success")
                return redirect(url_for('login'))
            except mysql.connector.Error as err:
                flash(f"Error: {err}", "danger")
            finally:
                cursor.close()
                connection.close()
        else:
            flash("Database connection failed!", "danger")
    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            try:
                cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
                user = cursor.fetchone()

                if user:
                    session['user_id'] = user['id']
                    session['username'] = user['name']
                    flash("Login successful!", "success")
                    return redirect(url_for('car_type'))
                else:
                    flash("Invalid login. Please try again.", "danger")
            except mysql.connector.Error as err:
                flash(f"Error: {err}", "danger")
            finally:
                cursor.close()
                connection.close()
        else:
            flash("Database connection failed!", "danger")
    return render_template('login.html')



# Check Car types
@app.route('/car_type', methods=['GET', 'POST'])
def car_type():
    if request.method == 'POST':
        car_type = request.form['car_type']  # Retrieve the car type from the form
        return redirect(url_for('book', car_type=car_type))  # Pass car_type

    return render_template('car_type.html')


# Global constant for car type prices per day
PRICE_PER_DAY = {
    'sedan': 2500,
    'mini campervan': 6000,
    'suv': 4000
}

@app.route('/book/<car_type>', methods=['GET', 'POST'])
def book(car_type):
    if request.method == 'GET':
        # Pass the correct price based on the car type to the HTML
        return render_template('booking.html', car_type=car_type, price_per_day=PRICE_PER_DAY.get(car_type.lower(), 0))

    if request.method == 'POST':
        try:
            # Retrieve form inputs
            check_in = request.form['check_in']
            check_out = request.form['check_out']
            special_requests = request.form['special_requests']
            payment_mode = request.form['payment_mode']

            # Get user ID from session (assuming user is logged in)
            user_id = session.get('user_id')

            # Calculate the number of days
            check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
            check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
            num_days = (check_out_date - check_in_date).days

            # Get the daily rate based on the car type (ensure car_type is lowercased)
            daily_rate = PRICE_PER_DAY.get(car_type.lower(), 0)
            total_price = daily_rate * num_days

            # Debug: Print total price for verification
            print(f"Total price calculated: {total_price}")

            # Insert booking into the database
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO bookings (user_id, car_type, num_days, pickup, dropoff, 
                special_requests, payment_mode, total_price)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (user_id, car_type, num_days, check_in, check_out, special_requests, payment_mode, total_price))

            conn.commit()
            cursor.close()
            conn.close()

            return redirect('/thank_you')

        except Exception as e:
            # Catch and print the error if there's an issue with SQL
            print(f"Error inserting into database: {e}")
            return "An error occurred while booking. Please try again."





# Thank You Route
@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

# My Bookings Route
@app.route('/my_bookings')
def my_bookings():
    user_id = session.get('user_id')  # Get user ID from session
    if not user_id:
        flash("You need to log in to view your bookings.", "danger")
        return redirect(url_for('login'))

    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM bookings WHERE user_id=%s", (user_id,))
            bookings = cursor.fetchall()  # Fetch all bookings for the user
            return render_template('my_bookings.html', bookings=bookings)  # Render bookings
        except mysql.connector.Error as err:
            flash(f"Error: {err}", "danger")
        finally:
            cursor.close()
            connection.close()
    else:
        flash("Database connection failed!", "danger")
    
    return render_template('my_bookings.html', bookings=[])


if __name__ == '__main__':
    app.run(debug=True)

