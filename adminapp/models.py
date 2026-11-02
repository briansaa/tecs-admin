import bcrypt
from django.db import models


def es_hash_bcrypt(valor: str) -> bool:
    return bool(valor) and valor.startswith(('$2a$', '$2b$', '$2y$')) and len(valor) == 60


class Usuario(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    # Se guarda el hash BCrypt (60 caracteres), compatible con el BCryptPasswordEncoder de tecs-cliente.
    contrasena = models.CharField(max_length=128)

    def set_password(self, raw: str) -> None:
        self.contrasena = bcrypt.hashpw(raw.encode(), bcrypt.gensalt(rounds=10)).decode()

    def check_password(self, raw: str) -> bool:
        if es_hash_bcrypt(self.contrasena):
            return bcrypt.checkpw(raw.encode(), self.contrasena.encode())
        return self.contrasena == raw  # usuarios antiguos con contraseña en texto plano

    def save(self, *args, **kwargs):
        if self.contrasena and not es_hash_bcrypt(self.contrasena):
            self.set_password(self.contrasena)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.codigo

class Polideportivo(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Pabellon(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Laboratorio(models.Model):
    nombre = models.CharField(max_length=255)
    pabellon = models.ForeignKey(Pabellon, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - {self.pabellon}"
    
class Horario(models.Model):
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.hora_inicio.strftime('%H:%M')} a {self.hora_fin.strftime('%H:%M')}"

class ReservaLaboratorio(models.Model):
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE, default=0)
    fecha = models.DateField()
    Horario = models.ForeignKey(Horario, on_delete=models.CASCADE)
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.laboratorio.nombre} - {self.Horario} - {self.Usuario.codigo}"

class ReservaPolideportivo(models.Model):
    polideportivo = models.ForeignKey(Polideportivo, on_delete=models.CASCADE, default=0)
    fecha = models.DateField()
    Horario = models.ForeignKey(Horario, on_delete=models.CASCADE)
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.polideportivo.nombre} - {self.Horario} - {self.Usuario.codigo}"
