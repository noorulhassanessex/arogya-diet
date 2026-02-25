~~~~app.py below ~~~~
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# ----- Home Page -----
@app.route('/')
def home():
    return render_template('index.html')

# ----- Tracker Page -----
@app.route('/tracker', methods=['GET', 'POST'])
def tracker():
    if request.method == 'POST':
        meal = request.form.get('meal')
        food = request.form.get('food')
        quantity = request.form.get('quantity')

        print(f"Meal: {meal}, Food: {food}, Quantity: {quantity}")

        # Later → save to SQL here
        return redirect('/tracker')

    return render_template('tracker.html')


# ----- Meal Plan Page -----
@app.route('/meal-plan')
def meal_plan():
    return render_template('meal_plan.html')


# ----- About Page -----
@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True) 






~~index.html below~~ 
 

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arogya Diet Management Tool</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>

<header>
    <h1>Arogya Diet</h1>
    <nav>
        <a href="/">Home</a>
        <a href="/tracker">Track Diet</a>
        <a href="/meal-plan">Meal Plan</a>
        <a href="/about">About</a>
    </nav>
</header>

<section class="hero">
    <h1>Eat Healthy. Stay Fit.</h1>
    <p>Track your meals, calories, and design the perfect diet plan for your fitness goals.</p>
    <a href="/tracker" class="btn">Start Tracking</a>
</section>

<footer>
    <p>© 2025 Arogya</p>
</footer>

</body>
</html> 

~~tracker.html below ~~


 <head> <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
 <form> 
    <label for="meal" > Meal:</label>
    <select id="meal" name="meal">  


        <option value="breakfast">breakfast</option> 
        <option value="Lunch">breakfast</option>
        <option value="Snacks">breakfast</option>
        <option value="dinner">breakfast</option> 
    </select>  


    <label for ="food"> food Item:</label> 
    <input type="text" id="food" name="food" placeholder="Enter food item"  

    <label for="quantity">Quantity(grams):</label>
    <input type="text" id="food" name="food"> placeholder="Enter food item"> 
    
     <label for="quantity">Quantity (grams):</label>
    <input type="number" id="quantity" name="quantity" placeholder="e.g., 100">

    <button type="submit"> Add meal</button>
    
</form> 


~~about.html below ~~

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About – Arogya Diet Management Tool</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>

<body>

    <header>
        <h1>Arogya Diet Management Tool</h1>
        <nav>
            <ul>
                <li><a href="/">Home</a></li>
                <li><a href="/tracker">Track Diet</a></li>
                <li><a href="/meal_plan">Meal Plan</a></li>
                <li><a class="active" href="/about">About</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <section class="hero">
            <h1>About Arogya</h1>
            <p>
                Arogya is a simple and user-friendly diet management tool designed to help students, 
                professionals, and health-conscious individuals track their meals, calories, and nutrition 
                goals more efficiently.
            </p>
        </section>

        <section class="form-container">
            <h2>Our Mission</h2>
            <p>
                The goal of Arogya is to encourage healthy eating habits by allowing users to easily log 
                their daily meals, monitor calorie intake, and generate customized meal plans. 
                We believe that small, consistent changes in diet can lead to major improvements 
                in overall health.
            </p>

            <h2>What You Can Do</h2>
            <ul>
                <li>Track calories and nutrients from your daily meals.</li>
                <li>Create personalized meal plans.</li>
                <li>Understand healthier food choices.</li>
                <li>Maintain diet goals for weight gain, weight loss, or balanced nutrition.</li>
            </ul>

            <h2>Why We Built This Project</h2>
            <p>
                This project was created as part of a university assignment to demonstrate web development 
                skills using Flask, HTML, CSS, and JavaScript. The aim was to build a fully functional 
                tool with clean UI, good routing, templates, and user-friendly interaction.
            </p>
        </section>
    </main>

    <footer>
        <p>&copy; 2025 Arogya</p>
    </footer>

</body>
</html>

~~meal_plan.html below ~~


<!DOCTYPE html> 
<html lang="en">   
<head> 
    <meta charset="UTD-8"> 
    <meta name="viewport" content="width=device-width , initial-scale=1.0">  
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <title>Track Meals</title>
</head> 
<body> 
    <header> 
        <h1>Arogya Diet</h1> 
        <nav> 
            <a href="/">Home</a>
            <a href ="/tracker">Track Diet</a>
            <a href="/meal-plan">Meal Plan</a>
            <a href="/about">About</a>

        </nav>
    </header>  
    <section class="hero"> 
        <h1> Your Personal Meal Plan</h1>
        <p>Balanced meals to help you reach your fitness goals. </p>
    </section>
    </body> 
</html> 
</html> 


~~style.css below~~ 

 
/* RESET */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Poppins', Arial, sans-serif;
}

body {
    background: #f7f9fc;
    color: #333;
}

/* HEADER */
header {
    background: linear-gradient(90deg, #ff4b91, #8349ff, #4facfe);
    padding: 20px;
    color: white;
    text-align: center;
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: 1px;
}

nav {
    margin-top: 10px;
}

nav a {
    color: white;
    margin: 0 15px;
    text-decoration: none;
    font-weight: 500;
    transition: 0.3s;
}

nav a:hover {
    text-shadow: 0px 0px 8px white;
}

/* HERO SECTION */
.hero {
    max-width: 700px;
    margin: 50px auto;
    text-align: center;
    background: white;
    padding: 40px;
    border-radius: 18px;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.1);
}

.hero h1 {
    font-size: 2.4rem;
    color: #333;
}

.hero p {
    margin: 15px 0;
    font-size: 1.2rem;
    color: #555;
}

.btn {
    display: inline-block;
    margin-top: 20px;
    padding: 12px 35px;
    border: none;
    font-size: 1.1rem;
    color: white;
    border-radius: 50px;
    cursor: pointer;
    background: linear-gradient(90deg, #ff4b91, #8349ff);
    transition: 0.3s;
}

.btn:hover {
    box-shadow: 0px 0px 15px rgba(255,0,140,0.8);
    transform: translateY(-2px);
}

/* TRACKER FORM */
.form-container {
    max-width: 500px;
    background: white;
    margin: 40px auto;
    padding: 30px;
    border-radius: 18px;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.1);
}

.form-container h2 {
    margin-bottom: 20px;
    color: #444;
}

label {
    font-weight: 500;
    color: #444;
}

input, select {
    width: 100%;
    padding: 12px;
    margin: 8px 0 18px 0;
    border: 2px solid #d1d1d1;
    border-radius: 10px;
    transition: 0.3s;
}

input:focus, select:focus {
    border-color: #8349ff;
    outline: none;
    box-shadow: 0px 0px 8px rgba(131, 73, 255, 0.4);
}

.submit-btn {
    width: 100%;
    padding: 15px;
    background: linear-gradient(90deg, #4facfe, #8349ff);
    color: white;
    border: none;
    font-size: 1.2rem;
    border-radius: 12px;
    cursor: pointer;
    transition: 0.3s;
}

.submit-btn:hover {
    box-shadow: 0px 0px 15px rgba(79,172,254,0.6);
    transform: translateY(-2px);
}
 
~~end~~

