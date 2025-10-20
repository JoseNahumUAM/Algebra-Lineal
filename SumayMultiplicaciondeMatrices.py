#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SumayMultiplicaciondeMatrices.py — Operaciones con matrices (Sumar, A×B, A·v)
UI UAM:
- Tabs: Sumar | Multiplicar A×B | A·v
- Controles: Dimensiones, Fracciones exactas, Generar, Ejemplo, Limpiar
- Resolver (muestra al instante) + Regresar a la derecha (sin botón de pasos)
"""

from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox
from fractions import Fraction
from typing import List, Union

Number = Union[Fraction, float]
UI_SCALE = 1.25

# --------------------------- utilidades numéricas ---------------------------

def _fmt(x: Number, dec: int = 6) -> str:
    if isinstance(x, Fraction):
        return str(x) if x.denominator != 1 else str(x.numerator)
    s = f"{float(x):.{dec}f}"
    return s.rstrip("0").rstrip(".") if "." in s else s

def _zero(use_frac: bool) -> Number:
    return Fraction(0, 1) if use_frac else 0.0

def suma_matrices(A: List[List[Number]], B: List[List[Number]]) -> List[List[Number]]:
    m, n = len(A), len(A[0])
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(m)]

def mult_matrices(A: List[List[Number]], B: List[List[Number]]) -> List[List[Number]]:
    m, k, n = len(A), len(A[0]), len(B[0])
    use_frac = isinstance(A[0][0], Fraction) or isinstance(B[0][0], Fraction)
    C = []
    for i in range(m):
        row = []
        for j in range(n):
            s = _zero(use_frac)
            for t in range(k):
                s = s + A[i][t] * B[t][j]
            row.append(s)
        C.append(row)
    return C

def mult_matriz_vector(A: List[List[Number]], v: List[Number]) -> List[List[Number]]:
    m, n = len(A), len(A[0])
    use_frac = isinstance(A[0][0], Fraction) or isinstance(v[0], Fraction)
    out = [[_zero(use_frac)] for _ in range(m)]
    for i in range(m):
        s = _zero(use_frac)
        for j in range(n):
            s = s + A[i][j] * v[j]
        out[i][0] = s
    return out

# --------------------------- UI: vista principal ----------------------------

class OpsView(ttk.Frame):
    def __init__(self, parent, on_back=None):
        super().__init__(parent)
        self.on_back = on_back
        try: self.tk.call("tk", "scaling", UI_SCALE)
        except tk.TclError: pass

        # paleta
        self.bg = "#eef4ff"; self.card = "#ffffff"
        self.primary = "#1f4fd6"; self.text = "#0f172a"; self.muted = "#475569"

        self._styles()
        self._state()
        self._build()

    # ----------------------- estilos -----------------------
    def _styles(self):
        s = ttk.Style(self)
        try: s.theme_use("clam")
        except tk.TclError: pass

        self.configure(style="Root.TFrame")
        s.configure("Root.TFrame", background=self.bg)
        s.configure("Card.TFrame", background=self.card)
        s.configure("HdrTitle.TLabel", font=("Segoe UI", 24, "bold"),
                   background=self.card, foreground=self.text)
        s.configure("HdrSub.TLabel", font=("Segoe UI", 11),
                   background=self.card, foreground=self.muted)
        s.configure("Sec.TLabel", font=("Segoe UI", 11, "bold"),
                   background=self.card, foreground=self.text)

        s.configure("Primary.TButton", font=("Segoe UI", 12, "bold"), padding=10)
        s.map("Primary.TButton",
              background=[("!disabled", self.primary), ("active", "#1a43b5")],
              foreground=[("!disabled", "white")])

        s.configure("Ghost.TButton", font=("Segoe UI", 11), padding=10)
        s.map("Ghost.TButton",
              background=[("!disabled", self.card), ("active", "#eef2ff")])

        s.configure("Tab.TButton", font=("Segoe UI", 11, "bold"), padding=8)

    # ----------------------- estado ------------------------
    def _state(self):
        self.tab = tk.IntVar(value=0)
        self.use_frac = tk.BooleanVar(value=True)

        self.m_sum = tk.IntVar(value=2); self.n_sum = tk.IntVar(value=2)
        self.m_ab  = tk.IntVar(value=2); self.k_ab = tk.IntVar(value=2); self.n_ab = tk.IntVar(value=2)
        self.m_av  = tk.IntVar(value=3); self.n_av = tk.IntVar(value=2)

        self.gridA: List[List[tk.Entry]] = []
        self.gridB: List[List[tk.Entry]] = []
        self.gridV: List[tk.Entry] = []
        self.gridR: ttk.Treeview | None = None

    # ----------------------- construcción UI ------------------------
    def _build(self):
        root = tk.Frame(self, bg=self.bg); root.pack(fill="both", expand=True, padx=24, pady=24)

        # Header
        hshadow = tk.Frame(root, bg="#dfe7fb"); hshadow.pack(fill="x", pady=(0,14))
        header = ttk.Frame(hshadow, style="Card.TFrame", padding=16); header.pack(fill="x", padx=1, pady=1)
        ttk.Label(header, text="Suma y Multiplicación de Matrices", style="HdrTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(header, text="Defina dimensiones, ingrese los valores y presione Resolver. El resultado y el registro se muestran de inmediato.",
                  style="HdrSub.TLabel").grid(row=1, column=0, sticky="w")

        # Tabs
        tabs_shadow = tk.Frame(root, bg="#dfe7fb"); tabs_shadow.pack(fill="x")
        tabs = ttk.Frame(tabs_shadow, style="Card.TFrame", padding=8); tabs.pack(fill="x", padx=1, pady=1)
        self.btn_sum = ttk.Button(tabs, text="Sumar", style="Tab.TButton",
                                  command=lambda: self._switch_tab(0))
        self.btn_axb = ttk.Button(tabs, text="Multiplicar A×B", style="Tab.TButton",
                                  command=lambda: self._switch_tab(1))
        self.btn_av  = ttk.Button(tabs, text="A · v", style="Tab.TButton",
                                  command=lambda: self._switch_tab(2))
        self.btn_sum.grid(row=0, column=0, padx=(0, 6))
        self.btn_axb.grid(row=0, column=1, padx=6)
        self.btn_av.grid(row=0, column=2, padx=6)

        # Controles superiores (dimensiones + fracciones + botones)
        ctrl_shadow = tk.Frame(root, bg="#dfe7fb"); ctrl_shadow.pack(fill="x", pady=(10,0))
        self.ctrl = ttk.Frame(ctrl_shadow, style="Card.TFrame", padding=12); self.ctrl.pack(fill="x", padx=1, pady=1)

        # Cuerpo
        body_shadow = tk.Frame(root, bg="#dfe7fb"); body_shadow.pack(fill="both", expand=True, pady=(12,0))
        self.body = ttk.Frame(body_shadow, style="Card.TFrame", padding=16); self.body.pack(fill="both", expand=True, padx=1, pady=1)

        # panel derecho (registro)
        self.right = ttk.Frame(self.body, style="Card.TFrame"); self.right.pack(side="right", fill="both", expand=True, padx=(8,0))
        ttk.Label(self.right, text="Registro", style="Sec.TLabel").pack(anchor="w")
        self.txt_log = tk.Text(self.right, height=22, wrap="word", relief="flat", bg="white")
        vbar = ttk.Scrollbar(self.right, orient="vertical", command=self.txt_log.yview)
        self.txt_log.configure(yscrollcommand=vbar.set)
        self.txt_log.pack(side="left", fill="both", expand=True, pady=(6,0))
        vbar.pack(side="right", fill="y")

        # panel izquierdo (entradas + resultado)
        self.left = ttk.Frame(self.body, style="Card.TFrame"); self.left.pack(side="left", fill="both", expand=True, padx=(0,8))

        # primera renderización
        self._switch_tab(0)

    # ----------------------- controles por pestaña ------------------------
    def _render_controls_for_tab(self, t: int):
        for w in self.ctrl.winfo_children(): w.destroy()

        frac_cb = ttk.Checkbutton(self.ctrl, text="Usar fracciones exactas", variable=self.use_frac)

        if t == 0:
            ttk.Label(self.ctrl, text="Dimensiones:", style="Sec.TLabel").grid(row=0, column=0, padx=(0,8))
            ttk.Spinbox(self.ctrl, from_=1, to=12, width=4, textvariable=self.m_sum,
                        command=self._generate).grid(row=0, column=1)
            ttk.Label(self.ctrl, text="×", style="Sec.TLabel").grid(row=0, column=2, padx=6)
            ttk.Spinbox(self.ctrl, from_=1, to=12, width=4, textvariable=self.n_sum,
                        command=self._generate).grid(row=0, column=3)
            frac_cb.grid(row=0, column=4, padx=(16,10))
        elif t == 1:
            ttk.Label(self.ctrl, text="A (m×k):", style="Sec.TLabel").grid(row=0, column=0, padx=(0,8))
            ttk.Spinbox(self.ctrl, from_=1, to=12, width=4, textvariable=self.m_ab,
                        command=self._generate).grid(row=0, column=1)
            ttk.Label(self.ctrl, text="×", style="Sec.TLabel").grid(row=0, column=2, padx=6)
            ttk.Spinbox(self.ctrl, from_=1, to=12, width=4, textvariable=self.k_ab,
                        command=self._generate).grid(row=0, column=3)

            ttk.Label(self.ctrl, text="B (k×n):", style="Sec.TLabel").grid(row=0, column=4, padx=(16,8))
            ttk.Spinbox(self.ctrl, from_=1, to=12, width=4, textvariable=self.k_ab,
                        command=self._generate).grid(row=0, column=5)
            ttk.Label(self.ctrl, text="×", style="Sec.TLabel").grid(row=0, column=6, padx=6)
            ttk.Spinbox(self.ctrl, from_=1, to=12, width=4, textvariable=self.n_ab,
                        command=self._generate).grid(row=0, column=7)
            frac_cb.grid(row=0, column=8, padx=(16,10))
        else:
            ttk.Label(self.ctrl, text="A (m×n):", style="Sec.TLabel").grid(row=0, column=0, padx=(0,8))
            ttk.Spinbox(self.ctrl, from_=1, to=12, width=4, textvariable=self.m_av,
                        command=self._generate).grid(row=0, column=1)
            ttk.Label(self.ctrl, text="×", style="Sec.TLabel").grid(row=0, column=2, padx=6)
            ttk.Spinbox(self.ctrl, from_=1, to=12, width=4, textvariable=self.n_av,
                        command=self._generate).grid(row=0, column=3)
            frac_cb.grid(row=0, column=4, padx=(16,10))

        # Botones solicitados (a la derecha)
        ttk.Button(self.ctrl, text="Generar", style="Ghost.TButton",
                   command=self._generate).grid(row=0, column=9, padx=4)
        ttk.Button(self.ctrl, text="Ejemplo", style="Ghost.TButton",
                   command=self._example).grid(row=0, column=10, padx=4)
        ttk.Button(self.ctrl, text="Limpiar", style="Ghost.TButton",
                   command=self._clear_all).grid(row=0, column=11, padx=4)

    def _render_left_for_tab(self, t: int):
        for w in self.left.winfo_children(): w.destroy()
        self.gridA, self.gridB, self.gridV = [], [], []
        self.gridR = None

        # etiquetas
        if t == 0:
            labA, labB, labR = "Matriz A", "Matriz B", "Resultado"
            rows, cols = self.m_sum.get(), self.n_sum.get()
            a_frame = ttk.Frame(self.left, style="Card.TFrame"); a_frame.grid(row=1, column=0, sticky="nw")
            b_frame = ttk.Frame(self.left, style="Card.TFrame"); b_frame.grid(row=1, column=1, sticky="nw", padx=(24,0))
            r_frame = ttk.Frame(self.left, style="Card.TFrame"); r_frame.grid(row=1, column=2, sticky="nw", padx=(24,0))
            ttk.Label(self.left, text=labA, style="Sec.TLabel").grid(row=0, column=0, sticky="w")
            ttk.Label(self.left, text=labB, style="Sec.TLabel").grid(row=0, column=1, sticky="w", padx=(24,0))
            ttk.Label(self.left, text=labR, style="Sec.TLabel").grid(row=0, column=2, sticky="w", padx=(24,0))

            self.gridA = self._build_grid(a_frame, rows, cols)
            self.gridB = self._build_grid(b_frame, rows, cols)
            self.gridR = self._build_table(r_frame, rows, cols)

            # acciones
            ttk.Button(self.left, text="Resolver", style="Primary.TButton",
                       command=self._solve).grid(row=2, column=0, pady=(12,0), sticky="w")
            ttk.Button(self.left, text="Regresar", style="Ghost.TButton",
                       command=self._back).grid(row=2, column=1, pady=(12,0), padx=(12,0), sticky="w")

        elif t == 1:
            labA, labB, labR = "Matriz A (m×k)", "Matriz B (k×n)", "Resultado"
            m, k, n = self.m_ab.get(), self.k_ab.get(), self.n_ab.get()
            a_frame = ttk.Frame(self.left, style="Card.TFrame"); a_frame.grid(row=1, column=0, sticky="nw")
            b_frame = ttk.Frame(self.left, style="Card.TFrame"); b_frame.grid(row=1, column=1, sticky="nw", padx=(24,0))
            r_frame = ttk.Frame(self.left, style="Card.TFrame"); r_frame.grid(row=1, column=2, sticky="nw", padx=(24,0))
            ttk.Label(self.left, text=labA, style="Sec.TLabel").grid(row=0, column=0, sticky="w")
            ttk.Label(self.left, text=labB, style="Sec.TLabel").grid(row=0, column=1, sticky="w", padx=(24,0))
            ttk.Label(self.left, text=labR, style="Sec.TLabel").grid(row=0, column=2, sticky="w", padx=(24,0))

            self.gridA = self._build_grid(a_frame, m, k)
            self.gridB = self._build_grid(b_frame, k, n)
            self.gridR = self._build_table(r_frame, m, n)

            ttk.Button(self.left, text="Resolver", style="Primary.TButton",
                       command=self._solve).grid(row=2, column=0, pady=(12,0), sticky="w")
            ttk.Button(self.left, text="Regresar", style="Ghost.TButton",
                       command=self._back).grid(row=2, column=1, pady=(12,0), padx=(12,0), sticky="w")

        else:
            labA, labV, labR = "Matriz A (m×n)", "Vector v (n×1)", "Resultado (m×1)"
            m, n = self.m_av.get(), self.n_av.get()
            a_frame = ttk.Frame(self.left, style="Card.TFrame"); a_frame.grid(row=1, column=0, sticky="nw")
            v_frame = ttk.Frame(self.left, style="Card.TFrame"); v_frame.grid(row=1, column=1, sticky="nw", padx=(24,0))
            r_frame = ttk.Frame(self.left, style="Card.TFrame"); r_frame.grid(row=1, column=2, sticky="nw", padx=(24,0))
            ttk.Label(self.left, text=labA, style="Sec.TLabel").grid(row=0, column=0, sticky="w")
            ttk.Label(self.left, text=labV, style="Sec.TLabel").grid(row=0, column=1, sticky="w", padx=(24,0))
            ttk.Label(self.left, text=labR, style="Sec.TLabel").grid(row=0, column=2, sticky="w", padx=(24,0))

            self.gridA = self._build_grid(a_frame, m, n)
            self.gridV = self._build_vector(v_frame, n)
            self.gridR = self._build_table(r_frame, m, 1)

            ttk.Button(self.left, text="Resolver", style="Primary.TButton",
                       command=self._solve).grid(row=2, column=0, pady=(12,0), sticky="w")
            ttk.Button(self.left, text="Regresar", style="Ghost.TButton",
                       command=self._back).grid(row=2, column=1, pady=(12,0), padx=(12,0), sticky="w")

    # ----------------------- helpers de UI -------------------------
    def _build_grid(self, parent, rows: int, cols: int) -> List[List[tk.Entry]]:
        grid = []
        for i in range(rows):
            row = []
            for j in range(cols):
                e = tk.Entry(parent, width=7, justify="center", font=("Consolas", 11))
                e.grid(row=i, column=j, padx=4, pady=4)
                e.insert(0, "0")
                row.append(e)
            grid.append(row)
        return grid

    def _build_vector(self, parent, n: int) -> List[tk.Entry]:
        vec = []
        for i in range(n):
            e = tk.Entry(parent, width=7, justify="center", font=("Consolas", 11))
            e.grid(row=i, column=0, padx=4, pady=4)
            e.insert(0, "0")
            vec.append(e)
        return vec

    def _build_table(self, parent, rows: int, cols: int) -> ttk.Treeview:
        tv = ttk.Treeview(parent, show="headings", height=max(6, rows))
        tv["columns"] = [f"c{k}" for k in range(cols)]
        for k in range(cols):
            tv.heading(f"c{k}", text=f"c{k+1}")
            tv.column(f"c{k}", width=80, anchor="center")
        tv.grid(row=0, column=0, sticky="nsew", pady=(4,0))
        return tv

    def _read_matrix(self, grid: List[List[tk.Entry]]) -> List[List[Number]]:
        use_frac = self.use_frac.get()
        M = []
        for i, row in enumerate(grid):
            vals = []
            for j, e in enumerate(row):
                t = e.get().strip()
                if not t: raise ValueError(f"Celda vacía en ({i+1},{j+1})")
                vals.append(Fraction(t) if use_frac else float(t))
            M.append(vals)
        return M

    def _read_vector(self, grid: List[tk.Entry]) -> List[Number]:
        use_frac = self.use_frac.get()
        v = []
        for i, e in enumerate(grid):
            t = e.get().strip()
            if not t: raise ValueError(f"Celda vacía en v[{i+1}]")
            v.append(Fraction(t) if use_frac else float(t))
        return v

    def _set_table(self, tv: ttk.Treeview, M: List[List[Number]]):
        for iid in tv.get_children(): tv.delete(iid)
        if not M: return
        cols = len(M[0])
        if len(tv["columns"]) != cols:
            tv["columns"] = [f"c{k}" for k in range(cols)]
            for k in range(cols):
                tv.heading(f"c{k}", text=f"c{k+1}")
                tv.column(f"c{k}", width=80, anchor="center")
        for row in M:
            tv.insert("", "end", values=[_fmt(x) for x in row])

    def _log(self, text: str, clear=False):
        self.txt_log.configure(state="normal")
        if clear: self.txt_log.delete("1.0","end")
        self.txt_log.insert("end", text + ("\n" if not text.endswith("\n") else ""))
        self.txt_log.configure(state="disabled")
        self.txt_log.see("end")

    # ----------------------- acciones ---------------------------
    def _switch_tab(self, t: int):
        self.tab.set(t)
        self._render_controls_for_tab(t)
        # reconstruir panel izquierdo
        for w in self.left.winfo_children(): w.destroy()
        self._render_left_for_tab(t)
        for b in (self.btn_sum, self.btn_axb, self.btn_av): b.state(["!disabled"])
        (self.btn_sum if t==0 else self.btn_axb if t==1 else self.btn_av).state(["disabled"])
        self._log("Listo para operar.\n", clear=True)

    def _generate(self):
        """Reconstruye grillas según dimensiones actuales."""
        self._render_controls_for_tab(self.tab.get())
        self._render_left_for_tab(self.tab.get())
        self._log("Generado con nuevas dimensiones.\n", clear=True)

    def _example(self):
        """Carga un ejemplo simple por pestaña (ajusta dimensiones y rellena)."""
        t = self.tab.get()
        if t == 0:
            self.m_sum.set(2); self.n_sum.set(2)
            self._generate()
            A = [[1,2],[3,4]]
            B = [[5,6],[7,8]]
            for i in range(2):
                for j in range(2):
                    self.gridA[i][j].delete(0,"end"); self.gridA[i][j].insert(0,str(A[i][j]))
                    self.gridB[i][j].delete(0,"end"); self.gridB[i][j].insert(0,str(B[i][j]))
            self._log("Ejemplo cargado: Suma 2×2.", clear=True)
        elif t == 1:
            self.m_ab.set(2); self.k_ab.set(3); self.n_ab.set(2)
            self._generate()
            A = [[1,0,2],[-1,3,1]]
            B = [[3,1],[2,1],[1,0]]
            for i in range(2):
                for j in range(3):
                    self.gridA[i][j].delete(0,"end"); self.gridA[i][j].insert(0,str(A[i][j]))
            for i in range(3):
                for j in range(2):
                    self.gridB[i][j].delete(0,"end"); self.gridB[i][j].insert(0,str(B[i][j]))
            self._log("Ejemplo cargado: A(2×3) × B(3×2).", clear=True)
        else:
            self.m_av.set(3); self.n_av.set(2)
            self._generate()
            A = [[1,2],[0,3],[1,-1]]
            v = [2,1]
            for i in range(3):
                for j in range(2):
                    self.gridA[i][j].delete(0,"end"); self.gridA[i][j].insert(0,str(A[i][j]))
            for j in range(2):
                self.gridV[j].delete(0,"end"); self.gridV[j].insert(0,str(v[j]))
            self._log("Ejemplo cargado: A(3×2) · v(2×1).", clear=True)

    def _clear_all(self):
        """Pone todos los campos a 0 y limpia resultado/registro."""
        for grid in (self.gridA, self.gridB):
            for row in grid:
                for e in row:
                    e.delete(0,"end"); e.insert(0,"0")
        for e in self.gridV:
            e.delete(0,"end"); e.insert(0,"0")
        if self.gridR:
            for iid in self.gridR.get_children(): self.gridR.delete(iid)
        self._log("Formulario limpio.\n", clear=True)

    def _solve(self):
        try:
            t = self.tab.get()
            if t == 0:
                A = self._read_matrix(self.gridA)
                B = self._read_matrix(self.gridB)
                if len(A)!=len(B) or len(A[0])!=len(B[0]):
                    raise ValueError("Para sumar, A y B deben tener la misma dimensión.")
                C = suma_matrices(A,B)
                self._set_table(self.gridR, C)
                self._log("Sumando matrices A + B …", clear=True)
                self._log("Resultado (A + B):")
                for r in C: self._log("[ " + "  ".join(_fmt(x) for x in r) + " ]")
            elif t == 1:
                A = self._read_matrix(self.gridA)
                B = self._read_matrix(self.gridB)
                if len(A[0]) != len(B):
                    raise ValueError("Para A×B, columnas de A = filas de B.")
                C = mult_matrices(A,B)
                self._set_table(self.gridR, C)
                self._log("Multiplicando matrices A × B …", clear=True)
                self._log("Resultado (A × B):")
                for r in C: self._log("[ " + "  ".join(_fmt(x) for x in r) + " ]")
            else:
                A = self._read_matrix(self.gridA)
                v = self._read_vector(self.gridV)
                if len(A[0]) != len(v):
                    raise ValueError("Para A·v, largo(v) = n (columnas de A).")
                C = mult_matriz_vector(A, v)
                self._set_table(self.gridR, C)
                self._log("Multiplicando matriz por vector A · v …", clear=True)
                self._log("Resultado (A · v):")
                for r in C: self._log("[ " + "  ".join(_fmt(x) for x in r) + " ]")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _back(self):
        if callable(self.on_back): self.on_back()

# --------------------------- API pública ----------------------------

def mount_ops(parent, on_back=None):
    parent.winfo_toplevel().title("UAM — Suma y Multiplicación de Matrices")
    view = OpsView(parent, on_back=on_back)
    view.pack(fill="both", expand=True)
    return view

if __name__ == "__main__":
    root = tk.Tk()
    try: root.state("zoomed")
    except Exception: pass
    mount_ops(root, on_back=root.destroy)
    root.mainloop()
