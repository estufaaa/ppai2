class Empleado:
    def __init__(self, nombre, apellido, email, telefono):
        self.apellido = apellido
        self.email = email
        self.nombre = nombre
        self.telefono = telefono

    def getNombreApellido(self):
        return f"{self.nombre} {self.apellido}"