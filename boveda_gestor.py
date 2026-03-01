import os
import json
from motor_cripto import encriptar, desencriptar

ARCHIVO_PUBLICO = "datos_publicos.dat"
ARCHIVO_PRIVADO = "datos_privados.dat"
ARCHIVO_PELIGRO = "datos_peligro.dat"


class GestorBoveda:
    def __init__(self):
        self.nivel_acceso = "ninguno"
        self.lista_publica = []
        self.lista_privada = []

    def primera_configuracion(self, contra_parcial, contra_total, contra_peligro):
        texto_vacio = b"[]"

        archivo1 = open(ARCHIVO_PUBLICO, "wb")
        archivo1.write(encriptar(texto_vacio, contra_parcial))
        archivo1.close()

        archivo2 = open(ARCHIVO_PRIVADO, "wb")
        archivo2.write(encriptar(texto_vacio, contra_total))
        archivo2.close()

        archivo3 = open(ARCHIVO_PELIGRO, "wb")
        archivo3.write(encriptar(b"PELIGRO", contra_peligro))
        archivo3.close()

    def entrar(self, contrasena):
        if os.path.exists(ARCHIVO_PELIGRO):
            try:
                archivo = open(ARCHIVO_PELIGRO, "rb")
                datos = archivo.read()
                archivo.close()
                if desencriptar(datos, contrasena) == b"PELIGRO":
                    self.nivel_acceso = "peligro"
                    return "peligro"
            except:
                pass

        if os.path.exists(ARCHIVO_PRIVADO):
            try:
                archivo = open(ARCHIVO_PRIVADO, "rb")
                datos = archivo.read()
                archivo.close()
                texto_limpio = desencriptar(datos, contrasena)
                self.lista_privada = json.loads(texto_limpio.decode())
                self.nivel_acceso = "total"
                return "total"
            except:
                pass

        if os.path.exists(ARCHIVO_PUBLICO):
            try:
                archivo = open(ARCHIVO_PUBLICO, "rb")
                datos = archivo.read()
                archivo.close()
                texto_limpio = desencriptar(datos, contrasena)
                self.lista_publica = json.loads(texto_limpio.decode())
                self.nivel_acceso = "parcial"
                return "parcial"
            except:
                pass

        return "error"

    def nueva_credencial(self, sitio, usuario, contrasena, es_privado):
        nuevo_dato = {
            "sitio": sitio,
            "usuario": usuario,
            "contrasena": contrasena
        }


        if es_privado == True and self.nivel_acceso == "total":
            self.lista_privada.append(nuevo_dato)
        else:
            self.lista_publica.append(nuevo_dato)

    def guardar_cambios(self, contrasena):
        if self.nivel_acceso == "parcial":
            texto = json.dumps(self.lista_publica).encode()
            archivo = open(ARCHIVO_PUBLICO, "wb")
            archivo.write(encriptar(texto, contrasena))
            archivo.close()

        if self.nivel_acceso == "total":
            texto = json.dumps(self.lista_privada).encode()
            archivo = open(ARCHIVO_PRIVADO, "wb")
            archivo.write(encriptar(texto, contrasena))
            archivo.close()

    def autodestruccion(self):
        archivos = [ARCHIVO_PUBLICO, ARCHIVO_PRIVADO, ARCHIVO_PELIGRO]
        for nombre in archivos:
            if os.path.exists(nombre):
                os.remove(nombre)