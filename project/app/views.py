from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .chatbot.retrieval import quey_vectorstore
import json

@csrf_exempt
def chatbot(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            query = body.get("query")

            if not query:
                return JsonResponse({"error": "Missing 'query' in request body"}, status=400)

            answer = quey_vectorstore(query)
            return JsonResponse({"query": query, "answer": answer}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)
