import requests
from django.http import JsonResponse

def get_prediction(request):


    if request.method == "POST":
        features = request.POST.getlist("features")

        try:
            response = requests.post(
                "http://127.0.0.1:5000/api/predict",
                json = {"features":features}
            )

            return JsonResponse(response.json())
        
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": str(e)}, status = 500)
