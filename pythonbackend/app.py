from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.ensemble import GradientBoostingClassifier

from sklearn.metrics import classification_report
import re
import string
import joblib
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

print("Loading data 1...")
data_fake = pd.read_csv('Fake.csv')
print("Data loaded successfully.")
print("Loading data 2...")
data_true = pd.read_csv('True.csv')
print("Data loaded successfully.")

data_fake["class"] = 0
data_true['class'] = 1

data_fake_manual_testing = data_fake.tail(10)
print("checkpoint 1...")

for i in range(23480, 23470, -1):
    data_fake.drop([i], axis=0, inplace=True)

print("checkpoint 2...")

data_true_manual_testing = data_true.tail(10)

print("checkpoint 3...")

for i in range(21416, 21406, -1):
    data_true.drop([i], axis=0, inplace=True)

print("checkpoint 4...")

data_fake_manual_testing.loc[:, 'class'] = 0
data_true_manual_testing.loc[:, 'class'] = 1

data_merge = pd.concat([data_fake, data_true], axis=0)
data_merge.reset_index(inplace=True)
data_merge.drop(['index'], axis=1, inplace=True)

data_merge['text'] = data_merge['text'].apply(lambda x: x.lower())
data_merge['text'] = data_merge['text'].apply(lambda x: re.sub(r'\[.*?\]', '', x))
data_merge['text'] = data_merge['text'].apply(lambda x: re.sub(r"\\W", " ", x))
data_merge['text'] = data_merge['text'].apply(lambda x: re.sub(r'https?://\S+|www\.\S+', '', x))
data_merge['text'] = data_merge['text'].apply(lambda x: re.sub(r'<.*?>+', '', x))
data_merge['text'] = data_merge['text'].apply(lambda x: re.sub(r'[%s]' % re.escape(string.punctuation), '', x))
data_merge['text'] = data_merge['text'].apply(lambda x: re.sub(r'\n', '', x))
data_merge['text'] = data_merge['text'].apply(lambda x: re.sub(r'\w*\d\w*', '', x))

data = data_merge.drop(['title', 'subject', 'date'], axis=1)
data = data.sample(frac=1)
data.reset_index(inplace=True)
data.drop(['index'], axis=1, inplace=True)

print("checkpoint 5...")

vectorization = TfidfVectorizer()
x = data['text']
y = data['class']
xv = vectorization.fit_transform(x)

x_train, x_test, y_train, y_test = train_test_split(xv, y, test_size=0.25)

print("checkpoint 6...")



# Check if the Logistic Regression model file exists
model_file = "logistic_regression_model.joblib"

if os.path.exists(model_file):
    # Load the model if it exists
    LR = joblib.load(model_file)
    print("Logistic Regression Model loaded successfully...")
else:
    # Train and save the model if it doesn't exist
    LR = LogisticRegression()
    LR.fit(x_train, y_train)
    joblib.dump(LR, model_file)
    print("Logistic Regression Model trained and saved successfully...")
    print("checkpoint 7...")




# Check if the Decision Tree model file exists
model_file_dt = "decision_tree_model.joblib"

if os.path.exists(model_file_dt):
    # Load the Decision Tree model if it exists
    DT = joblib.load(model_file_dt)
    print("Decision Tree Model loaded successfully...")
else:
    # Train and save the Decision Tree model if it doesn't exist
    DT = DecisionTreeClassifier()
    DT.fit(x_train, y_train)
    joblib.dump(DT, model_file_dt)
    print("Decision Tree Model trained and saved successfully...")
    print("checkpoint 8...")  # Add this line




# Check if the Gradient Boosting model file exists
model_file_gb = "gradient_boosting_model.joblib"

if os.path.exists(model_file_gb):
    # Load the Gradient Boosting model if it exists
    GB = joblib.load(model_file_gb)
    print("Gradient Boosting Model loaded successfully...")
else:
    # Train and save the Gradient Boosting model if it doesn't exist
    GB = GradientBoostingClassifier(random_state=0)
    GB.fit(x_train, y_train)
    joblib.dump(GB, model_file_gb)
    print("Gradient Boosting Model trained and saved successfully...")
    print("checkpoint 9...")  # Add this line





# Check if the RandomForest model file exists
model_file_rf = "random_forest_model.joblib"

if os.path.exists(model_file_rf):
    # Load the RandomForest model if it exists
    RF = joblib.load(model_file_rf)
    print("RandomForest Model loaded successfully...")
else:
    # Train and save the RandomForest model if it doesn't exist
    RF = RandomForestClassifier(random_state=0)
    RF.fit(x_train, y_train)
    joblib.dump(RF, model_file_rf)
    print("RandomForest Model trained and saved successfully...")
    print("checkpoint 10...")  # Add this line




def output_label(n):
    if n == 0:
        return "Fake News"
    elif n == 1:
        return "Not A Fake News"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        news = request.json['news']
        testing_news = {"text": [news]}
        new_def_test = pd.DataFrame(testing_news)
        new_def_test["text"] = new_def_test["text"].apply(lambda x: x.lower())
        new_def_test["text"] = new_def_test["text"].apply(lambda x: re.sub(r'\[.*?\]', '', x))
        new_def_test["text"] = new_def_test["text"].apply(lambda x: re.sub(r"\\W", " ", x))
        new_def_test["text"] = new_def_test["text"].apply(lambda x: re.sub(r'https?://\S+|www\.\S+', '', x))
        new_def_test["text"] = new_def_test["text"].apply(lambda x: re.sub(r'<.*?>+', '', x))
        new_def_test["text"] = new_def_test["text"].apply(lambda x: re.sub(r'[%s]' % re.escape(string.punctuation), '', x))
        new_def_test["text"] = new_def_test["text"].apply(lambda x: re.sub(r'\n', '', x))
        new_def_test["text"] = new_def_test["text"].apply(lambda x: re.sub(r'\w*\d\w*', '', x))

        new_x_test = new_def_test["text"]
        new_xv_test = vectorization.transform(new_x_test)

        pred_LR = LR.predict(new_xv_test)
        pred_DT = DT.predict(new_xv_test)
        pred_GB = GB.predict(new_xv_test)
        pred_RF = RF.predict(new_xv_test)


        result = {
            "LR Prediction": output_label(pred_LR[0]),
            "DT Prediction": output_label(pred_DT[0]),
            "GB Prediction": output_label(pred_GB[0]),
            "RF Prediction": output_label(pred_RF[0]),

        }

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=False, port=5000)
