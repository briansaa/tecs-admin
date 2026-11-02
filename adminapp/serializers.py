from rest_framework import serializers

from .models import (Horario, Laboratorio, Pabellon, Polideportivo,
                     ReservaLaboratorio, ReservaPolideportivo, Usuario)


class UsuarioSerializer(serializers.ModelSerializer):
    # La contraseña nunca se devuelve en las respuestas; al guardarla se convierte a hash BCrypt.
    contrasena = serializers.CharField(write_only=True, min_length=6, max_length=64)

    class Meta:
        model = Usuario
        fields = ['id', 'codigo', 'contrasena']


class PolideportivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Polideportivo
        fields = ['id', 'nombre']


class PabellonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pabellon
        fields = ['id', 'nombre']


class LaboratorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laboratorio
        fields = ['id', 'nombre', 'pabellon']


class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = ['id', 'hora_inicio', 'hora_fin']

    def validate(self, attrs):
        inicio = attrs.get('hora_inicio', getattr(self.instance, 'hora_inicio', None))
        fin = attrs.get('hora_fin', getattr(self.instance, 'hora_fin', None))
        if inicio and fin and fin <= inicio:
            raise serializers.ValidationError({'hora_fin': 'La hora de fin debe ser posterior a la hora de inicio.'})
        return attrs


class _ReservaSerializerBase(serializers.ModelSerializer):
    """Evita que un mismo espacio se reserve dos veces en la misma fecha y horario."""
    campo_espacio = None

    def validate(self, attrs):
        espacio = attrs.get(self.campo_espacio, getattr(self.instance, self.campo_espacio, None))
        fecha = attrs.get('fecha', getattr(self.instance, 'fecha', None))
        horario = attrs.get('Horario', getattr(self.instance, 'Horario', None))
        ocupado = self.Meta.model.objects.filter(**{self.campo_espacio: espacio}, fecha=fecha, Horario=horario)
        if self.instance is not None:
            ocupado = ocupado.exclude(pk=self.instance.pk)
        if ocupado.exists():
            raise serializers.ValidationError('Ese espacio ya está reservado en la fecha y horario elegidos.')
        return attrs


class ReservaLaboratorioSerializer(_ReservaSerializerBase):
    campo_espacio = 'laboratorio'

    class Meta:
        model = ReservaLaboratorio
        fields = ['id', 'laboratorio', 'fecha', 'Horario', 'Usuario']


class ReservaPolideportivoSerializer(_ReservaSerializerBase):
    campo_espacio = 'polideportivo'

    class Meta:
        model = ReservaPolideportivo
        fields = ['id', 'polideportivo', 'fecha', 'Horario', 'Usuario']
