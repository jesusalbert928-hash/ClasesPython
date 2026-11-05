# SE REQUIERE UN SISTEMA DE MONITOREO PARA UNA CALDERA INDUSTRIAL.
# EL SOFTWARE DEBE REGISTRAR LECTURAS DE PRESION DINAMICAMENTE MEDIANTE LA CLASE AUTOREFERENCIADA Nodoeventos y la calases gestora Historialeventos.
# Debe permitir registrar eventos al inicio, contar eventos criticos, mostrar la cadena y realizar una purga de eventos normales reconectando punteros para liberar memorias

class Nodoeventos:
    def __init__(self, id_sensor: str, lectura: float, tiempo: str, estado: str) -> None:
        self.id_sensor, self.lectura, self.tiempo, self.estado = id_sensor, lectura, tiempo, estado
        self.siguiente: "Nodoeventos | None" = None


class HistorialDeEventos:
    def __init__(self) -> None:
        self.cabeza: "Nodoeventos | None" = None
    def registro_evento(self, id_sensor: str, lectura: float, tiempo: str) -> None:
        estado = "CRITICO" if lectura > 95 else "NORMAL"
        nuevo = Nodoeventos(id_sensor, lectura, tiempo, estado)
        nuevo.siguiente, self.cabeza = self.cabeza, nuevo
        
    def contar_criticos(self) -> int:
        c, act = 0, self.cabeza
        while act:
            if act.estado == "CRITICO": 
                c += 1
            act = act.siguiente
        return c

    def mostrar_cadena(self) -> None:
        act = self.cabeza
        while act:
            print(f"[{act.id_sensor} | {act.lectura}PSI | {act.estado}] -> ", end="")
            act = act.siguiente
        print("None")

    def purgar_normales(self) -> None:
        while self.cabeza and self.cabeza.estado == "NORMAL":
            self.cabeza = self.cabeza.siguiente
        act = self.cabeza
        while act and act.siguiente:
            if act.siguiente.estado == "NORMAL":
                act.siguiente = act.siguiente.siguiente
            else:
                act = act.siguiente


# --- BLOQUE DE EJECUCIÓN ---
if __name__ == "__main__":
    historial = HistorialDeEventos()
    
    # Registrar eventos (los mayores a 95 se marcan como CRITICO automáticamente)
    historial.registro_evento("Sensor_1", 80.0, "10:00")
    historial.registro_evento("Sensor_2", 102.5, "10:05")
    historial.registro_evento("Sensor_3", 75.0, "10:10")
    historial.registro_evento("Sensor_4", 110.0, "10:15")

    print("--- Cadena Inicial ---")
    historial.mostrar_cadena()

    print(f"Total críticos: {historial.contar_criticos()}")

    # Purgar normales
    historial.purgar_normales()

    print("\n--- Cadena Después de Purgar Normales ---")
    historial.mostrar_cadena()