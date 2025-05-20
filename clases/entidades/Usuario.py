class Usuario:
    def __init__(self, username, password, empleado):
        self.nombreUsuario = username
        self.contraseña = password
        self.empleado = empleado

    def obtenerEmpleado(self):
        return self.empleado
