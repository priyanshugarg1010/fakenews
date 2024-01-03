import requests

# Set the URL of your Flask application
url = 'http://localhost:5000/predict'

# Define the input data (news text) you want to pass
input_data = {'news': 'Your news text goes here'}

# Make a POST request to the /predict endpoint
response = requests.post(url, json=input_data)

# Check the response
if response.status_code == 200:
    result = response.json()
    print("LR Prediction:", result["LR Prediction"])
    print("DT Prediction:", result["DT Prediction"])
    print("GBC Prediction:", result["GBC Prediction"])
    print("RFC Prediction:", result["RFC Prediction"])
else:
    print("Error:", response.status_code, response.text)
