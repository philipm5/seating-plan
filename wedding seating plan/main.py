from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__, static_folder='static', template_folder='templates')

# Load seating data using pandas
def load_seating_data():
    try:
        df = pd.read_csv('guest_seating.csv')
        # Combine first and family names to create a full name column
        df['full_name'] = df['First Name'].str.lower() + ' ' + df['Family Name'].str.lower()
        seating_data = df.set_index('full_name')['Table Number'].to_dict()
        return seating_data
    except FileNotFoundError:
        print("The file 'guest_seating.csv' was not found.")
        return {}
    except pd.errors.EmptyDataError:
        print("The file 'guest_seating.csv' is empty.")
        return {}
    except pd.errors.ParserError:
        print("There was an issue parsing 'guest_seating.csv'. Please check the file format.")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {}

# Load the seating data when the application starts
seating_data = load_seating_data()

# Route for the welcome page
@app.route('/')
def welcome():
    return render_template('welcome.html')

# Route for the seating information page
@app.route('/seating', methods=['POST', 'GET'])
def seating():
    if request.method == 'POST':
        first_name = request.form['first_name'].lower()
        family_name = request.form['family_name'].lower()
        full_name = f"{first_name} {family_name}"
        table_number = seating_data.get(full_name, "Not found")
        return jsonify({'table_number': table_number})
    return render_template('seating.html')

if __name__ == '__main__':
    app.run(debug=True)
