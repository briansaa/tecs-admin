from datetime import date, time

from django.test import TestCase
from rest_framework.test import APIClient

from .models import Horario, Laboratorio, Pabellon, ReservaLaboratorio, Usuario


class UsuarioTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_contrasena_se_guarda_como_hash_y_no_se_devuelve(self):
        res = self.client.post('/adminapp/api/usuarios/', {'codigo': 'U001', 'contrasena': 'secreta123'}, format='json')
        self.assertEqual(res.status_code, 201)
        self.assertNotIn('contrasena', res.data)
        usuario = Usuario.objects.get(codigo='U001')
        self.assertTrue(usuario.contrasena.startswith('$2b$'))
        self.assertTrue(usuario.check_password('secreta123'))
        self.assertFalse(usuario.check_password('otra'))

    def test_listado_no_expone_contrasenas(self):
        Usuario.objects.create(codigo='U002', contrasena='secreta123')
        res = self.client.get('/adminapp/api/usuarios/')
        self.assertEqual(res.status_code, 200)
        self.assertNotIn('contrasena', res.data[0])


class HorarioTests(TestCase):
    def test_hora_fin_debe_ser_posterior(self):
        res = APIClient().post('/adminapp/api/horarios/', {'hora_inicio': '12:00', 'hora_fin': '10:00'}, format='json')
        self.assertEqual(res.status_code, 400)
        self.assertIn('hora_fin', res.data)


class ReservaTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        pabellon = Pabellon.objects.create(nombre='A')
        self.lab = Laboratorio.objects.create(nombre='Lab 101', pabellon=pabellon)
        self.horario = Horario.objects.create(hora_inicio=time(8), hora_fin=time(10))
        self.usuario = Usuario.objects.create(codigo='U003', contrasena='secreta123')
        self.payload = {'laboratorio': self.lab.id, 'fecha': '2026-11-03', 'Horario': self.horario.id, 'Usuario': self.usuario.id}

    def test_crea_reserva(self):
        res = self.client.post('/adminapp/api/reservalaboratorios/', self.payload, format='json')
        self.assertEqual(res.status_code, 201, res.data)

    def test_rechaza_reserva_duplicada(self):
        ReservaLaboratorio.objects.create(laboratorio=self.lab, fecha=date(2026, 11, 3), Horario=self.horario, Usuario=self.usuario)
        res = self.client.post('/adminapp/api/reservalaboratorios/', self.payload, format='json')
        self.assertEqual(res.status_code, 400)
