from django.shortcuts import render
from .forms import HeartDiseaseForm
from .spark_model import predict_heart_disease

def predict_view(request):
    prediction = None
    probability = None

    if request.method == "POST":
        form = HeartDiseaseForm(request.POST)
        if form.is_valid():
            result = predict_heart_disease(form.cleaned_data)
            prediction = result["prediction"]
            probability = round(result["probability"] * 100, 2)
    else:
        form = HeartDiseaseForm()

    return render(request, "predict.html", {
        "form": form,
        "prediction": prediction,
        "probability": probability
    })
