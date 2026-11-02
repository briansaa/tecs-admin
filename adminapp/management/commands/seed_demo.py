from datetime import time

from django.core.management.base import BaseCommand

from adminapp.models import Horario, Laboratorio, Pabellon, Polideportivo, Usuario


class Command(BaseCommand):
    help = 'Carga pabellones, laboratorios, polideportivos, horarios y un usuario de prueba.'

    def handle(self, *args, **options):
        pab_a, _ = Pabellon.objects.get_or_create(nombre='Pabellón A')
        pab_b, _ = Pabellon.objects.get_or_create(nombre='Pabellón B')
        for nombre, pabellon in [('Lab. Cómputo 101', pab_a), ('Lab. Redes 102', pab_a), ('Lab. Electrónica 201', pab_b)]:
            Laboratorio.objects.get_or_create(nombre=nombre, pabellon=pabellon)
        for nombre in ['Cancha de Fútbol', 'Cancha de Vóley', 'Cancha de Básquet']:
            Polideportivo.objects.get_or_create(nombre=nombre)
        for inicio, fin in [(8, 10), (10, 12), (14, 16), (16, 18)]:
            Horario.objects.get_or_create(hora_inicio=time(inicio), hora_fin=time(fin))
        if not Usuario.objects.filter(codigo='U2024001').exists():
            Usuario.objects.create(codigo='U2024001', contrasena='demo1234')
        self.stdout.write(self.style.SUCCESS('Datos de prueba listos. Usuario: U2024001 / demo1234'))
