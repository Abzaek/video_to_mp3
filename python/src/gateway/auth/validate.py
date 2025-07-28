import os, requests

def token(request):
    
    if "Authorization" not in request.headers:
        return None, ("missing credentials", 401)

    token = request.headers['Authorization']

    if not token:
        return None, ("missing credentials", 401)

    response = requests.post(
        f"http://{os.getenv('AUTH_SVC_ADDRESS')}/validate",
        headers=request.headers,
    )

    if response.status_code == 200:
        return response.text, None
    
    return None, (response.text, response.status_code)