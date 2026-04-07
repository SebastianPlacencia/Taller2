# Sistema de Simulación y Monitoreo de Temperatura en ROS 2

Este repositorio contiene los scripts fuente en Python para un sistema de simulación, lectura y graficación de datos de temperatura utilizando el framework ROS 2. El entorno de ejecución está containerizado mediante Docker para asegurar la reproducibilidad y facilitar el desarrollo continuo mediante volúmenes compartidos.

## Arquitectura de Nodos

El proyecto se compone de tres nodos principales de ROS 2:

* **sensor_node.py**: Actúa como publicador. Genera y publica datos de temperatura simulada en un tópico específico a una frecuencia predeterminada.
* **reader_node.py**: Actúa como suscriptor. Recibe la información del nodo sensor, procesa los datos y los expone en la terminal para su verificación en tiempo real.
* **plotter_node.py**: Actúa como nodo de visualización y almacenamiento. Se suscribe a los datos procesados y utiliza bibliotecas de graficación (ej. Matplotlib) para generar un gráfico actualizado cada 5 segundos. La imagen resultante (`sensor_plot.png`) se exporta automáticamente a un volumen compartido.

## Configuración del Entorno (Docker)

El sistema está diseñado para ejecutarse dentro de un contenedor Docker automatizado. 

### 1. Dockerfile y Entrypoint
El despliegue utiliza un `Dockerfile` que automatiza la instalación de dependencias y la configuración del espacio de trabajo de ROS 2. 
Es imperativo que el archivo mantenga la instrucción `ENTRYPOINT ["/ros_entrypoint.sh"] CMD ["bash"]`. El script `ros_entrypoint.sh` proveído por la imagen oficial de ROS 2 se encarga de cargar las variables de entorno necesarias (`source /opt/ros/<distro>/setup.bash`) antes de ejecutar cualquier comando en el contenedor, garantizando que las bibliotecas de ROS 2 estén disponibles en el PATH.

### 2. Volúmenes Compartidos (Shared Folder)
Para facilitar el desarrollo y la extracción de datos, se emplea un volumen compartido entre el sistema host y el contenedor. 
* **Desarrollo:** Los archivos `sensor_node.py`, `reader_node.py` y `plotter_node.py` residen físicamente en el host, permitiendo su edición mediante cualquier IDE local. Estos cambios se reflejan instantáneamente dentro del contenedor.
* **Extracción de Gráficos:** El nodo `plotter_node` ejecuta la instrucción `plt.savefig('/ros2_ws/data/sensor_plot.png')`. Al mapear el directorio `/ros2_ws/data/` del contenedor hacia una carpeta local en el host, la gráfica generada queda inmediatamente accesible en el sistema operativo base sin necesidad de extracción manual.

## Instrucciones de Ejecución

Una vez que el contenedor esté en ejecución y el paquete compilado mediante `colcon build`, abra tres terminales independientes con acceso al contenedor y ejecute los nodos en el siguiente orden:

**Terminal 1: Iniciar el nodo sensor**
ros2 run sensor_serial sensor_node

**Terminal 2: Iniciar el nodo reader**
ros2 run sensor_serial sensor_reader

**Terminal 1: Iniciar el nodo plotter**
ros2 run sensor_serial sensor_node
