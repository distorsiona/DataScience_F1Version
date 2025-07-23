import requests
import pandas as pd

BASE_URL = "https://api.openf1.org/v1"


class OpenF1Client:
    def __init__(self):
        self.base_url = BASE_URL

    def obtener_datos(self, endpoint: str, params: dict = None) -> pd.DataFrame:
        if params is None:
            params = {}
        url = f"{self.base_url}/{endpoint}"
        print(f"Llamando a la URL: {url} con parámetros: {params}")

        try: 
            response = requests.get(url, params=params)
            response.raise_for_status()  #lanza un error si la respuesta no es exitosa
            data = response.json()
            return pd.DataFrame(data)
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener datos de {url}: {e}")
            return pd.DataFrame()
        
        
    def obtener_year_season(self, year: int) -> pd.DataFrame:
        url = "https://api.openf1.org/v1/sessions"
        df_sessions = pd.read_json(url)
        df_filtrado = df_sessions[df_sessions['date_start'].str.startswith(str(year))]
        return df_filtrado.reset_index(drop=True)
    
    def obtenerSessionKeys_drivers(self, driver_number: int = None, year: int = None) -> pd.DataFrame:
        params = {}
        if year:
            params["year"] = year
        if driver_number:
            params["driver_number"] = driver_number

        df = self.obtener_datos("drivers", params)
        print("AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII***************************+")
        print(df)

        if "session_name" in df.columns:
            df = df[df["session_name"]=="Race"]

        print("AQUI VAAAAAAAAAAAA")
        print(df)

        columnas = ['driver_number', 'full_name', 'team_name', 'session_key']
        return df[columnas] if all(c in df.columns for c in columnas) else df
    

    def obtenerLaps_driverYear(self, driver_number: int = None, year: int = None) -> pd.DataFrame:
        carreras = self.obtenerSessionKeys_drivers(driver_number, year)
        if carreras.empty or "session_key" not in carreras.columns:
            print("No se encontraron carreras para el año y/o piloto especificado.")
            return pd.DataFrame()
        
        session_keys = carreras["session_key"].unique().tolist()
        #obtener datos por cada vuelta de la session_key
        laps = []
        for key in session_keys:
            df_lap = self.obtener_datos("laps", {"session_key": key, "driver_number": driver_number})
            if not df_lap.empty:
                df_lap["session_key"] = key
                laps.append(df_lap)
        return pd.concat(laps, ignore_index=True) if laps else pd.DataFrame()

    def obtenerPosicion_driverYear(self, driver_number: int = None, year: int = None) -> pd.DataFrame:
        carrera = self.obtenerSessionKeys_drivers(driver_number, year)
        print(carrera) #######################33

        if carrera.empty or "session_key" not in carrera.columns:
            print("No se encontraron carreras para el año y/o piloto especificado.")
            return pd.DataFrame()
        
        session_keys = carrera["session_key"].unique().tolist()
        posiciones = []
        for key in session_keys:
            df_pos = self.obtener_datos("positions", {"session_key": key, "driver_number": driver_number})
            if not df_pos.empty:
                df_pos["session_key"] = key
                posiciones.append(df_pos)

        return pd.concat(posiciones, ignore_index=True) if posiciones else pd.DataFrame()

    def obtener_drivers(self, driver_numer: int = None,session_key: int = None, year: int = None) -> pd.DataFrame:
        params = {}
        
        if year and not session_key:
            sesiones = self.obtener_year_season(year)
            session_key = sesiones["session_key"].unique().tolist()
            params["session_key"] = session_key

        elif session_key:
            params["session_key"] = session_key

        if driver_numer:
            params["driver_number"] = driver_numer

        return self.obtener_datos("drivers", params)

    
    def obtener_laps(self, session_key: int = None, driver_number: int = None) -> pd.DataFrame:
        params = {}
        if session_key:
            params["session_key"] = session_key
        if driver_number:
            params["driver_number"] = driver_number

        return self.obtener_datos("laps", params)
    


    """
    Retorna un DataFrame con las sesiones de F1 de un año y país específicos, junto a sus session_keys.

    Args:
        cliente: una instancia del cliente OpenF1 (con métodos como `obtener_sessions`)
        year (int): año deseado, por ejemplo 2024
        pais (str): nombre del país tal como aparece en los datos, por ejemplo "Hungary", "Italy", "United Kingdom"

    Returns:
        DataFrame con columnas: ['session_key', 'meeting_key', 'location', 'session_name', 'session_start_time']
    """
    def session_yearAndCountry(self, year: int = None, country: str = None) -> pd.DataFrame:
        df = self.obtener_datos("sessions")

        if df.empty: 
            print("No se pudieron obtener las sesiones.")
            return df
        
        if year:
            df = df[df['date_start'].str.startswith(str(year))]
        
        if country:
            df = df[df['country_name'].str.contains(country, case=False, na=False)]

        df = df[df["session_name"] == "Race"] #opcional si solo se quiere ver las carreras

        columnas = ['session_key', 'meeting_key', 'country_name', 'session_name', 'date_start']
        
        return df[columnas] if all(c in df.columns for c in columnas) else df