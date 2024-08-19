import subprocess
import json
import csv
import os
import time
from datetime import datetime

# Lista de servidores específicos (ID y nombre)
servers = [
    {'id': '62779', 'name': 'PRITS_SJ'},
    {'id': '22807', 'name': 'FiberX'},
    {'id': '63832', 'name': 'PRITS_Ponce'},
    {'id': '35678', 'name': 'Miami Gold Data'},
    {'id': '22504', 'name': 'Claro Bayamon'},
    {'id': '22503', 'name': 'Claro Guaynabo'},
    # Agrega más servidores aquí según sea necesario
]

def run_speedtest(server_id):
    # Ejecuta una prueba de velocidad en un servidor específico
    print(f"Iniciando prueba en el servidor {server_id}...")
    result = subprocess.run(['./speedtest', '--server-id', str(server_id), '--format', 'json'], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error al ejecutar la prueba en el servidor {server_id}.")
        print(result.stderr)
        return None

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(f"Error al decodificar la respuesta JSON: {e}")
        return None

def save_to_csv(data, filename='speedtest_results.csv'):
    # Guarda los datos en un archivo CSV
    file_exists = os.path.isfile(filename)
    
    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerows(data)

def main():
    results = []
    
    for server in servers:
        server_id = server['id']
        server_name = server.get('name', 'Unknown')  # Usa 'Unknown' si 'name' no está presente
        print(f"Ejecutando prueba en el servidor {server_id} - {server_name}")
        result = run_speedtest(server_id)
        
        if result:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            results.append({
                'Date and Time': current_time,
                'Result ID': result['result']['id'],
                'Result Link': result['result']['url'],
                'Public IP': result['interface']['externalIp'],
                'Server ID': server_id,
                'Server Name': server_name,
                'Ping (ms)': result.get('ping', {}).get('latency', 'N/A'),
                'Download (Mbps)': result.get('download', {}).get('bandwidth', 0) / 125000,
                'Download Latency (ms)': result.get('download', {}).get('latency', {}).get('iqm', 'N/A'),
                'Upload (Mbps)': result.get('upload', {}).get('bandwidth', 0) / 125000,
                'Upload Latency (ms)': result.get('upload', {}).get('latency', {}).get('iqm', 'N/A')
            })
        time.sleep(1)  # Pausa entre pruebas para evitar sobrecargar la red
    
    if results:
        save_to_csv(results)
        print("Resultados guardados en 'speedtest_results.csv'")
    else:
        print("No se obtuvieron resultados válidos.")

if __name__ == "__main__":
    main()
