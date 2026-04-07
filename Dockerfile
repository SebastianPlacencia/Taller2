# 1. Base oficial de ROS2 Jazzy
FROM osrf/ros:jazzy-desktop

# 2. Instalación de herramientas
# Se Añade python3-matplotlib 
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    python3-colcon-common-extensions \
    nano \
    python3-matplotlib \
    && rm -rf /var/lib/apt/lists/*

# 3. Creación del Workspace automatizado
RUN mkdir -p /root/ros2_ws/src

# 4. Configuración automática del source
RUN echo "source /opt/ros/jazzy/setup.bash" >> /root/.bashrc

# Definimos el directorio de trabajo predeterminado
WORKDIR /root/ros2_ws

# 5. Mantenemos el entrypoint original
ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]

