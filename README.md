# Práctica: Simulación y Lectura de Temperatura con ROS 2 y Docker

Este repositorio contiene los archivos de Python desarrollados para la práctica de simulación, lectura y graficación de datos de un sensor de temperatura usando ROS 2. Todo el entorno está montado en Docker para no tener que instalar ROS 2 directamente en la computadora.

## Nodos del Proyecto

El sistema funciona con tres nodos principales de ROS 2 que se comunican entre sí:

* **sensor_node.py**: Es el publicador. Se encarga de simular las lecturas de un sensor de temperatura y enviar (publicar) esos datos constantemente a un tópico.
* **reader_node.py**: Es el suscriptor. Escucha el tópico del sensor, recibe los datos de temperatura y los imprime en la terminal para que podamos verlos.
* **plotter_node.py**: Es un nodo extra que también escucha los datos del sensor, pero en lugar de solo imprimirlos, usa una librería (como Matplotlib) para dibujar un gráfico. Este gráfico se actualiza y se guarda como imagen (`sensor_plot.png`) cada 5 segundos.

## Configuración de Docker

Para que todo esto funcione sin problemas, configuramos un contenedor con algunas características clave:

### 1. Dockerfile y el Entrypoint
Usamos un `Dockerfile` para automatizar la instalación de las herramientas necesarias. Un detalle súper importante en este archivo es que mantenemos la línea:
`ENTRYPOINT ["/ros_entrypoint.sh"] CMD ["bash"]`

Es necesario el archivo `ros_entrypoint.sh` (que ya viene en la imagen oficial de ROS 2) se encarga de ejecutar automáticamente el comando `source` del entorno de ROS. Si quitamos esa línea, el contenedor arrancaría, pero la terminal no reconocería ningún comando de ROS 2 (como `ros2 run` o `colcon build`).

### 2. Carpeta Compartida (Shared Folder)
Para no tener que estar copiando archivos a cada rato dentro del contenedor, configuramos un volumen compartido (Shared folder) entre nuestra computadora y Docker. Esto nos da dos grandes ventajas:
* **Para programar:** Podemos tener los archivos `sensor_node.py`, `reader_node.py` y `plotter_node.py` en nuestra compu y editarlos cómodamente con nuestro propio IDE. Los cambios se actualizan en el contenedor de inmediato.
* **Para ver los resultados:** Como el `plotter_node` guarda la gráfica con el comando `plt.savefig('/ros2_ws/data/sensor_plot.png')`, al estar esa carpeta enlazada a nuestra computadora, la imagen del gráfico aparece directamente en nuestros archivos locales sin tener que hacer nada extra.

## Pasos para ejecutarlo

Una vez que el contenedor de Docker esté corriendo y los paquetes estén compilados, abre tres terminales diferentes (todas dentro del contenedor) y ejecuta un nodo en cada una:

**Terminal 1: Iniciar el nodo sensor**
ros2 run sensor_serial sensor_node

**Terminal 2: Iniciar el nodo reader**
ros2 run sensor_serial sensor_reader

**Terminal 1: Iniciar el nodo plotter**
ros2 run sensor_serial sensor_node
