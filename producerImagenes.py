import json
import random

def main():
    num_images = 50  # Número total de tareas a generar (aumentado a 50)
    tasks = []
    for i in range(num_images):
        # Simulamos la generación de una imagen como un diccionario
        task = {"id": i, "data": f"Imagen_{random.randint(1000, 9999)}"}
        tasks.append(task)
    # Guardamos todas las tareas en un archivo JSON
    with open("tasks.json", "w") as f:
        json.dump(tasks, f, indent=4)
    print(f"Productor: Se han generado {num_images} tareas en tasks.json")

if __name__ == "__main__":
    main()
