from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Imports from utils
from predictor.utils.predict import get_prediction
from predictor.utils.transformer import process_symptoms
from django.shortcuts import render
from .utils.transformer import match_symptom, process_symptoms  # adjust if needed


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
def disease_predictor_view(request):
    matched_symptoms = prediction = info = None

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'get_matches':
            user_input = request.POST.get('symptom')
            if user_input:
                matched_symptoms = match_symptom(user_input)
        elif action == 'get_prediction':
            selected_raw = request.POST.get('selected_symptoms')
            selected_symptoms = selected_raw.split(',') if selected_raw else []
            if selected_symptoms:
                prediction, info = process_symptoms(selected_symptoms)

    return render(request, 'disease_predictor.html', {
        'matched_symptoms': matched_symptoms,
        'prediction': prediction,
        'info': info,
    })


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
