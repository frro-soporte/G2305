# Implementar los metodos de la capa de negocio de socios.

from practico_05.ejercicio_01 import Socio
from practico_05.ejercicio_02 import DatosSocio


class DniRepetido(Exception):
    pass


class LongitudInvalida(Exception):
    pass


class MaximoAlcanzado(Exception):
    pass


class NegocioSocio(object):

    MIN_CARACTERES = 3
    MAX_CARACTERES = 15
    MAX_SOCIOS = 200

    def __init__(self):
        self.datos = DatosSocio()

    def buscar(self, id_socio):
        """
        Devuelve la instancia del socio, dado su id.
        Devuelve None si no encuentra nada.
        :rtype: Socio
        """
        return self.datos.buscar(id_socio)


    def buscar_dni(self, dni_socio):
        """
        Devuelve la instancia del socio, dado su dni.
        Devuelve None si no encuentra nada.
        :rtype: Socio
        """
        return self.datos.buscar_dni(dni_socio)

    def todos(self):
        """
        Devuelve listado de todos los socios.
        :rtype: list
        """

        return self.datos.todos()

    def alta(self, socio):
        """
        Da de alta un socio.
        Se deben validar las 3 reglas de negocio primero.
        Si no validan, levantar la excepcion correspondiente.
        Devuelve True si el alta fue exitoso.
        :type socio: Socio
        :rtype: bool
        """
        if  self.regla_1(socio) and   self.regla_2(socio) and  self.regla_3():
            socio_insertado = self.datos.alta(socio)
            return bool(socio_insertado.id)
        return False

    def baja(self, id_socio):
        """
        Borra el socio especificado por el id.
        Devuelve True si el borrado fue exitoso.
        :rtype: bool
        """
        return self.datos.baja(id_socio)

    def modificacion(self, socio):
        """
        Modifica un socio.
        Se debe validar la regla 2 primero.
        Si no valida, levantar la excepcion correspondiente.
        Devuelve True si la modificacion fue exitosa.
        :type socio: Socio
        :rtype: bool
        """
        if self.regla_2(socio):
            self.datos.modificacion(socio)
        else:
            raise LongitudInvalida
        return False

    def regla_1(self, socio):
        """
        Validar que el DNI del socio es unico (que ya no este usado).
        :type socio: Socio
        :raise: DniRepetido
        :return: bool
        """
        socio = self.datos.buscar_dni(socio.dni)
        if socio is not None:
            # Si ya existe un socio con el mismo DNI, lanzamos una excepción
            raise DniRepetido("El DNI ya está en uso.")
        return not bool(socio)

    def regla_2(self, socio):
        """
        Validar que el nombre y el apellido del socio cuenten con mas de 3 caracteres pero menos de 15.
        :type socio: Socio
        :raise: LongitudInvalida
        :return: bool
        """
        nombre_valido = self.MIN_CARACTERES <= len(socio.nombre) <= self.MAX_CARACTERES
        apellido_valido = self.MIN_CARACTERES <= len(socio.apellido) <= self.MAX_CARACTERES

        if not nombre_valido or not apellido_valido:
            # Si no cumplen con la longitud válida, lanzamos una excepción
            raise LongitudInvalida("El nombre y el apellido deben tener entre 3 y 15 caracteres.")

        return True

    def regla_3(self):
        """
        Validar que no se esta excediendo la cantidad maxima de socios.
        :raise: MaximoAlcanzado
        :return: bool
        """
        # Validar que no se está excediendo la cantidad máxima de socios
        cant_socios = self.datos.contarSocios()
        if cant_socios >= self.MAX_SOCIOS:
            # Si se alcanzó el límite máximo de socios, lanzamos una excepción
            raise MaximoAlcanzado("Se ha alcanzado el límite máximo de socios.")
        return True
