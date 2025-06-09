import requests

def get_ip_info(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,zip,lat,lon,isp,org,as")
        data = response.json()
        if data.get("status") == "success":
            info = (
                f"Country: {data.get('country')}\n"
                f"Region: {data.get('regionName')}\n"
                f"City: {data.get('city')}\n"
                f"ZIP: {data.get('zip')}\n"
                f"Latitude: {data.get('lat')}\n"
                f"Longitude: {data.get('lon')}\n"
                f"ISP: {data.get('isp')}\n"
                f"Org: {data.get('org')}\n"
                f"AS: {data.get('as')}\n"
            )
            return info
        else:
            return f"Error: {data.get('message')}"
    except Exception as e:
        return f"Request Error: {e}"

def get_http_headers(url):
    if not url.startswith("http"):
        url = "http://" + url
    try:
        response = requests.head(url, timeout=5)
        headers = "\n".join(f"{k}: {v}" for k, v in response.headers.items())
        return headers
    except Exception as e:
        return f"Error fetching headers: {e}"