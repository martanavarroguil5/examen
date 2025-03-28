# examen
Proyecto de Procesamiento de Imágenes
Requisitos

filelock: Instálalo con:

bash
pip install filelock



Archivos Principales
producerImagenes.py: Genera tareas (imágenes) en tasks.json.

consumer.py: Procesa las tareas y guarda resultados en results.json.

monitor.py: Ajusta la cantidad de procesos consumer según la carga.



Ejecución
Ejecuta el producer y cuando aarezca el mensaje en terminal de que se ha inicializado y, ejecuta el monitor. No se hace se parando terminales, es todo en la misma terminal dando al run de una y luego el de la otra. en el script de monitor se imlementa ya de base la  proceso de consumers

