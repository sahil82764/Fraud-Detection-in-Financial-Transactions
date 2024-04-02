from flask import Flask, render_template, request
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

app = Flask(__name__)

# Load the dataset
data_path = 'fraud_data.xlsx'
data = pd.read_excel(data_path)

# Separate features and target variable
X = data.drop(columns=["isFraud", "isFlaggedFraud"])
y = data["isFraud"]

# Define categorical and numerical features
categorical_features = ["type", "nameOrig", "nameDest"]
numerical_features = ["step", "amount", "oldbalanceOrg", "newbalanceOrig", "oldbalanceDest", "newbalanceDest"]

# Preprocessing for numerical data
numeric_transformer = StandardScaler()

# Preprocessing for categorical data
categorical_transformer = OneHotEncoder(handle_unknown="ignore")

# Bundle preprocessing for numerical and categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numerical_features),
        ("cat", categorical_transformer, categorical_features)
    ])

# Append classifier to preprocessing pipeline.
# Now we have a full prediction pipeline.
clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier', LogisticRegression())])

# Train the model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
clf.fit(X_train, y_train)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/prediction', methods=['POST'])
def prediction():
    mode = request.form['mode']
    if mode == 'batch':
        return render_template('index.html', mode='batch')
    elif mode == 'realtime':
        return render_template('index.html', mode='realtime')
    else:
        return 'Invalid mode'

@app.route('/result', methods=['POST'])
def result():
    mode = request.form['mode']
    if mode == 'batch':
        file_path = request.form['file_path']
        # Perform batch prediction and save output file
        predictions = clf.predict(X_test)  # Dummy prediction, replace with actual batch prediction
        predictions_df = pd.DataFrame(predictions, columns=['Prediction'])
        timestamp = pd.Timestamp.now().strftime('%Y%m%d%H%M%S')
        predictions_df.to_csv(f'predictions_{timestamp}.csv', index=False)
        return render_template('result.html', result=f'Batch prediction file saved at predictions_{timestamp}.csv')
    elif mode == 'realtime':
        # Get real-time input and perform prediction
        inputs = [request.form[key] for key in numerical_features + categorical_features]
        inputs_df = pd.DataFrame([inputs], columns=numerical_features + categorical_features)
        inputs_preprocessed = preprocessor.transform(inputs_df)
        prediction = clf.predict(inputs_preprocessed)[0]  # Dummy prediction, replace with actual prediction
        return render_template('result.html', result=f'Real-time prediction: {prediction}')
    else:
        return 'Invalid mode'

if __name__ == '__main__':
    app.run(debug=True)
