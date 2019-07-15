"""
import requests

# https://stackoverflow.com/a/25890585
def get_geo_coordinates(address, api_key):
    response = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}')
    resp_json_payload = response.json()
    return resp_json_payload['results'][0]['geometry']['location']
"""
