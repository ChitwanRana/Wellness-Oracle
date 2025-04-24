from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Imports from utils
from predictor.utils.predict import get_prediction
from predictor.utils.transformer import process_symptoms

# Load disease info JSON once
with open("predictor/utils/disease_info.json") as f:
    disease_info = json.load(f)

# -----------------------------------
# API Endpoint: Symptom Matching
# -----------------------------------
@csrf_exempt
def get_matches(request):
    user_input = request.GET.get("query")
    if not user_input:
        return JsonResponse({"error": "No input provided"}, status=400)

    matches = process_symptoms(user_input)
    return JsonResponse({"matches": matches})

# -----------------------------------
# API Endpoint: Predict Disease
# -----------------------------------
@csrf_exempt
def predict_disease(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            matched_symptoms = body.get("matched_symptoms", [])
            predictions = get_prediction(matched_symptoms)
            disease = predictions[0] if predictions else "Unknown"

            info = disease_info.get(disease, {
                "description": "Info not found.",
                "do": [], "dont": [], "workout": "", "diet": ""
            })

            return JsonResponse({
                "disease": disease,
                "info": info
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=405)

# -----------------------------------
# Template View: Form-based UI
# -----------------------------------
def index(request):
    matched_symptoms = None
    prediction = None
    info = None

    if request.method == "POST":
        user_input = request.POST.get("symptom")
        matched_symptoms = process_symptoms(user_input)
        predictions = get_prediction(matched_symptoms)
        if predictions:
            prediction = predictions[0]
            info = disease_info.get(prediction, {
                "description": "Info not found.",
                "do": [], "dont": [], "workout": "", "diet": ""
            })

    return render(request, "predictor/index.html", {
        "matched_symptoms": matched_symptoms,
        "prediction": prediction,
        "info": info,
    })
