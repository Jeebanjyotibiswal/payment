from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Mapping of amount to QR image and course details
COURSE_PLANS = {
    150: {
        'qr_image': '150.jpg',
        'name': 'Basic Plan',
        'description': '1-month access to basic courses'
    },
    250: {
        'qr_image': '100.jpg', 
        'name': 'Standard Plan',
        'description': '3-month access to all courses'
    },
    300: {
        'qr_image': '100.jpg',
        'name': 'Premium Plan',
        'description': '6-month premium access'
    },
    2000: {
        'qr_image': '2000.jpg',
        'name': 'Professional Plan',
        'description': '1-year full access with certificate'
    },
    3500: {
        'qr_image': '3500.jpg',
        'name': 'Master Plan',
        'description': 'Lifetime access with premium support'
    }
}

@app.route('/')
def home():
    return render_template('index.html', plans=COURSE_PLANS)

@app.route('/enroll/<int:amount>')
def enroll(amount):
    if amount not in COURSE_PLANS:
        flash('Invalid payment amount selected!', 'error')
        return redirect(url_for('home'))
    
    plan = COURSE_PLANS[amount]
    return render_template('enroll.html', amount=amount, plan=plan)

@app.route('/payment', methods=['POST'])
def payment():
    try:
        amount = int(request.form['amount'])
        name = request.form.get('name', '').strip()
        batch = request.form.get('batch', '').strip()
        age = request.form.get('age', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        
        # Validate required fields
        if not all([name, batch, age, phone, email]):
            flash('Please fill in all required fields!', 'error')
            return redirect(url_for('enroll', amount=amount))
        
        if amount not in COURSE_PLANS:
            flash('Invalid payment amount!', 'error')
            return redirect(url_for('home'))
        
        plan = COURSE_PLANS[amount]
        
        # Here you would typically save the enrollment data to a database
        print(f"New enrollment: {name}, {email}, Amount: {amount}")
        
        return render_template('payment.html',
                           name=name,
                           batch=batch,
                           age=age,
                           phone=phone,
                           email=email,
                           amount=amount,
                           plan=plan)
    
    except Exception as e:
        flash('An error occurred. Please try again!', 'error')
        return redirect(url_for('home'))

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)