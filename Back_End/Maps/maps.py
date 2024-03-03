import python_weather
import asyncio
import pandas as pd
from geopy.geocoders import Nominatim
import plotly.express as px
import pandas as pd

class MapsController:
    def __init__(self, connection):
        self.__connection = connection
        
    def generate_map(self):
        try:
            c = self.__connection
            df = pd.read_sql_query("select * from campsAddress",c)
            fig = px.scatter_geo(
                df,lat='address_latitude',lon='address_longitude', hover_name="camp_id", color="camp_id")
            fig.update_layout(title = 'Refugee Camps Map', title_x=0.5)
            return fig.show()
        except Exception as e:
                return False

    def generate_latlong(self,address,camp_id):
        geolocator = Nominatim(user_agent="RefugeeApp")
        loc = geolocator.geocode(address)
        try:
            c = self.__connection.cursor()    
            sql = f"INSERT INTO campsAddress VALUES('{camp_id}','{loc.address}','{loc.latitude}','{loc.longitude}')"
            c.execute(sql)
            self.__connection.commit()
            print("coordinates inserted")
            return True
        except Exception as e:
                return False

    def update_address(self,address,camp_id):
        geolocator = Nominatim(user_agent="RefugeeApp")
        location = geolocator.geocode(address)
        try:
            c = self.__connection.cursor()    
            sql = f"UPDATE campsAddress SET address='{location.address}', \
            address_latitude={location.latitude},address_longitude={location.longitude} \
            WHERE camp_id = {camp_id}"
            c.execute(sql)
            self.__connection.commit()
            return True
        except Exception as e:
            return False

    def remove_address(self, camp_id):
        try:
            c = self.__connection.cursor()    
            sql = f"DELETE FROM campsAddress WHERE camp_id = {camp_id}"
            c.execute(sql)
            self.__connection.commit()
            return True
        except Exception as e:
            return False
    
    def get_camp_address(self, camp_id):
        try:
            c = self.__connection.cursor()
            sql = f"SELECT address FROM campsAddress WHERE camp_id = {camp_id}"
            c.execute(sql)
            self.__connection.commit()
            return c.fetchone()[0]
        except Exception as e:
            print(f"The exception/error is: {e}")
            return False

    async def getweather(self,camp_id):
        # declare the client. format defaults to the metric system (celcius, km/h, etc.)
        client = python_weather.Client(format=python_weather.METRIC)

        # fetch a weather forecast from a city
        weather = await client.find(self.get_camp_address(camp_id))
        #self.get_camp_address(

        # returns the current day's forecast temperature (int)
        weather_result =(weather.current.temperature,weather.current.sky_text)
        
        await client.close()
        if __name__ == "__main__":
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.getweather())
        
        return weather_result
