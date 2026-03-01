import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip
import secrets
import string
import os

from boveda_gestor import GestorBoveda


class Aplicacion:
    def __init__(self, ventana_principal):
        self.ventana = ventana_principal
        self.ventana.title("Gestor VirtusKey")
        self.ventana.geometry("600x450")

        self.gestor = GestorBoveda()
        self.contrasena_usada = ""

        if os.path.exists("datos_publicos.dat") == False:
            self.mostrar_configuracion()
        else:
            self.mostrar_login()

    def borrar_pantalla(self):
        for cosita in self.ventana.winfo_children():
            cosita.destroy()

    def mostrar_configuracion(self):
        self.borrar_pantalla()
        marco = tk.Frame(self.ventana)
        marco.pack(pady=40)

        tk.Label(marco, text="Bienvenido. Crea tus 3 claves:", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(marco, text="Clave Parcial:").pack()
        caja_parcial = tk.Entry(marco, show="*")
        caja_parcial.pack(pady=5)

        tk.Label(marco, text="Clave Total:").pack()
        caja_total = tk.Entry(marco, show="*")
        caja_total.pack(pady=5)

        tk.Label(marco, text="Clave de Peligro Extremo:").pack()
        caja_peligro = tk.Entry(marco, show="*")
        caja_peligro.pack(pady=5)

        def boton_crear():
            c1 = caja_parcial.get()
            c2 = caja_total.get()
            c3 = caja_peligro.get()

            if c1 != "" and c2 != "" and c3 != "":
                self.gestor.primera_configuracion(c1, c2, c3)
                messagebox.showinfo("Exito", "Todo configurado. Ya puedes entrar.")
                self.mostrar_login()
            else:
                messagebox.showerror("Aviso", "Rellena todas las cajas")

        tk.Button(marco, text="Guardar Claves", command=boton_crear).pack(pady=15)

    def mostrar_login(self):
        self.borrar_pantalla()
        marco = tk.Frame(self.ventana)
        marco.pack(pady=50)

        tk.Label(marco, text="Inicia sesión en VirtusKey", font=("Arial", 16, "bold")).pack(pady=10)

        self.caja_login = tk.Entry(marco, show="*")
        self.caja_login.pack(pady=10)

        tk.Button(marco, text="Entrar", command=self.comprobar_login).pack()

    def comprobar_login(self):
        clave = self.caja_login.get()
        resultado = self.gestor.entrar(clave)

        if resultado == "parcial" or resultado == "total":
            self.contrasena_usada = clave
            self.mostrar_menu()
        elif resultado == "peligro":
            self.gestor.autodestruccion()
            messagebox.showwarning("PELIGRO", "Archivos borrados. Cerrando programa.")
            self.ventana.quit()
        else:
            messagebox.showerror("Error", "Clave incorrecta")

    def mostrar_menu(self):
        self.borrar_pantalla()
        marco = tk.Frame(self.ventana)
        marco.pack(pady=50)

        texto_nivel = "Nivel de acceso: " + self.gestor.nivel_acceso
        tk.Label(marco, text=texto_nivel, font=("Arial", 14)).pack(pady=15)

        tk.Button(marco, text="Añadir nueva contraseña", command=self.mostrar_añadir).pack(pady=5)
        tk.Button(marco, text="Ver mis contraseñas", command=self.mostrar_lista).pack(pady=5)
        tk.Button(marco, text="Guardar y Salir", command=self.salir_programa).pack(pady=20)

    def mostrar_añadir(self):
        self.borrar_pantalla()
        marco = tk.Frame(self.ventana)
        marco.pack(pady=30)

        tk.Label(marco, text="Sitio web:").grid(row=0, column=0, pady=5)
        caja_sitio = tk.Entry(marco)
        caja_sitio.grid(row=0, column=1)

        tk.Label(marco, text="Usuario:").grid(row=1, column=0, pady=5)
        caja_user = tk.Entry(marco)
        caja_user.grid(row=1, column=1)

        tk.Label(marco, text="Contraseña:").grid(row=2, column=0, pady=5)
        self.caja_pass = tk.Entry(marco)
        self.caja_pass.grid(row=2, column=1)

        tk.Button(marco, text="Generar Random", command=self.crear_pass_random).grid(row=3, column=1, pady=5)

        self.opcion_privada = tk.BooleanVar(value=False)
        if self.gestor.nivel_acceso == "total":
            tk.Checkbutton(marco, text="Es privada", variable=self.opcion_privada).grid(row=4, column=1)

        def guardar_todo():
            s = caja_sitio.get()
            u = caja_user.get()
            p = self.caja_pass.get()
            priv = self.opcion_privada.get()

            if s != "" and u != "" and p != "":
                self.gestor.nueva_credencial(s, u, p, priv)
                self.gestor.guardar_cambios(self.contrasena_usada)
                messagebox.showinfo("Genial", "Contraseña guardada")
                self.mostrar_menu()
            else:
                messagebox.showerror("Error", "Rellena todo por favor")

        tk.Button(marco, text="Guardar", command=guardar_todo).grid(row=5, column=0, pady=20)
        tk.Button(marco, text="Atrás", command=self.mostrar_menu).grid(row=5, column=1)

    def crear_pass_random(self):
        letras_y_numeros = string.ascii_letters + string.digits + string.punctuation
        clave_nueva = ""

        for i in range(16):
            letra_suelta = secrets.choice(letras_y_numeros)
            clave_nueva = clave_nueva + letra_suelta

        self.caja_pass.delete(0, tk.END)
        self.caja_pass.insert(0, clave_nueva)

    def mostrar_lista(self):
        self.borrar_pantalla()
        marco = tk.Frame(self.ventana)
        marco.pack(pady=20, fill="both", expand=True)

        columnas = ("Sitio", "Usuario", "Pass")
        self.tabla = ttk.Treeview(marco, columns=columnas, show='headings')
        self.tabla.heading("Sitio", text="Sitio")
        self.tabla.heading("Usuario", text="Usuario")
        self.tabla.heading("Pass", text="Contraseña")
        self.tabla.pack(fill="both", expand=True)

        if self.gestor.nivel_acceso == "total":
            lista_a_mostrar = self.gestor.lista_privada
        else:
            lista_a_mostrar = self.gestor.lista_publica

        for elemento in lista_a_mostrar:
            self.tabla.insert("", "end", values=(elemento["sitio"], elemento["usuario"], "****"),
                              tags=(elemento["contrasena"],))

        def copiar_pass():
            fila_elegida = self.tabla.selection()
            if len(fila_elegida) > 0:  # Si hay algo seleccionado
                id_fila = fila_elegida[0]
                clave_de_verdad = self.tabla.item(id_fila, "tags")[0]
                pyperclip.copy(clave_de_verdad)
                messagebox.showinfo("Copiada", "Ya puedes pegarla donde quieras")
            else:
                messagebox.showwarning("Aviso", "Selecciona una fila primero")

        tk.Button(marco, text="Copiar", command=copiar_pass).pack(side="left", padx=10, pady=10)
        tk.Button(marco, text="Atrás", command=self.mostrar_menu).pack(side="left")

    def salir_programa(self):
        if self.contrasena_usada != "" and self.gestor.nivel_acceso != "peligro":
            self.gestor.guardar_cambios(self.contrasena_usada)
        self.ventana.quit()

if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = Aplicacion(ventana_principal)
    ventana_principal.mainloop()
