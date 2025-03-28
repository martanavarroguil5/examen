import json
import time
import random
import os
from filelock import FileLock

def get_task():
    lock = FileLock("tasks.json.lock")
    with lock:
        try:
            with open("tasks.json", "r") as f:
                tasks = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            tasks = []
        if not tasks:
            return None
        # Extraemos la primera tarea (puedes cambiar la estrategia de extracción)
        task = tasks.pop(0)
        with open("tasks.json", "w") as f:
            json.dump(tasks, f, indent=4)
    return task

def append_result(result):
    lock = FileLock("results.json.lock")
    with lock:
        try:
            with open("results.json", "r") as f:
                results = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            results = []
        results.append(result)
        with open("results.json", "w") as f:
            json.dump(results, f, indent=4)

def process_task(task):
    # Simulación del procesamiento (por ejemplo, análisis o extracción de características)
    time.sleep(random.uniform(0.1, 0.5))
    result = {"id": task["id"], "result": f"{task['data']}_processed"}
    return result

def main():
    while True:
        task = get_task()
        if task is None:
            # No hay tareas; se espera un momento antes de reintentar
            time.sleep(1)
            continue
        result = process_task(task)
        append_result(result)
        print(f"Consumidor {os.getpid()} procesó tarea {task}")

if __name__ == "__main__":
    main()
