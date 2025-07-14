import joblib
import numpy as np
from config.path_config import MODEL_OUTPUT_PATH
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Load model with error handling
try:
    loaded_model = joblib.load(MODEL_OUTPUT_PATH)
    model_loaded = True
    print(f"✅ Model loaded successfully from {MODEL_OUTPUT_PATH}")
except Exception as e:
    loaded_model = None
    model_loaded = False
    print(f"❌ Error loading model: {e}")

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        if not model_loaded:
            return render_template('index.html', prediction=None, error="Model not available")

        try:
            lead_time = int(request.form["lead_time"])
            no_of_special_request = int(request.form["no_of_special_request"])
            avg_price_per_room = float(request.form["avg_price_per_room"])
            arrival_month = int(request.form["arrival_month"])
            arrival_date = int(request.form["arrival_date"])

            market_segment_type = int(request.form["market_segment_type"])
            no_of_week_nights = int(request.form["no_of_week_nights"])
            no_of_weekend_nights = int(request.form["no_of_weekend_nights"])

            type_of_meal_plan = int(request.form["type_of_meal_plan"])
            room_type_reserved = int(request.form["room_type_reserved"])


            features = np.array([[lead_time,no_of_special_request,avg_price_per_room,arrival_month,arrival_date,market_segment_type,no_of_week_nights,no_of_weekend_nights,type_of_meal_plan,room_type_reserved]])

            prediction = loaded_model.predict(features)

            # Get probability if available
            probability = None
            if hasattr(loaded_model, 'predict_proba'):
                prob = loaded_model.predict_proba(features)[0]
                probability = prob[1] if len(prob) > 1 else prob[0]

            # Package form data for display
            form_data = {
                'lead_time': lead_time,
                'no_of_special_request': no_of_special_request,
                'avg_price_per_room': avg_price_per_room,
                'arrival_month': arrival_month,
                'arrival_date': arrival_date,
                'market_segment_type': market_segment_type,
                'no_of_week_nights': no_of_week_nights,
                'no_of_weekend_nights': no_of_weekend_nights,
                'type_of_meal_plan': type_of_meal_plan,
                'room_type_reserved': room_type_reserved
            }

            return render_template('index.html', 
                                 prediction=prediction[0], 
                                 probability=probability,
                                 form_data=form_data,
                                 model_loaded=model_loaded)
        
        except Exception as e:
            return render_template('index.html', 
                                 prediction=None, 
                                 error=f"Error making prediction: {str(e)}",
                                 model_loaded=model_loaded)
    
    return render_template("index.html", prediction=None, model_loaded=model_loaded)

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'model_loaded': model_loaded,
        'model_path': MODEL_OUTPUT_PATH
    })

if __name__=="__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
