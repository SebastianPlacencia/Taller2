import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import matplotlib.pyplot as plt
import re # Para extraer el número del string

class PlotterNode(Node):
    def __init__(self):
        super().__init__('plotter_node')
        self.subscription = self.create_subscription(
            String, 'sensor_data', self.listener_callback, 10)
        
        # Timer para graficar cada 5 segundos
        self.timer = self.create_timer(5.0, self.plot_data)
        
        self.temperaturas = []
        self.lecturas = []
        self.contador = 0
        self.get_logger().info('Plotter iniciado. Guardando gráfico cada 5s...')

    def listener_callback(self, msg):
        # El mensaje viene como "Temperatura: 25C". Extraemos solo el número:
        match = re.search(r'\d+', msg.data)
        if match:
            temp = int(match.group())
            self.temperaturas.append(temp)
            self.lecturas.append(self.contador)
            self.contador += 1

    def plot_data(self):
        if not self.temperaturas:
            return
        
        # Configurar tamaño de la figura (más panorámico)
        plt.figure(figsize=(8, 5))
        
        # Graficar la línea principal con marcadores elegantes
        plt.plot(self.lecturas, self.temperaturas, 
                 marker='o', markersize=6, markerfacecolor='white', 
                 markeredgewidth=2, color='#FF5733', linewidth=2.5, 
                 label='Temperatura')
        
        # Rellenar el área debajo de la curva
        plt.fill_between(self.lecturas, self.temperaturas, color='#FF5733', alpha=0.2)
        
        # Configurar títulos y etiquetas
        plt.title('Historial de Temperatura del Sensor', fontsize=14, fontweight='bold')
        plt.xlabel('Número de Lectura', fontsize=11, fontweight='bold')
        plt.ylabel('Temperatura (°C)', fontsize=11, fontweight='bold')
        
        # Configurar los ejes y la grilla
        plt.ylim(15, 35) # Límites estáticos basados en los datos (20-30)
        plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
        plt.legend(loc='upper right')
        
        # Ajustar los márgenes para que no se corte nada
        plt.tight_layout()
        
        # Guardar en alta resolución en la carpeta compartida con Windows
        ruta_guardado = '/ros2_ws/data/sensor_plot.png'
        plt.savefig(ruta_guardado, dpi=300)
        plt.close()
        self.get_logger().info(f'Gráfico actualizado en: {ruta_guardado}')

def main(args=None):
    rclpy.init(args=args)
    node = PlotterNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()