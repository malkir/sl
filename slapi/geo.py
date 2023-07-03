from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import json

class ReverseGeo:
    def __init__(self, user_agent="slapi/v0.0.1"):
        self.geolocator = Nominatim(user_agent=user_agent)

    def reverse_geocode(self, lat, lon, zoom=18, metadata=None):
        try:
            location = self.geolocator.reverse((lat, lon), zoom=zoom)
            address = location.raw['address']
            result = {
                'addressLines': [address.get('house_number', 'REQUIRED') + ', ' + address.get('road', '')],
                'locality': address.get('town', ''),
                'administrativeArea': address.get('state', ''),
                'administrativeAreaCode': address.get('ISO3166-2-lvl4', 'REQUIRED').split('-')[1], # Split from eg. US-CA
                'region': address.get('country', ''),
                'regionCode': address.get('ISO3166-2-lvl4', 'REQUIRED').split('-')[0], # Split from eg. US-CA
                'postalCode': address.get('postcode', ''),
                'metadata': metadata,
                'formattedAddress': location.address,
                'latitude': round(location.latitude, 14), # TODO: How many decimal places?
                'longitude': round(location.longitude, 14) # TODO: How many decimal places?
            }
            #return(address)
            return json.dumps(result)
        except GeocoderTimedOut:
            return self.reverse_geocode(lat, lon, zoom)

#geocoder = ReverseGeo()
#location = geocoder.reverse_geocode(33.83666565915305, -118.387475861189030, metadata="my house")