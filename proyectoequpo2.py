from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import csv		
import calendar
import mysql.connector



HOST_SERVIDOR = "localhost"  
DB_CONFIG = { "host": HOST_SERVIDOR, ... }
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "sistema_alertas_temprana"
}

def conectar():
    return mysql.connector.connect(**DB_CONFIG)

def query(sql, params=None, fetch=False):
    conn = conectar()
    cur = conn.cursor()
    cur.execute(sql, params or ())
    data = cur.fetchall() if fetch else None
    conn.commit()
    cur.close()
    conn.close()
    return data

C_BG = "#0a1f3a"
C_BG2 = "#122e55"
C_SIDE = "#071a33"
C_BTN = "#123766"
C_BTN2 = "#1d5aa8"
C_CAMPO = "#2a5a8a"

F_TIT = ("Segoe UI Black", 22)
F_SUB = ("Segoe UI", 12, "bold")
F_TXT = ("Segoe UI", 11)
F_TXT_B = ("Segoe UI", 11, "bold")
F_BTN = ("Segoe UI", 11, "bold")
F_BTN_MENU = ("Segoe UI", 12, "bold")
def revisar_alertas():

def color_campana():
def descargar_pdf():
    
def descargar_csv():
class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de alertas temprana :)")
        self.root.state('zoomed')
        self.root.configure(bg=C_BG)
        box = tk.Frame(root, bg=C_SIDE)
        box.place(relx=0.5, rely=0.5, anchor="center", width=400, height=500)
        tk.Label(box, text="CONTROL ESCOLAR", font=("Segoe UI Black", 24), bg=C_SIDE, fg="white").pack(pady=(40,5))
        tk.Label(box, text="", font=("Segoe UI", 11), bg=C_SIDE, fg="#7aa0cc").pack(pady=(0,25))
        tk.Label(box, text="Usuario:", font=F_SUB, bg=C_SIDE, fg="white", anchor="w").pack(fill="x", padx=40)
        self.u = tk.Entry(box, font=("Segoe UI", 13), bg=C_CAMPO, fg="white", relief="flat")
        self.u.pack(fill="x", padx=40, pady=8, ipady=10)
        self.u.insert(0, "director")
        tk.Label(box, text="Contraseña:", font=F_SUB, bg=C_SIDE, fg="white", anchor="w").pack(fill="x", padx=40, pady=(10,0))
        self.p = tk.Entry(box, font=("Segoe UI", 13), bg=C_CAMPO, fg="white", relief="flat", show="*")
        self.p.pack(fill="x", padx=40, pady=8, ipady=10)
        self.p.insert(0, "123")
        tk.Button(box, text="INICIAR SESIÓN", bg=C_BTN2, fg="white", font=("Segoe UI Black", 12), relief="flat", command=self.login).pack(fill="x", padx=40, pady=35, ipady=12)

    def login(self):
        u = self.u.get().lower().strip()
        p = self.p.get().strip()
        try:
            res = query("SELECT nombre_usuario FROM usuario WHERE nombre_usuario=%s AND contrasena=%s", (u, p), fetch=True)
        except Exception as e:
            messagebox.showerror("Error BD", f"No se pudo conectar a la base:\n{e}\n\n¿Ya ejecutaste base.sql en phpMyAdmin?")
            return
        if not res:
            messagebox.showerror("Error", "Usuario o contraseña incorrecto")
            return
        if u == "docente":
            info = ("Docente", "Panchito", "Grupo 1")
        else:
            info = ("Director", "---", "Escuela Primaria")
        self.root.destroy()
        r = tk.Tk()
        App(r, info[0], info[1], info[2])
        r.mainloop()

