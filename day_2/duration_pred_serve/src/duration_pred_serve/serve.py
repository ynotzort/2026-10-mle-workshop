import pickle
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

with open("models/2022-01.pkl", "rb") as f_in:
    model = pickle.load(f_in)


class PredictRequest(BaseModel):
    """Inputs required for the prediction."""

    PULocationID: str = Field(description="PickUp Location ID")
    DOLocationID: str = Field(description="DropOff location ID")
    trip_distance: float = Field(description="Distance in km")


class PredictionResponse(BaseModel):
    """Result of the prediction"""

    prediction_duration_minutes: float = Field(
        description="Predicted trip duration in minutes"
    )


def predict(model_input: dict[str, Any]) -> float:
    """Do the prediction using the model"""
    prediction = model.predict(model_input)
    return float(prediction[0])


def prepare_features(predict_request: PredictRequest) -> dict[str, Any]:
    """feature preparation/engineering if needed"""
    result = predict_request.model_dump()
    result["PULocationID"] = str(result["PULocationID"])  # example
    result["trip_distance"] = float(result["trip_distance"])  # example

    return result


def post_process_prediction(prediction: float) -> float:
    """Do postprocessing of the raw model output if necessary"""
    return prediction


# fastAPI

app = FastAPI()


@app.post("/predict")
def predict_endpoint(predict_request: PredictRequest) -> PredictionResponse:
    # preprocess the raw input from the user
    model_input = prepare_features(predict_request)

    # feed the preprocessed data into the model and get a prediction
    prediction_raw = predict(model_input)

    # post process the prediction
    prediction = post_process_prediction(prediction_raw)

    # create the final response
    response = PredictionResponse(prediction_duration_minutes=prediction)
    return response


# trip = {
#     "PULocationID": "43",
#     "DOLocationID": "238",
#     "trip_distance": 1.16,
# }

# prediction = model.predict(trip)
# print(prediction[0])
