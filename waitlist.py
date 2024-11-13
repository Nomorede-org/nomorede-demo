import requests

def add_to_waitlist(name, mobile, email, message,backend_url):
    url = backend_url+"/customer/waitlist"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "name": name,
        "mobile": mobile,
        "email": email,
        "message": message
    }
    print(data)
    response = requests.post(url, headers=headers, json=data)
    return response.status_code