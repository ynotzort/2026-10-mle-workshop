import pickle


with open("models/2022-01.pkl", "rb") as f_in:
    model = pickle.load(f_in)

trip = {
    "PULocationID": "43",
    "DOLocationID": "238",
    "trip_distance": 1.16,
}

prediction = model.predict(trip)
print(prediction[0])

