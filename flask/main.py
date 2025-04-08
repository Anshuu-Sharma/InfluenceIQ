from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
import joblib
import numpy as np

# Load model and scaler
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

app = FastAPI()




# 🧠 New input format
class UserFeatures(BaseModel):
    username: str
    posts: int
    following: int
    followers: int
    has_profile_pic: bool
    private: bool
    follower_following_ratio: float
    bio_length: int
    username_length: int
    digits_in_username: int

@app.post("/predict")
def predict(users: List[UserFeatures]):
    features = []
    
    for user in users:
        row = [
            user.posts,
            user.followers,
            user.following,
            int(user.has_profile_pic),
            int(user.private),
            user.follower_following_ratio,
            user.bio_length,
            user.username_length,
            user.digits_in_username
        ]
        features.append(row)

    scaled_features = scaler.transform(features)
    predictions = model.predict(scaled_features)

    return {"predictions": predictions.tolist()}



