#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculadora.py — Hub (tarjetas) integrado y responsivo.
Integra GAUSS con vista propia (Gauss.mount_gauss).
"""

import os
import tkinter as tk
from tkinter import ttk

from Gauss import mount_gauss   # <<<<< import desde Gauss.py
from GaussJordan import mount_gauss_jordan # <<<<< import desde GaussJordan.py
from MatrizInversa import mount_inversa    # <<<<< import desde GaussJordan.py
from SumayMultiplicaciondeMatrices import mount_ops
from VectorValidacion import mount_vector_validacion



LOGO_PATH = "logo_uam.png"      # PNG para logo en header / fallback de icono
ICON_PATH = "uam.ico"           # ICO recomendado para Windows (opcional)
UI_SCALE = 1.25

CARDS = [
    ("Determinantes",          "[ 4  7 ]\n[ 2  2 ]\n[ 1  6 ]",            "Determinantes.py"),
    ("Gauss",                  "[ 1  2 -1 | 3 ]\n[ 0  3  2 | 9 ]\n[ 0  0 -1 | 8 ]", "Gauss.py"),
    ("Gauss-Jordan",           "[ 1 0 0 | 2 ]\n[ 0 1 2 | 1 ]\n[ 0 0 1 | 0 ]",     "GaussJordan.py"),
    ("Matriz Inversa",         "[ a  b  c  d ]\n[ e  f  g  h ]\n[ i  j  k  l ]", "MatrizInversa.py"),
    ("Suma y Multiplicación",  "[ 1 3 2 ]  [ 5 6 ]\n[ 2 4 4 ]×[ 7 8 ]",         "SumayMultiplicacio.py"),
    ("Vector Validación",      "[ 1 ]\n[ 0 ]\n[ 0 ]\n[ 1 ]",                      "VectorValidacion.py"),
]

def load_logo(path, target=(80, 80)):
    if not os.path.exists(path):
        return None
    try:
        from PIL import Image, ImageTk  # type: ignore
        img = Image.open(path).convert("RGBA")
        img.thumbnail(target, Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception:
        try:
            img = tk.PhotoImage(file=path)
            w, h = img.width(), img.height()
            fx = max(1, w // max(1, target[0]))
            fy = max(1, h // max(1, target[1]))
            if fx > 1 or fy > 1:
                img = img.subsample(fx, fy)
            return img
        except Exception:
            return None

class HubFrame(ttk.Frame):
    def __init__(self, parent, on_back=None):
        super().__init__(parent)
        self.on_back = on_back
        try:
            self.tk.call("tk", "scaling", UI_SCALE)
        except tk.TclError:
            pass

        self._build_styles()
        self._build_ui()

    def _build_styles(self):
        s = ttk.Style(self)
        try: s.theme_use("clam")
        except tk.TclError: pass

        self.bg = "#eef4ff"; self.card = "#ffffff"; self.stroke = "#dbe3f7"
        self.primary = "#1f4fd6"; self.text = "#0f172a"; self.muted = "#475569"

        self.configure(style="Root.TFrame")
        s.configure("Root.TFrame", background=self.bg)
        s.configure("Card.TFrame", background=self.card)
        s.configure("Header.TFrame", background=self.card)
        s.configure("HdrTitle.TLabel", font=("Segoe UI", 30, "bold"), background=self.card, foreground=self.text)
        s.configure("HdrSub.TLabel", font=("Segoe UI", 13), background=self.card, foreground=self.muted)
        s.configure("CardTitle.TLabel", font=("Segoe UI", 15, "bold"), background=self.card, foreground=self.text)
        s.configure("CardMatrix.TLabel", font=("Consolas", 12), background=self.card, foreground="#111827")
        s.configure("Ghost.TButton", font=("Segoe UI", 12), padding=10)
        s.map("Ghost.TButton", background=[("!disabled", self.card), ("active", "#eef2ff")])
        s.configure("CardBtn.TButton", font=("Segoe UI", 12), padding=10)
        s.map("CardBtn.TButton", background=[("!disabled", self.card), ("active", "#eef2ff")])

    def _build_ui(self):
        container = tk.Frame(self, bg=self.bg)
        container.pack(fill="both", expand=True, padx=30, pady=30)

        header_shadow = tk.Frame(container, bg="#dfe7fb")
        header_shadow.pack(fill="x", pady=(0, 16))
        header = ttk.Frame(header_shadow, style="Card.TFrame", padding=24)
        header.pack(fill="x", padx=1, pady=1)

        header.columnconfigure(1, weight=1)
        self._logo = load_logo(LOGO_PATH, target=(86, 86))
        if self._logo:
            logo = ttk.Label(header, image=self._logo, background=self.card)
        else:
            canvas = tk.Canvas(header, width=86, height=86, bg=self.card, highlightthickness=0)
            canvas.create_oval(6, 6, 80, 80, outline="#93c5fd", width=2)
            canvas.create_text(43, 43, text="UAM", fill=self.primary, font=("Segoe UI", 13, "bold"))
            logo = canvas
        logo.grid(row=0, column=0, rowspan=2, padx=(0, 16))

        ttk.Label(header, text="CALCULADORA DE MATRICES", style="HdrTitle.TLabel").grid(row=0, column=1, sticky="w")
        ttk.Label(header, text="Universidad Americana — seleccione una operación (ventana integrada)",
                  style="HdrSub.TLabel").grid(row=1, column=1, sticky="w")

        grid_shadow = tk.Frame(container, bg="#dfe7fb")
        grid_shadow.pack(fill="both", expand=True)
        grid_card = ttk.Frame(grid_shadow, style="Card.TFrame", padding=18)
        grid_card.pack(fill="both", expand=True, padx=1, pady=1)

        grid = ttk.Frame(grid_card, style="Card.TFrame")
        grid.pack(fill="both", expand=True)
        for col in range(3):
            grid.columnconfigure(col, weight=1, uniform="cols")

        for idx, (title, ascii_matrix, _file) in enumerate(CARDS):
            r, c = divmod(idx, 3)
            cell_shadow = tk.Frame(grid, bg=self.stroke)
            cell_shadow.grid(row=r, column=c, padx=12, pady=12, sticky="nsew")
            cell = ttk.Frame(cell_shadow, style="Card.TFrame", padding=16)
            cell.pack(fill="both", expand=True, padx=1, pady=1)

            ttk.Label(cell, text=title, style="CardTitle.TLabel").pack(pady=(4, 8))
            ttk.Label(cell, text=ascii_matrix, style="CardMatrix.TLabel", justify="center").pack(pady=(0, 10))

            if title == "Gauss":
                ttk.Button(cell, text="Abrir", style="CardBtn.TButton",
                           command=self._open_gauss).pack()
            elif title == "Gauss-Jordan":
                ttk.Button(cell, text="Abrir", style="CardBtn.TButton",
               command=self._open_gj).pack()   # ← usa _open_gj
            elif title == "Matriz Inversa":
                ttk.Button(cell, text="Abrir", style="CardBtn.TButton",
               command=self._open_inversa).pack()
            elif title == "Suma y Multiplicación":
                ttk.Button(cell, text="Abrir", style="CardBtn.TButton",
               command=self._open_ops).pack()
            elif title == "Vector Validación":
                ttk.Button(cell, text="Abrir", style="CardBtn.TButton",
               command=self._open_vector).pack()


            else:
                ttk.Button(cell, text="Abrir (próximamente)", style="CardBtn.TButton").pack()

        footer = ttk.Frame(container, style="Card.TFrame")
        footer.pack(fill="x", pady=(16, 0))
        ttk.Button(footer, text="Regresar", style="Ghost.TButton",
                   command=self._back).pack(side="right")   # ← texto actualizado

    # --- navegación ---
    def _back(self):
        if callable(self.on_back):
            self.on_back()

    def _open_gauss(self):
        parent = self.master
        for w in parent.winfo_children():
            w.destroy()
        mount_gauss(parent, on_back=self._back_to_hub)
    def _open_inversa(self):
        parent = self.master
        for w in parent.winfo_children():
            w.destroy()
        mount_inversa(parent, on_back=self._back_to_hub)

    def _open_gj(self):
        parent = self.master            # contenedor raíz donde está montado el hub
        for w in parent.winfo_children():
            w.destroy()                 # limpia la ventana
        # monta la vista de Gauss-Jordan en la MISMA ventana
        mount_gauss_jordan(parent, on_back=self._back_to_hub)

    def _back_to_hub(self):
        parent = self.master
        for w in parent.winfo_children():
            w.destroy()
        HubFrame(parent, on_back=self.on_back).pack(fill="both", expand=True)
    def _open_ops(self):
        parent = self.master
        for w in parent.winfo_children(): w.destroy()
        mount_ops(parent, on_back=self._back_to_hub)
    def _open_vector(self):
        parent = self.master
        for w in parent.winfo_children(): w.destroy()
        mount_vector_validacion(parent, on_back=self._back_to_hub)



# ---------- API pública ----------
def mount(parent, on_back=None):
    # Asegura el título cuando se monta el hub
    parent.winfo_toplevel().title("UAM — Calculadora de Matrices")
    hub = HubFrame(parent, on_back=on_back)
    hub.pack(fill="both", expand=True)
    return hub

if __name__ == "__main__":
    root = tk.Tk()

    # Título e icono de la app
    root.title("UAM — Calculadora de Matrices")
    try:
        if os.path.exists(ICON_PATH):
            root.iconbitmap(ICON_PATH)  # .ico (Windows)
    except Exception:
        pass
    # Fallback PNG (mantener referencia para que no se libere)
    try:
        from PIL import Image, ImageTk  # type: ignore
        _icon_png = ImageTk.PhotoImage(file=LOGO_PATH)
        root.iconphoto(True, _icon_png)
        root._icon_ref = _icon_png
    except Exception:
        try:
            _icon_png = tk.PhotoImage(file=LOGO_PATH)
            root.iconphoto(True, _icon_png)
            root._icon_ref = _icon_png
        except Exception:
            pass

    root.state("zoomed")
    mount(root, on_back=root.destroy)
    root.mainloop()