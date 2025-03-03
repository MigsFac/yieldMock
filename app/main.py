import pickle
import numpy as np
from flask import Blueprint,request,jsonify

ml_blueprint = Blueprint('ml', __name__)

@ml_blueprint.route('/predict',methods=['POST'])
def predict():

    try:
        data = request.get_json()
        features = np.array(data["features"]).reshape(1,-1)
        prediction = model.predict(features).tolist()

        return jsonify({"prediction": prediction})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400