import json
import time
import subprocess
from filelock import FileLock

def count_tasks():
    """
    Devuelve la cantidad de tareas pendientes en tasks.json.
    """
    lock = FileLock("tasks.json.lock")
    with lock:
        try:
            with open("tasks.json", "r") as f:
                tasks = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            tasks = []
    return len(tasks)

def monitor_consumer_pool(
    min_consumers=0,       # Número mínimo de consumidores. Se permite que sea 0 para que todos terminen.
    max_consumers=5,       # Máximo de consumidores.
    high_threshold=5,      # Umbral alto para lanzar más consumidores.
    low_threshold=2,       # Umbral bajo para reducir consumidores.
    check_interval=3       # Intervalo de tiempo (segundos) entre chequeos.
):
    consumer_processes = []

    # Iniciamos con el número mínimo de consumidores
    for _ in range(min_consumers):
        p = subprocess.Popen(["python", "consumer.py"])
        consumer_processes.append(p)
    print(f"Monitor: Iniciado con {min_consumers} consumidores.")

    try:
        while True:
            tasks_count = count_tasks()
            print(f"Monitor: Tareas pendientes: {tasks_count}, consumidores activos: {len(consumer_processes)}")

            # Escalar consumidores si hay muchas tareas y no hemos llegado al máximo
            if tasks_count > high_threshold and len(consumer_processes) < max_consumers:
                p = subprocess.Popen(["python", "consumer.py"])
                consumer_processes.append(p)
                print("Monitor: Se añadió un nuevo consumidor.")

            # Desescalar consumidores si hay pocas tareas y tenemos más que el mínimo
            if tasks_count < low_threshold and len(consumer_processes) > min_consumers:
                p = consumer_processes.pop()
                p.terminate()
                print("Monitor: Se eliminó un consumidor.")

            # Si no hay tareas pendientes y no quedan consumidores, salimos del bucle
            if tasks_count == 0 and len(consumer_processes) == min_consumers:
                # Si min_consumers = 0, significa que ya no tenemos ningún consumidor vivo
                # Si min_consumers > 0, aquí se quedaría el número mínimo de consumidores
                #   (puedes ajustar la lógica si quieres cerrar incluso con min_consumers > 0)
                if min_consumers == 0:
                    print("Monitor: No hay tareas pendientes y no hay consumidores activos, cerrando monitor.")
                    break
                else:
                    print("Monitor: No hay tareas pendientes, pero mantenemos el mínimo de consumidores activo.")
                    # Si deseas cerrarlo aunque min_consumers sea > 0, simplemente haz:
                    # break
                    # en vez de este else.
            
            time.sleep(check_interval)

    except KeyboardInterrupt:
        print("Monitor: Recibido KeyboardInterrupt. Terminando consumidores...")

    finally:
        # Cierra a todos los consumidores antes de salir
        for p in consumer_processes:
            p.terminate()
        for p in consumer_processes:
            p.wait()
        print("Monitor: Todos los consumidores terminados.")

if __name__ == "__main__":
    monitor_consumer_pool()
