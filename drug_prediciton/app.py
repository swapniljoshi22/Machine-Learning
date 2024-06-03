from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load the serialized model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Define mappings
sex_map = {"M": 0, "F": 1}
bp_map = {"LOW": 0, "NORMAL": 1, "HIGH": 2}
cholesterol_map = {"NORMAL": 0, "HIGH": 1}
drug_map = {"drugA": 0, "drugB": 1, "drugC": 2, "drugX": 3, "DrugY": 4}

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    # Get input values from the form
    age = float(request.form['age'])
    sex = sex_map[request.form['sex']]
    bp = bp_map[request.form['bp']]
    cholesterol = cholesterol_map[request.form['cholesterol']]
    na_to_k = float(request.form['na_to_k'])

    # Make prediction using the model
    prediction = model.predict([[age, sex, bp, cholesterol, na_to_k]])

    # Map the prediction back to drug name
    drug_name = [k for k, v in drug_map.items() if v == prediction[0]][0]

    # Render template with prediction result
    return render_template('result.html', drug_name=drug_name)

if __name__ == '__main__':
    app.run(debug=True)
