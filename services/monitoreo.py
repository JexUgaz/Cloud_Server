import subprocess
import time
import csv

def guardar_tiempos_idle_en_csv(workers, duracion_total=300, intervalo=5):
    tiempo_inicio = time.time()
    tiempo_actual = tiempo_inicio

    try:
        while tiempo_actual - tiempo_inicio < duracion_total:
            for i, worker_info in enumerate(workers):
                tiempo_idle = obtener_tiempo_idle(worker_info)

                if tiempo_idle is not None:
                    # Obtener el tiempo actual con milisegundos
                    tiempo_actual_con_milisegundos = time.time()
                    tiempo_milisegundos = int((tiempo_actual_con_milisegundos - int(tiempo_actual_con_milisegundos)) * 1000)

                    # Formatear la marca de tiempo con Hora:minutos:segundos:milisegundos
                    marca_tiempo = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(tiempo_actual_con_milisegundos))
                    marca_tiempo_con_milisegundos = f"{marca_tiempo}:{tiempo_milisegundos:03}"

                    # Guardar en el archivo CSV
                    with open(f"worker{i+1}_tiempos_idle.csv", mode='a', newline='') as archivo_csv:
                        csv_writer = csv.writer(archivo_csv)
                        csv_writer.writerow([marca_tiempo_con_milisegundos, tiempo_idle])

            time.sleep(intervalo)
            tiempo_actual = time.time()

    except KeyboardInterrupt:
        print("Proceso interrumpido por el usuario.")
    
    finally:
        print("Guardado finalizado.")

def obtener_tiempo_idle(worker_info):
    try:
        comando = f"ssh {worker_info[1]}@{worker_info[0]} cat /proc/stat | head -n 1 | awk '{{print $5}}'"
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)

        if resultado.returncode == 0:
            tiempo_idle = int(resultado.stdout.strip())
            return tiempo_idle
        else:
            print(f"Error al ejecutar el comando. Código de retorno: {resultado.returncode}")
            return None

    except Exception as e:
        print(f"Error al obtener el tiempo idle: {e}")
        return None

def main():

    workers = [
        ("10.0.0.30", "ubuntu", "ubuntu"),
        ("10.0.0.40", "ubuntu", "ubuntu"),
        ("10.0.0.50", "ubuntu", "ubuntu")
    ]
    guardar_tiempos_idle_en_csv(workers)

# Uso de la función para cada worker
if __name__ == "__main__":
    main()