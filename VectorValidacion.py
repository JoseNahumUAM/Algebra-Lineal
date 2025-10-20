#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
VectorValidacion.py — Verificador de independencia lineal (Gauss con pasos)
Coherente con el estilo de tus otras vistas:
- Controles: dimensión n, cantidad de vectores p
- Botones: Generar | Ejemplo | Limpiar
- Acción: Resolver | Regresar
- Izquierda: entradas (vectores por columnas) y RREF (tabla centrada)
- Derecha: registro (paso a paso) con scroll único
"""

from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List

Number = float | int
UI_SCALE = 1.25


# --------------------- utilidades numéricas ---------------------
def _fmt(x: Number) -> str:
    if isinstance(x, float) and abs(x - round(x)) < 1e-12:
        x = int(round(x))
    return str(x)

def _imprimir_matriz_txt(M: List[List[Number]]) -> str:
    lines = []
    for fila in M:
        s = "  [ "
        for j, v in enumerate(fila):
            if j == len(fila) - 2:
                s += f"{_fmt(v)}  |  "
            elif j == len(fila) - 1:
                s += f"{_fmt(v)} "
            else:
                s += f"{_fmt(v)}  "
        s += "]"
        lines.append(s)
    return "\n".join(lines)

def _gauss_adelante(M: List[List[Number]], log: List[str]) -> None:
    n_f = len(M)
    paso = 1
    log.append("\n================= ELIMINACIÓN HACIA ADELANTE =================")
    for i in range(n_f):
        # pivot swap si hace falta
        if abs(M[i][i]) < 1e-12:
            for k in range(i + 1, n_f):
                if abs(M[k][i]) > 1e-12:
                    log.append(f"\nPaso {paso}: Intercambiamos F{i+1} ↔ F{k+1}")
                    M[i], M[k] = M[k], M[i]
                    log.append("Resultado del intercambio:\n" + _imprimir_matriz_txt(M))
                    paso += 1
                    break

        piv = M[i][i]
        if abs(piv) < 1e-12:
            continue

        # normalizar pivote
        if abs(piv - 1) > 1e-12:
            log.append(f"Paso {paso}: Normalizamos F{i+1} dividiendo por { _fmt(piv) }")
            for j in range(len(M[i])):
                M[i][j] = M[i][j] / piv
            log.append("Resultado tras normalizar:\n" + _imprimir_matriz_txt(M))
            paso += 1

        # anular debajo
        for k in range(i + 1, n_f):
            fac = M[k][i]
            if abs(fac) > 1e-12:
                log.append(f"Paso {paso}: F{k+1} = F{k+1} - ({_fmt(fac)})·F{i+1}")
                for j in range(len(M[i])):
                    M[k][j] -= fac * M[i][j]
                log.append("Resultado:\n" + _imprimir_matriz_txt(M))
                paso += 1

def _retroceso(M: List[List[Number]], log: List[str]) -> None:
    n_f = len(M)
    n_c = len(M[0]) - 1
    paso = 1
    log.append("\n================= RETROCESO (RREF) =================")
    for i in range(n_f - 1, -1, -1):
        piv_col = -1
        for j in range(n_c):
            if abs(M[i][j]) > 1e-12:
                piv_col = j
                break
        if piv_col == -1:
            continue

        piv = M[i][piv_col]
        if abs(piv - 1) > 1e-12 and abs(piv) > 1e-12:
            for j in range(len(M[i])):
                M[i][j] = M[i][j] / piv
            log.append(f"Paso {paso}: Normalizamos F{i+1} (pivote a 1)\n" + _imprimir_matriz_txt(M))
            paso += 1

        for k in range(i - 1, -1, -1):
            fac = M[k][piv_col]
            if abs(fac) > 1e-12:
                log.append(f"Paso {paso}: F{k+1} = F{k+1} - ({_fmt(fac)})·F{i+1}")
                for j in range(len(M[i])):
                    M[k][j] -= fac * M[i][j]
                log.append("Resultado:\n" + _imprimir_matriz_txt(M))
                paso += 1

def _limpiar(M: List[List[Number]]) -> None:
    for i in range(len(M)):
        for j in range(len(M[i])):
            x = M[i][j]
            if abs(x) < 1e-12:
                M[i][j] = 0
            elif isinstance(x, float) and abs(x - round(x)) < 1e-12:
                M[i][j] = int(round(x))

def _rango(M: List[List[Number]]) -> int:
    n_c = len(M[0]) - 1
    r = 0
    for fila in M:
        if any(abs(v) > 1e-12 for v in fila[:n_c]):
            r += 1
    return r


# --------------------- Interfaz ---------------------
class VectorValidacionView(ttk.Frame):
    def __init__(self, parent, on_back=None):
        super().__init__(parent)
        self.on_back = on_back

        try: self.tk.call("tk", "scaling", UI_SCALE)
        except tk.TclError: pass

        # paleta
        self.bg="#eef4ff"; self.card="#ffffff"; self.primary="#1f4fd6"
        self.text="#0f172a"; self.muted="#475569"

        self._styles()
        self._ui()

    def _styles(self):
        s = ttk.Style(self)
        try: s.theme_use("clam")
        except tk.TclError: pass

        s.configure("Root.TFrame", background=self.bg)
        s.configure("Card.TFrame", background=self.card)
        s.configure("HdrTitle.TLabel", font=("Segoe UI", 24, "bold"), background=self.card, foreground=self.text)
        s.configure("HdrSub.TLabel", font=("Segoe UI", 11), background=self.card, foreground=self.muted)
        s.configure("Sec.TLabel", font=("Segoe UI", 11, "bold"), background=self.card, foreground=self.text)

        s.configure("Primary.TButton", font=("Segoe UI", 12, "bold"), padding=10)
        s.map("Primary.TButton", background=[("!disabled", self.primary), ("active", "#1a43b5")],
                                   foreground=[("!disabled", "white")])
        s.configure("Ghost.TButton", font=("Segoe UI", 11), padding=10)
        s.map("Ghost.TButton", background=[("!disabled", self.card), ("active", "#eef2ff")])
        self.configure(style="Root.TFrame")

    def _ui(self):
        root = tk.Frame(self, bg=self.bg)
        root.pack(fill="both", expand=True, padx=30, pady=30)

        # header
        hshadow = tk.Frame(root, bg="#dfe7fb"); hshadow.pack(fill="x", pady=(0, 14))
        header  = ttk.Frame(hshadow, style="Card.TFrame", padding=16); header.pack(fill="x", padx=1, pady=1)
        ttk.Label(header, text="Vector Validación — Independencia lineal (sistema homogéneo)",
                  style="HdrTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(header, text="Ingrese dimensión n y cantidad de vectores p. Los vectores se capturan por columnas v₁…vₚ.",
                  style="HdrSub.TLabel").grid(row=1, column=0, sticky="w")

        # controles
        cshadow = tk.Frame(root, bg="#dfe7fb"); cshadow.pack(fill="x")
        ctrl = ttk.Frame(cshadow, style="Card.TFrame", padding=12); ctrl.pack(fill="x", padx=1, pady=1)

        self.var_n = tk.IntVar(value=3)
        self.var_p = tk.IntVar(value=3)
        ttk.Label(ctrl, text="Dimensión n:", style="Sec.TLabel").grid(row=0, column=0, padx=(0,6))
        ttk.Spinbox(ctrl, from_=1, to=10, textvariable=self.var_n, width=6).grid(row=0, column=1, padx=(0,16))
        ttk.Label(ctrl, text="Cantidad de vectores p:", style="Sec.TLabel").grid(row=0, column=2, padx=(0,6))
        ttk.Spinbox(ctrl, from_=1, to=10, textvariable=self.var_p, width=6).grid(row=0, column=3, padx=(0,16))

        ttk.Button(ctrl, text="Generar", style="Ghost.TButton", command=self._generar).grid(row=0, column=4, padx=4)
        ttk.Button(ctrl, text="Ejemplo", style="Ghost.TButton", command=self._ejemplo).grid(row=0, column=5, padx=4)
        ttk.Button(ctrl, text="Limpiar",  style="Ghost.TButton", command=self._limpiar).grid(row=0, column=6, padx=4)

        # área principal
        area = tk.Frame(root, bg=self.bg); area.pack(fill="both", expand=True, pady=(14,0))
        area.grid_columnconfigure(0, weight=3, uniform="cols")
        area.grid_columnconfigure(1, weight=4, uniform="cols")

        # izquierda: entradas + resultado
        left_shadow = tk.Frame(area, bg="#dfe7fb"); left_shadow.grid(row=0, column=0, sticky="nsew", padx=(0,8))
        self.left = ttk.Frame(left_shadow, style="Card.TFrame", padding=16); self.left.pack(fill="both", expand=True, padx=1, pady=1)

        ttk.Label(self.left, text="Matriz aumentada [A | 0] (A con columnas v₁…vₚ)", style="Sec.TLabel").grid(row=0, column=0, sticky="w", pady=(0,8))

        self.frame_inputs = ttk.Frame(self.left, style="Card.TFrame"); self.frame_inputs.grid(row=1, column=0, sticky="w")
        self.frame_result = ttk.Frame(self.left, style="Card.TFrame");  self.frame_result.grid(row=2, column=0, sticky="w", pady=(10,0))

        ttk.Label(self.frame_result, text="RREF", style="Sec.TLabel").grid(row=0, column=0, sticky="w")
        self.tbl = self._build_table(self.frame_result, rows=6, cols=4)  # placeholder

        # botones inferiores
        btns = ttk.Frame(self.left, style="Card.TFrame"); btns.grid(row=3, column=0, sticky="w", pady=(10,0))
        ttk.Button(btns, text="Resolver", style="Primary.TButton", command=self._resolver).pack(side="left")
        ttk.Button(btns, text="Regresar", style="Ghost.TButton", command=self._back).pack(side="left", padx=(10,0))

        # derecha: registro
        right_shadow = tk.Frame(area, bg="#dfe7fb"); right_shadow.grid(row=0, column=1, sticky="nsew", padx=(8,0))
        right = ttk.Frame(right_shadow, style="Card.TFrame", padding=16); right.pack(fill="both", expand=True, padx=1, pady=1)
        ttk.Label(right, text="Registro (pasos)", style="Sec.TLabel").pack(anchor="w")

        self.canvas = tk.Canvas(right, bg=self.card, highlightthickness=0)
        vbar = ttk.Scrollbar(right, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vbar.set)
        self.canvas.pack(side="left", fill="both", expand=True); vbar.pack(side="right", fill="y")

        self.right = ttk.Frame(self.canvas, style="Card.TFrame")
        self._win = self.canvas.create_window((0,0), window=self.right, anchor="nw")
        self.txt_log = tk.Text(self.right, height=22, relief="flat", bg="white", wrap="word")
        self.txt_log.pack(fill="both", expand=True)

        self.right.bind("<Configure>", self._on_right_cfg)
        self.canvas.bind("<Configure>", self._on_canvas_cfg)
        self._bind_mousewheel(self.canvas)

        # inicial
        self._generar()

    # --- Treeview centrado
    def _build_table(self, parent, rows: int, cols: int) -> ttk.Treeview:
        tv = ttk.Treeview(parent, show="headings", height=max(6, rows), selectmode="none")
        tv["columns"] = [f"c{k}" for k in range(cols)]
        COL_W = 88
        for k in range(cols):
            col = f"c{k}"
            tv.heading(col, text=f"c{k+1}", anchor="center")
            tv.column(col, width=COL_W, minwidth=COL_W, stretch=False, anchor="center")
        tv.grid(row=1, column=0, sticky="n", pady=(4,0))
        return tv

    def _set_table(self, tv: ttk.Treeview, M: List[List[Number]]):
        for iid in tv.get_children():
            tv.delete(iid)
        if not M:
            return
        cols = len(M[0])
        if len(tv["columns"]) != cols:
            tv["columns"] = [f"c{k}" for k in range(cols)]
        COL_W = 88
        for k in range(cols):
            col = f"c{k}"
            tv.heading(col, text=f"c{k+1}", anchor="center")
            tv.column(col, width=COL_W, minwidth=COL_W, stretch=False, anchor="center")
        for row in M:
            tv.insert("", "end", values=[_fmt(x) for x in row])

    # --- scroll
    def _on_right_cfg(self, _e):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    def _on_canvas_cfg(self, e):
        self.canvas.itemconfigure(self._win, width=e.width)
    def _bind_mousewheel(self, widget):
        widget.bind_all("<MouseWheel>", self._mw)
        widget.bind_all("<Button-4>", self._mw_linux)
        widget.bind_all("<Button-5>", self._mw_linux)
    def _mw(self, e): self.canvas.yview_scroll(int(-e.delta/120), "units")
    def _mw_linux(self, e): self.canvas.yview_scroll(-1 if e.num == 5 else 1, "units")

    def _set_log(self, txt: str):
        self.txt_log.configure(state="normal")
        self.txt_log.delete("1.0", "end")
        self.txt_log.insert("1.0", txt)
        self.txt_log.configure(state="disabled")
        self.canvas.yview_moveto(0)

    # --- generar / ejemplo / limpiar
    def _generar(self):
        for w in self.frame_inputs.winfo_children():
            w.destroy()

        n = max(1, int(self.var_n.get()))
        p = max(1, int(self.var_p.get()))

        head = ttk.Frame(self.frame_inputs, style="Card.TFrame"); head.grid(row=0, column=0, sticky="w")
        for j in range(p):
            ttk.Label(head, text=f"v{j+1}", style="Sec.TLabel", width=6).grid(row=0, column=j, padx=4, pady=(0,2))

        self.ent: List[List[tk.Entry]] = []
        grid = ttk.Frame(self.frame_inputs, style="Card.TFrame"); grid.grid(row=1, column=0, sticky="w")
        for i in range(n):
            row_e = []
            for j in range(p):
                e = tk.Entry(grid, width=6, justify="center", font=("Consolas", 11))
                e.grid(row=i, column=j, padx=4, pady=3)
                e.insert(0, "0")
                row_e.append(e)
            self.ent.append(row_e)

        self._set_table(self.tbl, [[0]*(p+1) for _ in range(max(2, n))])
        self._set_log("")

    def _ejemplo(self):
        n = 3; p = 3
        self.var_n.set(n); self.var_p.set(p)
        self._generar()
        # alterna
        if not hasattr(self, "_toggle_ex"): self._toggle_ex = False
        self._toggle_ex = not self._toggle_ex
        if self._toggle_ex:
            Acols = [[1,0,0],[0,1,0],[0,0,1]]        # independiente
        else:
            Acols = [[1,2,3],[0,1,1],[1,0,1]]        # dependiente

        for j in range(p):
            for i in range(n):
                self.ent[i][j].delete(0,"end")
                self.ent[i][j].insert(0, str(Acols[j][i]))

    def _limpiar(self):
        self._generar()
        self._set_log("")

    # --- resolver
    def _leer(self) -> List[List[int]]:
        n = int(self.var_n.get()); p = int(self.var_p.get())
        M = [[0]*(p+1) for _ in range(n)]
        for j in range(p):
            for i in range(n):
                s = self.ent[i][j].get().strip()
                ok = s[1:].isdigit() if s.startswith("-") else s.isdigit()
                if not ok:
                    raise ValueError(f"Entrada inválida en fila {i+1}, columna v{j+1}")
                M[i][j] = int(s)
        return M

    def _resolver(self):
        try:
            M = self._leer()
        except Exception as e:
            messagebox.showerror("Entrada inválida", str(e))
            return

        log: List[str] = []
        log.append("Matriz aumentada inicial [A | 0]:\n" + _imprimir_matriz_txt(M))
        _gauss_adelante(M, log)
        _retroceso(M, log)
        _limpiar(M)
        log.append("\nMatriz aumentada final (RREF):\n" + _imprimir_matriz_txt(M))

        r = _rango(M)
        p = len(M[0]) - 1
        log.append("\n================= ANÁLISIS FINAL =================")
        log.append(f"Rango(A) = {r}")
        log.append(f"Cantidad de vectores p = {p}")

        if r == p:
            log.append("\nConclusión: Los vectores son LINEALMENTE INDEPENDIENTES.\n"
                       "La única solución del sistema homogéneo es la trivial.")
        else:
            log.append("\nConclusión: Los vectores son LINEALMENTE DEPENDIENTES.\n"
                       "Existen soluciones no triviales.")
            ecuaciones = []
            for fila in M:
                lhs = []
                for j, c in enumerate(fila[:-1], start=1):
                    if abs(c) > 1e-12:
                        lhs.append(f"{_fmt(c)}·x{j}")
                ecuaciones.append(" + ".join(lhs) if lhs else "0")
            log.append("\nEcuaciones (RREF):")
            for eq in ecuaciones:
                log.append(f"  {eq} = 0")

        self._set_table(self.tbl, M)
        self._set_log("\n".join(log))

    # navegación
    def _back(self):
        if callable(self.on_back):
            self.on_back()


# --------------------- API pública ---------------------
def mount_vector_validacion(parent, on_back=None):
    parent.winfo_toplevel().title("UAM — Vector Validación")
    view = VectorValidacionView(parent, on_back=on_back)
    view.pack(fill="both", expand=True)
    return view


# Demo
if __name__ == "__main__":
    root = tk.Tk()
    try: root.state("zoomed")
    except Exception: pass
    mount_vector_validacion(root, on_back=root.destroy)
    root.mainloop()
