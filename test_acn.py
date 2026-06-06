import requests

TOKEN = "6nIRhdftYQ5UPTKSSaONj9sAU98RyxkIyXFoa-HIN7I"

url = "https://ev.caltech.edu/api/v1/sessions/caltech"

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)
print(response.text[:1000])