class App:
    def __init__(self, root, rol, nombre, grupo):
        self.root = root
        self.rol = rol
        self.nombre = nombre
        self.grupo = grupo
        self.root.title("Sistema de alertas temprana :)")
        self.root.state('zoomed')
        self.root.configure(bg=C_BG)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        self.cargar_datos_db()

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=32, font=F_TXT)
        style.configure("Treeview.Heading", font=F_TXT_B, background=C_SIDE, foreground="white")

        self.side = tk.Frame(root, bg=C_SIDE, width=295)
        self.side.grid(row=0, column=0, sticky="nsew")
        self.side.grid_propagate(False)
        tk.Label(self.side, text=f"Panel\n{rol.upper()}", font=("Segoe UI Black", 16), bg=C_SIDE, fg="white").pack(pady=25)

        if rol == "Director":
            mods = [("Inicio", self.inicio_dir), ("Docentes", self.panel_docentes), ("Historial", self.panel_historial), ("Avisos", self.panel_avisos_director), ("Citatorio", self.panel_citatorio)]
        else:
            mods = [("Inicio", self.inicio_docente), ("Asistencias", self.panel_asistencias), ("Alumnos", self.panel_alumnos_pro), ("Incidencias", self.panel_incidencias), ("Justificantes", self.panel_justificante)]

        for n, fn in mods:
            tk.Button(self.side, text=f"  {n}", font=F_BTN_MENU, bg=C_BTN, fg="white", anchor="w", relief="flat", padx=20, pady=5, command=lambda f=n: self.mostrar(f)).pack(fill="x", padx=12, pady=4, ipady=12)

        tk.Button(self.side, text="  Cerrar Sesión", bg="#5c1a1a", fg="white", font=F_BTN_MENU, relief="flat", command=self.cerrar).pack(side="bottom", fill="x", padx=12, pady=15, ipady=8)

        self.cont = tk.Frame(root, bg=C_BG)
        self.cont.grid(row=0, column=1, sticky="nsew")
        self.cont.rowconfigure(0, weight=1)
        self.cont.columnconfigure(0, weight=1)

        self.paneles = {}
        for n, fn in mods:
            p = tk.Frame(self.cont, bg=C_BG)
            p.grid(row=0, column=0, sticky="nsew")
            fn(p)
            self.paneles[n] = p
        self.mostrar("Inicio")

    def cargar_datos_db(self):
        try:
            rows = query("SELECT tipo FROM asistencia", fetch=True)
            self.contador = {"Asistencia": 0, "Retardo": 0, "Falta": 0, "Justificante": 0}
            for (t,) in rows:
                if t in self.contador:
                    self.contador[t] += 1
            self.alumnos = [r[0] for r in query("SELECT nombre FROM alumno", fetch=True)]
            if not self.alumnos:
                self.alumnos = ["Alumno 1", "Alumno 2", "Alumno 3", "Alumno 4", "Alumno 5"]
            self.historial_asist = [f"{r[2]} - {r[0]} - {r[1]}" for r in query("SELECT tipo, fecha_hora, detalle FROM asistencia", fetch=True)]
            self.historial_just = [r[0] for r in query("SELECT motivo FROM justificante", fetch=True)]
            self.historial_incid = [r[0] for r in query("SELECT descripcion FROM incidencia", fetch=True)]
            self.avisos = [r[0] for r in query("SELECT mensaje FROM aviso", fetch=True)]
            self.citatorios = query("SELECT motivo, fecha_cita, hora, detalles FROM itinerario", fetch=True)
            notif = query("SELECT descripcion FROM incidencia", fetch=True)
            self.notificaciones = [r[0] for r in notif] if notif else ["Sin notificaciones"]
        except Exception as e:
            messagebox.showerror("Error BD", f"No se pudo cargar datos:\n{e}")
            self.contador = {"Asistencia": 0, "Retardo": 0, "Falta": 0, "Justificante": 0}
            self.alumnos = ["Alumno 1", "Alumno 2", "Alumno 3", "Alumno 4", "Alumno 5"]
            self.historial_asist = []
            self.historial_just = []
            self.historial_incid = []
            self.avisos = []
            self.notificaciones = []
            self.citatorios = []

    def mostrar(self, n):
        self.paneles[n].tkraise()
        if n == "Inicio":
            self.root.after(100, self.dibujar)
    def cerrar(self):
        self.root.destroy()
        r = tk.Tk()
        Login(r)
        r.mainloop()
    def encabezado(self, parent, t):
        f = tk.Frame(parent, bg=C_BG)
        f.pack(fill="x", padx=20, pady=12)
        tk.Label(f, text=t.upper(), font=F_TIT, bg=C_BG, fg="white").pack(side="left")

    def inicio_dir(self, parent):
        self.encabezado(parent, f"Director {self.nombre}")
        self.f_dir = tk.Frame(parent, bg=C_BG)
        self.f_dir.pack(fill="both", expand=True, padx=15, pady=5)
        self.f_dir.grid_columnconfigure(0, weight=2)
        self.f_dir.grid_columnconfigure(1, weight=1)
        self.f_dir.grid_rowconfigure(1, weight=0)
        self.f_dir.grid_rowconfigure(2, weight=1)
        self.cards_f = tk.Frame(self.f_dir, bg=C_BG)
        self.cards_f.grid(row=0, column=0, columnspan=2, sticky="ew", pady=8)
        for i in range(4):
            self.cards_f.grid_columnconfigure(i, weight=1)
        self.cards = {}
        cols = ["#0a2a52", "#133b73", "#1e5aa8", "#3a86d6"]
        for i, k in enumerate(["Asistencia", "Retardo", "Falta", "Justificante"]):
            card = tk.Frame(self.cards_f, bg="white")
            card.grid(row=0, column=i, padx=6, sticky="ew")
            tk.Label(card, text=k, font=F_TXT_B, bg="white", fg=C_BG).pack(pady=(10, 0))
            lbl = tk.Label(card, text="0", font=("Segoe UI Black", 22), bg="white", fg=cols[i])
            lbl.pack(pady=(0, 10))
            self.cards[k] = lbl
        self.c_bar = tk.Canvas(self.f_dir, bg="white", height=280, highlightthickness=0)
        self.c_bar.grid(row=1, column=0, sticky="nsew", padx=6, pady=6)
        self.f_info = tk.Frame(self.f_dir, bg=C_BG)
        self.f_info.grid(row=1, column=1, sticky="nsew", padx=6, pady=6)
        self.f_info.grid_columnconfigure((0, 1), weight=1)
        self.box_doc = tk.Frame(self.f_info, bg="white")
        self.box_doc.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        tk.Label(self.box_doc, text="DOCENTES PRESENTES", font=F_TXT_B, bg="white", fg=C_BG).pack(pady=(20, 8))
        try:
            total_doc = query("SELECT COUNT(*) FROM docente", fetch=True)[0][0]
        except:
            total_doc = 6
        self.lbl_doc = tk.Label(self.box_doc, text=f"5/{total_doc}", font=("Segoe UI Black", 36), bg="white", fg="#123766")
        self.lbl_doc.pack()
        self.box_avisos_resumen = tk.Frame(self.f_info, bg="white")
        self.box_avisos_resumen.grid(row=0, column=1, sticky="nsew", padx=(6, 0))
        tk.Label(self.box_avisos_resumen, text="AVISOS ACTIVOS", font=F_TXT_B, bg="white", fg=C_BG).pack(pady=(20, 8))
        self.lbl_avisos_num = tk.Label(self.box_avisos_resumen, text=str(len(self.avisos)), font=("Segoe UI Black", 36), bg="white", fg="#1d5aa8")
        self.lbl_avisos_num.pack()
        self.f_notif_inicio = tk.Frame(self.f_dir, bg="white", bd=2, relief="solid")
        self.f_notif_inicio.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)
        header = tk.Frame(self.f_notif_inicio, bg=C_SIDE)
        header.pack(fill="x")
        tk.Label(header, text=" NOTIFICACIONES ", font=F_SUB, bg=C_SIDE, fg="white", padx=15, pady=10).pack(side="left")
        tk.Label(header, text=f"{len(self.notificaciones)} nuevas", font=F_TXT_B, bg=C_BTN2, fg="white", padx=10, pady=4).pack(side="right", padx=15)
        cont_notif = tk.Frame(self.f_notif_inicio, bg="white")
        cont_notif.pack(fill="both", expand=True, padx=15, pady=12)
        for n in self.notificaciones:
            card = tk.Frame(cont_notif, bg="#eef3fa", bd=1, relief="solid")
            card.pack(fill="x", pady=5, ipady=6)
            tk.Label(card, text=f"> {n}", font=F_TXT, bg="#eef3fa", fg=C_BG, anchor="w", wraplength=900).pack(fill="x", padx=12)

    def dibujar(self):
        if not hasattr(self, 'c_bar'):
            return
        for k in self.cards:
            self.cards[k].config(text=str(self.contador[k]))
        c = self.c_bar
        c.delete("all")
        w = c.winfo_width() or 600
        h = 280
        c.create_text(15, 15, text="Grafica", anchor="w", font=F_TXT_B, fill=C_BG)
        max_v = max(self.contador.values()) or 1
        colores = ["#0a2a52", "#133b73", "#1e5aa8", "#3a86d6"]
        keys = list(self.contador.keys())
        bw = w // 10
        x = 40
        for i, k in enumerate(keys):
            v = self.contador[k]
            alt = int((v / max_v) * 170)
            y0 = h - 35
            y1 = y0 - alt
            c.create_rectangle(x, y0, x + bw, y1, fill=colores[i], outline="")
            c.create_text(x + bw // 2, y1 - 12, text=str(v), font=F_TXT_B, fill=C_BG)
            c.create_text(x + bw // 2, y0 + 12, text=k, font=("Segoe UI", 9, "bold"), fill=C_BG)
            x += bw + 40

    def inicio_docente(self, parent):
        self.encabezado(parent, f"Docente {self.nombre} - {self.grupo}")
        main = tk.Frame(parent, bg=C_BG)
        main.pack(fill="both", expand=True, padx=20, pady=10)
        self.f_cards_doc = tk.Frame(main, bg=C_BG)
        self.f_cards_doc.pack(fill="x", pady=10)
        for i in range(4):
            self.f_cards_doc.grid_columnconfigure(i, weight=1)
        self.cards_doc = {}
        for i, (k, col) in enumerate([("Asistencias", "#0a2a52"), ("Retardos", "#1e5aa8"), ("Faltas", "#0a2a52"), ("Justificantes", "#2a5a8a")]):
            card = tk.Frame(self.f_cards_doc, bg="white")
            card.grid(row=0, column=i, padx=8, sticky="ew")
            tk.Label(card, text=k.upper(), font=F_TXT_B, bg="white", fg=C_BG).pack(pady=(15, 2))
            lbl = tk.Label(card, text="0", font=("Segoe UI Black", 30), bg="white", fg=col)
            lbl.pack(pady=(0, 15))
            self.cards_doc[k] = lbl
        f_avisos = tk.Frame(main, bg="white", bd=2, relief="solid")
        f_avisos.pack(fill="both", expand=True, pady=15)
        header = tk.Frame(f_avisos, bg=C_SIDE)
        header.pack(fill="x")
        tk.Label(header, text="  AVISOS ", font=F_SUB, bg=C_SIDE, fg="white", padx=15, pady=12).pack(side="left")
        tk.Label(header, text=f"{len(self.avisos)} nuevos", font=F_TXT_B, bg="#1d5aa8", fg="white", padx=10, pady=4).pack(side="right", padx=15)
        cont_avisos = tk.Frame(f_avisos, bg="white")
        cont_avisos.pack(fill="both", expand=True, padx=15, pady=15)
        for av in self.avisos:
            card = tk.Frame(cont_avisos, bg="#eef3fa", bd=1, relief="solid")
            card.pack(fill="x", pady=6, ipady=6)
            tk.Label(card, text=f"> {av}", font=F_TXT, bg="#eef3fa", fg=C_BG, anchor="w", wraplength=800, justify="left").pack(fill="x", padx=12)
        self.root.after(200, self.actualizar_cards_doc)

    def actualizar_cards_doc(self):
        if not hasattr(self, 'cards_doc'):
            return
        self.cards_doc["Asistencias"].config(text=str(self.contador["Asistencia"]))
        self.cards_doc["Retardos"].config(text=str(self.contador["Retardo"]))
        self.cards_doc["Faltas"].config(text=str(self.contador["Falta"]))
        self.cards_doc["Justificantes"].config(text=str(self.contador["Justificante"]))

    def panel_docentes(self, parent):
        self.encabezado(parent, "Control Docentes")
        marco = tk.Frame(parent, bg="white")
        marco.pack(fill="both", expand=True, padx=15, pady=10)
        form = tk.Frame(marco, bg="white")
        form.pack(fill="x", padx=10, pady=8)
        form.grid_columnconfigure(1, weight=1)
        form.grid_columnconfigure(3, weight=1)
        tk.Label(form, text="Fecha:", font=F_TXT_B, bg="white").grid(row=0, column=0, sticky="w")
        e_fecha = tk.Entry(form, font=F_TXT, bg="#eef3fa")
        e_fecha.grid(row=0, column=1, sticky="ew", padx=5, ipady=4)
        e_fecha.insert(0, datetime.now().strftime("%d/%m/%Y"))
        tk.Label(form, text="Nombre:", font=F_TXT_B, bg="white").grid(row=0, column=2, sticky="w", padx=(15, 0))
        e_nombre = tk.Entry(form, font=F_TXT, bg="#eef3fa")
        e_nombre.grid(row=0, column=3, sticky="ew", padx=5, ipady=4)
        tk.Label(form, text="Materia:", font=F_TXT_B, bg="white").grid(row=1, column=0, sticky="w", pady=4)
        e_materia = tk.Entry(form, font=F_TXT, bg="#eef3fa")
        e_materia.grid(row=1, column=1, sticky="ew", padx=5, ipady=4)
        tk.Label(form, text="Grupo:", font=F_TXT_B, bg="white").grid(row=1, column=2, sticky="w", padx=(15, 0))
        e_grupo = ttk.Combobox(form, values=["Grupo 1", "Grupo 2", "Grupo 3"], font=F_TXT)
        e_grupo.grid(row=1, column=3, sticky="ew", padx=5, ipady=3)
        e_grupo.current(0)
        cols = ("ID", "Nombre", "Materia", "Grupo")
        tabla = ttk.Treeview(marco, columns=cols, show="headings", height=12)
        for col in cols:
            tabla.heading(col, text=col)
            tabla.column(col, width=130, anchor="center")
        tabla.pack(fill="both", expand=True, padx=10, pady=10)
        def cargar():
            for i in tabla.get_children():
                tabla.delete(i)
            for r in query("SELECT id_docente, nombre, materia, grupo FROM docente", fetch=True):
                tabla.insert("", "end", values=r)
        cargar()
        btns = tk.Frame(marco, bg="white")
        btns.pack(fill="x", padx=10, pady=8)
        def agregar():
            n = e_nombre.get().strip()
            if not n:
                return
            #Maura isabella
            nid = query("SELECT IFNULL(MAX(id_docente),0)+1 FROM docente", fetch=True)[0][0]
            query("INSERT INTO docente (id_docente, nombre, materia, grupo) VALUES (%s,%s,%s,%s)", (nid, n, e_materia.get(), e_grupo.get()))
            cargar()
            e_nombre.delete(0, tk.END)
            e_materia.delete(0, tk.END)
            
        def eliminar():
            sel = tabla.selection()
            if not sel:
                messagebox.showwarning("Selecciona", "Selecciona un docente")
                return
            did = tabla.item(sel[0], "values")[0]
            query("DELETE FROM docente WHERE id_docente=%s", (did,))
            tabla.delete(sel[0])
        tk.Button(btns, text="Agregar Docente", bg=C_BTN2, fg="white", font=F_BTN, command=agregar).pack(side="left", expand=True, fill="x", padx=5, ipady=8)
        tk.Button(btns, text="Eliminar Docente", bg=C_BG2, fg="white", font=F_BTN, command=eliminar).pack(side="left", expand=True, fill="x", padx=5, ipady=8)

    def panel_historial(self, parent):
        self.encabezado(parent, "Historial")
        main = tk.Frame(parent, bg=C_BG)
        main.pack(fill="both", expand=True, padx=15, pady=10)
        cuadro = tk.Frame(main, bg="white", bd=2, relief="solid")
        cuadro.pack(fill="x", pady=(0, 10), ipady=10)
        tk.Label(cuadro, text=" RESUMEN ", font=F_SUB, bg="white", fg=C_BG).pack(anchor="w", padx=15, pady=(10, 5))
        resumen = tk.Frame(cuadro, bg="white")
        resumen.pack(fill="x", padx=15, pady=5)
        for t, col in [("Asistencias", "#0a2a52"), ("Justificantes", "#1e5aa8"), ("Incidencias", "#122e55")]:
            f = tk.Frame(resumen, bg="#eef3fa", bd=1, relief="solid")
            f.pack(side="left", expand=True, fill="x", padx=5, ipady=5)
            tk.Label(f, text=t, font=F_TXT_B, bg="#eef3fa", fg=C_BG).pack()
            tk.Label(f, text="5", font=F_TXT, bg="#eef3fa", fg=col).pack()
        btns = tk.Frame(main, bg=C_BG)
        btns.pack(fill="x", pady=8)
        tabla_frame = tk.Frame(main, bg="white", bd=2, relief="solid")
        tabla_frame.pack(fill="both", expand=True, pady=10)
        tk.Label(tabla_frame, text=" Registros", font=F_SUB, bg="white", fg=C_BG, anchor="w").pack(fill="x", padx=10, pady=8)
        cols = ("Alumno", "Tipo", "Detalle", "Fecha/Hora")
        self.tabla_hist = ttk.Treeview(tabla_frame, columns=cols, show="headings", height=15)
        for col in cols:
            self.tabla_hist.heading(col, text=col)
            self.tabla_hist.column(col, width=140, anchor="center")
        self.tabla_hist.column("Detalle", width=250)
        self.tabla_hist.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        def mostrar(tipo):
            #Ximena 
            for item in self.tabla_hist.get_children():
                self.tabla_hist.delete(item)
            if tipo == "Asistencias":
                for r in query("SELECT detalle, tipo, fecha_hora FROM asistencia", fetch=True):
                    self.tabla_hist.insert("", "end", values=(r[0], r[1], "-", r[2]))
            elif tipo == "Justificantes":
                for r in query("SELECT motivo, imagen, fecha FROM justificante", fetch=True):
                    self.tabla_hist.insert("", "end", values=(r[0], "Justificante", r[1], r[2]))
            else:
                for r in query("SELECT descripcion, tipo, fecha FROM incidencia", fetch=True):
                    self.tabla_hist.insert("", "end", values=(r[0], r[1], "-", r[2]))
            #
        tk.Button(btns, text=" Asistencias", bg="#0a2a52", fg="white", font=F_BTN, relief="flat", padx=20, pady=10, command=lambda: mostrar("Asistencias")).pack(side="left", padx=6)
        tk.Button(btns, text=" Justificantes", bg="#1e5aa8", fg="white", font=F_BTN, relief="flat", padx=20, pady=10, command=lambda: mostrar("Justificantes")).pack(side="left", padx=6)
        tk.Button(btns, text=" Incidencias", bg="#122e55", fg="white", font=F_BTN, relief="flat", padx=20, pady=10, command=lambda: mostrar("Incidencias")).pack(side="left", padx=6)
        mostrar("Asistencias")

    def panel_citatorio(self, parent):
        self.encabezado(parent, "Citatorio")
        marco = tk.Frame(parent, bg="white")
        marco.pack(fill="both", expand=True, padx=15, pady=10)
        form = tk.Frame(marco, bg="#eef3fa", bd=1, relief="solid")
        form.pack(fill="x", padx=10, pady=10)
        form.grid_columnconfigure(1, weight=1)
        form.grid_columnconfigure(3, weight=1)
        tk.Label(form, text="Alumno:", font=F_TXT_B, bg="#eef3fa").grid(row=0, column=0, sticky="w", padx=10, pady=8)
        c_alu = ttk.Combobox(form, values=self.alumnos, font=F_TXT)
        c_alu.grid(row=0, column=1, sticky="ew", padx=5, ipady=4)
        c_alu.current(0)
        tk.Label(form, text="Motivo:", font=F_TXT_B, bg="#eef3fa").grid(row=0, column=2, sticky="w", padx=10, pady=8)
        e_motivo = tk.Entry(form, font=F_TXT, bg="white")
        e_motivo.grid(row=0, column=3, sticky="ew", padx=5, ipady=4)
        tk.Label(form, text="Fecha cita mamá/papá:", font=F_TXT_B, bg="#eef3fa").grid(row=1, column=0, sticky="w", padx=10, pady=8)
        e_fecha = tk.Entry(form, font=F_TXT, bg="white")
        e_fecha.grid(row=1, column=1, sticky="ew", padx=5, ipady=4)
        e_fecha.insert(0, datetime.now().strftime("%d/%m/%Y"))
        tk.Label(form, text="Hora:", font=F_TXT_B, bg="#eef3fa").grid(row=1, column=2, sticky="w", padx=10, pady=8)
        e_hora = ttk.Combobox(form, values=["08:00", "09:00", "10:00", "11:00", "12:00"], font=F_TXT)
        e_hora.grid(row=1, column=3, sticky="ew", padx=5, ipady=3)
        e_hora.current(0)
        tk.Label(form, text="Detalles:", font=F_TXT_B, bg="#eef3fa").grid(row=2, column=0, sticky="nw", padx=10, pady=8)
        txt_obs = tk.Text(form, height=3, font=F_TXT, bg="white")
        txt_obs.grid(row=2, column=1, columnspan=3, sticky="ew", padx=5, pady=8)
        tabla = ttk.Treeview(marco, columns=("Alumno", "Motivo", "Fecha", "Hora"), show="headings", height=10)
        for col in ("Alumno", "Motivo", "Fecha", "Hora"):
            tabla.heading(col, text=col)
            tabla.column(col, width=130, anchor="center")
        tabla.pack(fill="both", expand=True, padx=10, pady=10)
        def cargar():
            #Sahory sherlyn
            for i in tabla.get_children():
                tabla.delete(i)
            for r in query("SELECT detalles, motivo, fecha_cita, hora FROM itinerario", fetch=True):
                tabla.insert("", "end", values=r)
        cargar()
            #
        def agregar():
            if not e_motivo.get().strip():
                messagebox.showwarning("Falta", "Pon motivo")
                return
            #Brandon yael
            nid = query("SELECT IFNULL(MAX(id_itinerario),0)+1 FROM itinerario", fetch=True)[0][0]
            detalles = f"{c_alu.get()} - {txt_obs.get('1.0','end').strip()}"
            query("INSERT INTO itinerario (id_itinerario, motivo, fecha_cita, hora, detalles) VALUES (%s,%s,%s,%s,%s)", (nid, e_motivo.get(), e_fecha.get(), e_hora.get(), detalles))
            cargar()
           #
            e_motivo.delete(0, tk.END)
            txt_obs.delete("1.0", "end")
        tk.Button(marco, text="Crear Citatorio", bg=C_BTN2, fg="white", font=F_BTN, command=agregar).pack(fill="x", padx=10, pady=10, ipady=8)

    def panel_avisos_director(self, parent):
        self.encabezado(parent, "Avisos")
        self.f_crear = tk.Frame(parent, bg="white")
        self.f_crear.pack(fill="both", expand=True, padx=15, pady=10)
        header = tk.Frame(self.f_crear, bg=C_SIDE)
        header.pack(fill="x")
        tk.Label(header, text="  CREAR NUEVO AVISO", font=F_SUB, bg=C_SIDE, fg="white", padx=12, pady=10).pack(side="left")
        form = tk.Frame(self.f_crear, bg="white")
        form.pack(fill="x", padx=12, pady=10)
        form.grid_columnconfigure(1, weight=1)
        tk.Label(form, text="Dirigido a:", font=F_TXT_B, bg="white").grid(row=0, column=0, sticky="w", pady=4)
        self.c_destino = ttk.Combobox(form, values=["Todos los docentes", "Grupo 1", "Grupo 2", "Padres"], font=F_TXT)
        self.c_destino.grid(row=0, column=1, sticky="ew", padx=8, ipady=3)
        self.c_destino.current(0)
        tk.Label(form, text="Asunto:", font=F_TXT_B, bg="white").grid(row=1, column=0, sticky="w", pady=4)
        self.e_asunto = tk.Entry(form, font=F_TXT, bg="#eef3fa")
        self.e_asunto.grid(row=1, column=1, sticky="ew", padx=8, ipady=4)
        tk.Label(form, text="Mensaje:", font=F_TXT_B, bg="white").grid(row=2, column=0, sticky="nw", pady=4)
        self.txt_aviso = tk.Text(form, height=4, font=F_TXT, bg="#eef3fa")
        self.txt_aviso.grid(row=2, column=1, sticky="ew", padx=8, pady=4)
        tabla_frame = tk.Frame(self.f_crear, bg="white", bd=1, relief="solid")
        tabla_frame.pack(fill="both", expand=True, padx=12, pady=10)
        tk.Label(tabla_frame, text="  Historial de avisos", font=F_SUB, bg="white", fg=C_BG, anchor="w").pack(fill="x", padx=10, pady=8)
        cols = ("ID", "Dirigido", "Asunto", "Mensaje", "Fecha")
        self.tabla_avisos = ttk.Treeview(tabla_frame, columns=cols, show="headings", height=10)
        for col in cols:
            self.tabla_avisos.heading(col, text=col)
            self.tabla_avisos.column(col, width=120, anchor="center")
        self.tabla_avisos.column("Mensaje", width=250)
        self.tabla_avisos.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        def cargar():
            for i in self.tabla_avisos.get_children():
                self.tabla_avisos.delete(i)
            for r in query("SELECT id_aviso, destinatario, asunto, mensaje, fecha FROM aviso", fetch=True):
                self.tabla_avisos.insert("", "end", values=r)
        cargar()
        def crear_aviso():
            asunto = self.e_asunto.get().strip()
            msg = self.txt_aviso.get("1.0", "end").strip()
            if not asunto or not msg:
                messagebox.showwarning("Falta", "Pon asunto y mensaje")
                return
            nid = query("SELECT IFNULL(MAX(id_aviso),0)+1 FROM aviso", fetch=True)[0][0]
            query("INSERT INTO aviso (id_aviso, destinatario, asunto, mensaje, fecha) VALUES (%s,%s,%s,%s,%s)", (nid, self.c_destino.get(), asunto, msg, datetime.now().strftime("%d/%m/%Y %H:%M")))
            cargar()
            self.e_asunto.delete(0, tk.END)
            self.txt_aviso.delete("1.0", "end")
        def eliminar_aviso():
            sel = self.tabla_avisos.selection()
            if not sel:
                messagebox.showwarning("Selecciona", "Selecciona un aviso")
                return
            aid = self.tabla_avisos.item(sel[0], "values")[0]
            query("DELETE FROM aviso WHERE id_aviso=%s", (aid,))
            self.tabla_avisos.delete(sel[0])
        btns_aviso = tk.Frame(form, bg="white")
        btns_aviso.grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)
        tk.Button(btns_aviso, text="Publicar Aviso", bg=C_BTN2, fg="white", font=F_BTN, command=crear_aviso).pack(side="left", expand=True, fill="x", padx=(0, 5), ipady=8)
        tk.Button(btns_aviso, text="Eliminar Aviso", bg=C_BG2, fg="white", font=F_BTN, command=eliminar_aviso).pack(side="left", expand=True, fill="x", padx=(5, 0), ipady=8)

    def panel_asistencias(self, parent):
        self.encabezado(parent, "Asistencias")
        marco = tk.Frame(parent, bg="white")
        marco.pack(fill="both", expand=True, padx=15, pady=10)
        top = tk.Frame(marco, bg="#e8eef7")
        top.pack(fill="x", padx=10, pady=10)
        self.lbl_hora = tk.Label(top, text="", font=F_SUB, bg="#e8eef7", fg=C_BG)
        self.lbl_hora.pack(side="left", padx=10, pady=10)
        def actualizar_hora():
            ahora = datetime.now().strftime("%d/%m/%Y %H:%M")
            self.lbl_hora.config(text=f"{self.grupo} | Hora: {ahora}")
            self.root.after(1000, actualizar_hora)
        actualizar_hora()
        cont = tk.Frame(marco, bg="white")
        cont.pack(fill="both", expand=True)
        canvas = tk.Canvas(cont, bg="white", highlightthickness=0)
        sb = ttk.Scrollbar(cont, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg="white")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        for alumno in self.alumnos:
            row = tk.Frame(inner, bg="#f2f6fa", bd=1, relief="solid")
            row.pack(fill="x", pady=8, ipady=14, padx=10)
            tk.Label(row, text=alumno, font=("Segoe UI", 13, "bold"), bg="#f2f6fa", fg=C_BG, width=22, anchor="w").pack(side="left", padx=15)
            lbl = tk.Label(row, text="Sin marcar", font=("Segoe UI", 11), bg="#f2f6fa", fg="gray", width=18)
            lbl.pack(side="left")
            def marcar(a, e, l):
                l.config(text=e, fg=C_SIDE, font=F_TXT_B)
                nid = query("SELECT IFNULL(MAX(id_registro),0)+1 FROM asistencia", fetch=True)[0][0]
                query("INSERT INTO asistencia (id_registro, tipo, fecha_hora, detalle) VALUES (%s,%s,%s,%s)", (nid, e, datetime.now().strftime("%d/%m %H:%M"), f"{a} - {e}"))
                self.contador[e] += 1
                self.actualizar_cards_doc()
            btns = tk.Frame(row, bg="#f2f6fa")
            btns.pack(side="right", padx=15)
            for txt in ["Asistencia", "Retardo", "Falta", "Justificante"]:
                tk.Button(btns, text=txt, bg=C_BTN, fg="white", font=("Segoe UI", 11, "bold"), relief="flat", padx=14, pady=8, command=lambda a=alumno, e=txt, l=lbl: marcar(a, e, l)).pack(side="left", padx=4)
        tk.Button(marco, text="Guardar Asistencias", bg="#1d5aa8", fg="white", font=("Segoe UI", 12, "bold"), command=lambda: messagebox.showinfo("OK", "Asistencias guardadas en la base de datos")).pack(fill="x", padx=10, pady=10, ipady=10)

    def panel_alumnos_pro(self, parent):
        self.encabezado(parent, "Agregar Alumnos")
        marco = tk.Frame(parent, bg="white")
        marco.pack(fill="both", expand=True, padx=15, pady=10)
        form = tk.Frame(marco, bg="#eef3fa", bd=1, relief="solid")
        form.pack(fill="x", padx=10, pady=10)
        form.grid_columnconfigure(1, weight=1)
        form.grid_columnconfigure(3, weight=1)
        tk.Label(form, text="Nombre:", font=F_TXT_B, bg="#eef3fa").grid(row=0, column=0, sticky="w", padx=10, pady=8)
        e_nombre = tk.Entry(form, font=F_TXT, bg="white")
        e_nombre.grid(row=0, column=1, sticky="ew", padx=5, ipady=6)
        tk.Label(form, text="Curp:", font=F_TXT_B, bg="#eef3fa").grid(row=0, column=2, sticky="w", padx=10, pady=8)
        e_mat = tk.Entry(form, font=F_TXT, bg="white")
        e_mat.grid(row=0, column=3, sticky="ew", padx=5, ipady=6)
        tk.Label(form, text="Grupo:", font=F_TXT_B, bg="#eef3fa").grid(row=1, column=0, sticky="w", padx=10, pady=8)
        e_grupo = ttk.Combobox(form, values=["Grupo 1", "Grupo 2", "Grupo 3"], font=F_TXT)
        e_grupo.grid(row=1, column=1, sticky="ew", padx=5, ipady=4)
        e_grupo.current(0)
        tk.Label(form, text="Tutor:", font=F_TXT_B, bg="#eef3fa").grid(row=1, column=2, sticky="w", padx=10, pady=8)
        e_tutor = tk.Entry(form, font=F_TXT, bg="white")
        e_tutor.grid(row=1, column=3, sticky="ew", padx=5, ipady=6)
        tabla = ttk.Treeview(marco, columns=("ID", "Nombre", "Curp", "Grupo", "Tutor"), show="headings", height=12)
        for col in ("ID", "Nombre", "Curp", "Grupo", "Tutor"):
            tabla.heading(col, text=col)
            tabla.column(col, width=140, anchor="center")
        tabla.pack(fill="both", expand=True, padx=10, pady=10)
        def cargar():
            for i in tabla.get_children():
                tabla.delete(i)
            for r in query("SELECT id_alumno, nombre, curp, grupo, tutor FROM alumno", fetch=True):
                tabla.insert("", "end", values=r)
        cargar()
        btns = tk.Frame(marco, bg="white")
        btns.pack(fill="x", padx=10, pady=8)
        def agregar():
            n = e_nombre.get().strip()
            if not n:
                messagebox.showwarning("Falta", "Pon nombre")
                return
            nid = query("SELECT IFNULL(MAX(id_alumno),0)+1 FROM alumno", fetch=True)[0][0]
            query("INSERT INTO alumno (id_alumno, nombre, curp, grupo, tutor) VALUES (%s,%s,%s,%s,%s)", (nid, n, e_mat.get(), e_grupo.get(), e_tutor.get()))
            self.alumnos.append(n)
            cargar()
            e_nombre.delete(0, tk.END)
            e_mat.delete(0, tk.END)
            e_tutor.delete(0, tk.END)
        def baja():
            sel = tabla.selection()
            if not sel:
                messagebox.showwarning("Selecciona", "Selecciona un alumno")
                return
            if messagebox.askyesno("Baja", "¿Dar de baja?"):
                aid = tabla.item(sel[0], "values")[0]
                query("DELETE FROM alumno WHERE id_alumno=%s", (aid,))
                tabla.delete(sel[0])
        tk.Button(btns, text=" Añadir Alumno", bg=C_BTN2, fg="white", font=F_BTN_MENU, command=agregar).pack(side="left", expand=True, fill="x", padx=5, ipady=10)
        tk.Button(btns, text=" Dar de Baja", bg=C_BG2, fg="white", font=F_BTN_MENU, command=baja).pack(side="left", expand=True, fill="x", padx=5, ipady=10)

    def panel_incidencias(self, parent):
        self.encabezado(parent, "Incidencias")
        marco = tk.Frame(parent, bg="white")
        marco.pack(fill="both", expand=True, padx=15, pady=10)
        f1 = tk.Frame(marco, bg="#eef3fa", bd=1, relief="solid")
        f1.pack(fill="x", padx=10, pady=10)
        tk.Label(f1, text="Situación / Descripción:", font=F_TXT_B, bg="#eef3fa", fg=C_BG, anchor="w").pack(fill="x", padx=10, pady=(10, 2))
        c_alu = ttk.Combobox(f1, values=self.alumnos, font=F_TXT, state="readonly")
        c_alu.pack(fill="x", padx=10, pady=5, ipady=4)
        c_alu.current(0)
        var = tk.StringVar(value="Leve")
        fr = tk.Frame(f1, bg="#eef3fa")
        fr.pack(fill="x", padx=10, pady=5)
        tk.Radiobutton(fr, text="Leve", variable=var, value="Leve", bg="#eef3fa").pack(side="left")
        tk.Radiobutton(fr, text="Grave", variable=var, value="Grave", bg="#eef3fa", fg=C_SIDE, font=F_TXT_B).pack(side="left")
        txt = tk.Text(f1, height=3, font=F_TXT, bg="white")
        txt.pack(fill="x", padx=10, pady=8)
        btn_f = tk.Frame(f1, bg="#eef3fa")
        btn_f.pack(fill="x", padx=10, pady=5)
        f2 = tk.Frame(marco, bg="white", bd=1, relief="solid")
        f2.pack(fill="both", expand=True, padx=10, pady=10)
        tk.Label(f2, text="Incidencias", font=F_SUB, bg="white", fg=C_BG, anchor="w").pack(fill="x", padx=10, pady=8)
        cols = ("ID", "Alumno", "Tipo", "Descripción", "Fecha")
        tabla = ttk.Treeview(f2, columns=cols, show="headings", height=8)
        for col in cols:
            tabla.heading(col, text=col)
            tabla.column(col, width=130, anchor="center")
        tabla.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        def cargar():
            for i in tabla.get_children():
                tabla.delete(i)
            for r in query("SELECT id_incidencia, descripcion, tipo, fecha FROM incidencia", fetch=True):
                tabla.insert("", "end", values=(r[0], r[1], r[2], r[1], r[3]))
        cargar()
        def guardar():
            causa = txt.get("1.0", "end").strip()
            if not causa:
                return
            fecha = datetime.now().strftime("%d/%m %H:%M")
            nid = query("SELECT IFNULL(MAX(id_incidencia),0)+1 FROM incidencia", fetch=True)[0][0]
            desc = f"{c_alu.get()} - {causa}"
            query("INSERT INTO incidencia (id_incidencia, tipo, descripcion, fecha) VALUES (%s,%s,%s,%s)", (nid, var.get(), desc, fecha))
            cargar()
            txt.delete("1.0", "end")
        tk.Button(btn_f, text="Enviar Incidencia", bg=C_SIDE, fg="white", font=F_BTN, command=guardar).pack(fill="x", ipady=6)

    def panel_justificante(self, parent):
        self.encabezado(parent, "Justificantes")
        marco = tk.Frame(parent, bg="white")
        marco.pack(fill="both", expand=True, padx=15, pady=10)
        f1 = tk.Frame(marco, bg="#eef3fa", bd=1, relief="solid")
        f1.pack(fill="x", padx=10, pady=10)
        tk.Label(f1, text="Situación / Motivo del justificante:", font=F_TXT_B, bg="#eef3fa", fg=C_BG, anchor="w").pack(fill="x", padx=10, pady=(10, 2))
        c_alu = ttk.Combobox(f1, values=self.alumnos, font=F_TXT)
        c_alu.pack(fill="x", padx=10, pady=5, ipady=4)
        c_alu.current(0)
        txt = tk.Text(f1, height=3, font=F_TXT, bg="white")
        txt.pack(fill="x", padx=10, pady=8)
        self.lbl_ruta = tk.Label(f1, text="Sin imagen", font=("Segoe UI", 9, "italic"), bg="#eef3fa", fg="gray", anchor="w")
        self.lbl_ruta.pack(fill="x", padx=10)
        btns = tk.Frame(f1, bg="#eef3fa")
        btns.pack(fill="x", padx=10, pady=8)
        f2 = tk.Frame(marco, bg="white", bd=1, relief="solid")
        f2.pack(fill="both", expand=True, padx=10, pady=10)
        tk.Label(f2, text=" Justificantes ", font=F_SUB, bg="white", fg=C_BG, anchor="w").pack(fill="x", padx=10, pady=8)
        cols = ("ID", "Alumno", "Motivo", "Imagen", "Fecha")
        tabla = ttk.Treeview(f2, columns=cols, show="headings", height=7)
        for col in cols:
            tabla.heading(col, text=col)
            tabla.column(col, width=120, anchor="center")
        tabla.column("Motivo", width=200)
        tabla.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        def cargar():
            for i in tabla.get_children():
                tabla.delete(i)
            for r in query("SELECT id_justificante, motivo, imagen, fecha FROM justificante", fetch=True):
                tabla.insert("", "end", values=(r[0], r[1], r[1], r[2], r[3]))
        cargar()
        def abrir():
            ruta = filedialog.askopenfilename(filetypes=[("Imagen", "*.jpg *.png *.jpeg")])
            if ruta:
                self.lbl_ruta.config(text=f"Imagen: {ruta}")
        def guardar():
            m = txt.get("1.0", "end").strip()
            if not m:
                return
            fecha = datetime.now().strftime("%d/%m %H:%M")
            img = self.lbl_ruta.cget('text') if "Imagen:" in self.lbl_ruta.cget('text') else "Sin imagen"
            nid = query("SELECT IFNULL(MAX(id_justificante),0)+1 FROM justificante", fetch=True)[0][0]
            query("INSERT INTO justificante (id_justificante, motivo, imagen, fecha) VALUES (%s,%s,%s,%s)", (nid, f"{c_alu.get()} - {m}", img, fecha))
            self.contador["Justificante"] += 1
            cargar()
            txt.delete("1.0", "end")
            self.lbl_ruta.config(text="Sin imagen")
            self.actualizar_cards_doc()
        def eliminar():
            sel = tabla.selection()
            if sel:
                jid = tabla.item(sel[0], "values")[0]
                query("DELETE FROM justificante WHERE id_justificante=%s", (jid,))
                tabla.delete(sel[0])
        tk.Button(btns, text=" Agregar Imagen", bg=C_BTN2, fg="white", font=F_BTN, command=abrir).pack(side="left", expand=True, fill="x", padx=3, ipady=6)
        tk.Button(btns, text=" Guardar", bg=C_SIDE, fg="white", font=F_BTN, command=guardar).pack(side="left", expand=True, fill="x", padx=3, ipady=6)
        tk.Button(marco, text="Eliminar Seleccionado", bg=C_BG2, fg="white", font=F_BTN, command=eliminar).pack(fill="x", padx=10, pady=8, ipady=5)

if __name__ == "__main__":
    root = tk.Tk()
    Login(root)
    root.mainloop()
