# main.py

from src.openf1_client import OpenF1Client

def main():
    cliente = OpenF1Client()

    print("Obteniendo pilotos de 2024...")
    df_drivers = cliente.obtener_drivers(year=2025)
    print(df_drivers.columns)
    print(df_drivers)

    # print("\nObteniendo vueltas del GP de Canadá 2024 (session_key=9636)...")
    # df_laps = cliente.obtener_laps(session_key=9636)
    # print(df_laps[['driver_number', 'lap_number', 'lap_time']].head())


    df_sesiones = cliente.session_yearAndCountry(year=2024, country="Hungary") 
    print("Esto imprime?")
    print(df_sesiones)

    laps_df = cliente.obtenerLaps_driverYear(driver_number=63, year=2024)
    positions_df = cliente.obtenerPosicion_driverYear(driver_number=63, year=2024)


    print(laps_df.head())
    print(positions_df.head())

if __name__ == "__main__":
    main()
