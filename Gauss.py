#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gauss.py — Método de Gauss integrado (con paso a paso visible)
• Botones:  Resolver  |  Regresar al menú
• Resolver: triangulariza + soluciones + MUESTRA los logs (paso a paso)
• Scroll: SOLO para el panel derecho (Soluciones + Logs). La matriz no se mueve.
"""
from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox
from fractions import Fraction
from dataclasses import dataclass
from typing import List, Union

Number = Union[Fraction, float]
UI_SCALE = 1.25

# ---------- Utils ----------
def formatear_num(x: Number, dec=6) -> str:
    if isinstance(x, Fraction):
        return str(x) if x.denominator != 1 else str(x.numerator)
    s = f"{float(x):.{dec}f}"
    s = s.rstrip("0").rstrip(".") if "." in s else s
    return s if s else "0"

def es_cero(x: Number, tol: float = 1e-12) -> bool:
    if isinstance(x, Fraction): return x == 0
    return abs(float(x)) < tol

def copiar_matriz(M: List[List[Number]]) -> List[List[Number]]:
    return [row[:] for row in M]

# ---------- Resultado ----------
@dataclass
class GaussResultado:
    triangular: List[List[Number]]
    estado: str                    # "unica" | "infinitas" | "incompatible"
    variables_libres: List[int]
    soluciones: List[Number]
    logs: List[str]                # <- paso a paso

# ---------- Núcleo (con logs) ----------
def gauss_resolver(matriz: List[List[Number]], usar_tol: bool = True) -> GaussResultado:
    logs: List[str] = []
    A = copiar_matriz(matriz)
    m = len(A); n = len(A[0]) - 1; filas, cols = m, n + 1

    def _zero(v: Number) -> bool:
        return es_cero(v, 1e-12 if usar_tol else 0.0)

    # Eliminación a triangular superior (pivoteo parcial)
    for i in range(min(filas, n)):
        logs.append(f"\n— Iteración {i+1}: columna {i+1}")
        max_row = max(range(i, filas), key=lambda r: abs(float(A[r][i])))
        if _zero(A[max_row][i]):
            logs.append(f"Columna {i+1} sin pivote (columna libre).")
            continue
        if max_row != i:
            A[i], A[max_row] = A[max_row], A[i]
            logs.append(f"Swap: F{i+1} ↔ F{max_row+1}")
        piv = A[i][i]
        logs.append(f"Pivote: {formatear_num(piv)} (F{i+1}, C{i+1})")

        for j in range(i+1, filas):
            if _zero(A[j][i]): 
                continue
            factor = A[j][i] / piv
            logs.append(f"F{j+1} = F{j+1} - ({formatear_num(factor)})·F{i+1}")
            for k in range(i, cols):
                A[j][k] = A[j][k] - factor * A[i][k]

    # Analizar sistema
    pivotes = []
    incompatible = False
    for i in range(filas):
        pcol = -1
        for j in range(n):
            if not _zero(A[i][j]):
                pcol = j
                if j not in pivotes: pivotes.append(j)
                break
        if pcol == -1 and not _zero(A[i][-1]):
            incompatible = True

    if incompatible: estado = "incompatible"
    elif len(pivotes) < n: estado = "infinitas"
    else: estado = "unica"

    variables_libres = [j for j in range(n) if j not in pivotes]

    # Sustitución regresiva
    sol = [Fraction(0) if all(isinstance(x, Fraction) for row in A for x in row) else 0.0 for _ in range(n)]
    if estado != "incompatible":
        for i in range(filas-1, -1, -1):
            pcol = -1
            for j in range(n):
                if not _zero(A[i][j]): pcol = j; break
            if pcol == -1: continue
            suma = A[i][-1]
            for j in range(pcol+1, n):
                if not _zero(A[i][j]): suma = suma - A[i][j]*sol[j]
            if _zero(A[i][pcol]): continue
            sol[pcol] = suma / A[i][pcol]
            logs.append(f"x{pcol+1} = {formatear_num(suma)} / {formatear_num(A[i][pcol])} = {formatear_num(sol[pcol])}")

    return GaussResultado(triangular=A, estado=estado,
                          variables_libres=variables_libres, soluciones=sol, logs=logs)

# ---------- Vista Tk ----------
class GaussView(ttk.Frame):
    def __init__(self, parent, on_back=None):
        super().__init__(parent)
        self.on_back = on_back
        try: self.tk.call("tk", "scaling", UI_SCALE)
        except tk.TclError: pass

        self.bg="#eef4ff"; self.card="#ffffff"; self.primary="#1f4fd6"
        self.stroke="#dbe3f7"; self.text="#0f172a"; self.muted="#475569"

        self.configure(style="Root.TFrame")
        self._build_styles()
        self._build_ui()

    def _build_styles(self):
        s = ttk.Style(self)
        try: s.theme_use("clam")
        except tk.TclError: pass
        s.configure("Root.TFrame", background=self.bg)
        s.configure("Card.TFrame", background=self.card)
        s.configure("HdrTitle.TLabel", font=("Segoe UI", 22, "bold"), background=self.card, foreground=self.text)
        s.configure("HdrSub.TLabel", font=("Segoe UI", 11), background=self.card, foreground=self.muted)
        s.configure("Sec.TLabel", font=("Segoe UI", 11, "bold"), background=self.card, foreground=self.text)
        s.configure("Ghost.TButton", font=("Segoe UI", 11), padding=10)
        s.map("Ghost.TButton", background=[("!disabled", self.card), ("active", "#eef2ff")])
        s.configure("Primary.TButton", font=("Segoe UI", 12, "bold"), padding=10)
        s.map("Primary.TButton",
              background=[("!disabled", self.primary), ("active", "#1a43b5")],
              foreground=[("!disabled", "white")])

    def _build_ui(self):
        container = tk.Frame(self, bg=self.bg)
        container.pack(fill="both", expand=True, padx=30, pady=30)

        # Header
        header_shadow = tk.Frame(container, bg="#dfe7fb")
        header_shadow.pack(fill="x", pady=(0, 14))
        header = ttk.Frame(header_shadow, style="Card.TFrame", padding=18)
        header.pack(fill="x", padx=1, pady=1)
        ttk.Label(header, text="Gauss — Sistema Ax = b", style="HdrTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(header, text="Ingrese A (m×n) y b (m×1). Enteros, decimales o fracciones (p. ej. 1/2).",
                  style="HdrSub.TLabel").grid(row=1, column=0, sticky="w")

        # Controles
        ctrl_shadow = tk.Frame(container, bg="#dfe7fb"); ctrl_shadow.pack(fill="x")
        ctrl = ttk.Frame(ctrl_shadow, style="Card.TFrame", padding=12); ctrl.pack(fill="x", padx=1, pady=1)
        self.var_m = tk.IntVar(value=3); self.var_n = tk.IntVar(value=3); self.var_frac = tk.BooleanVar(value=True)

        row = 0
        ttk.Label(ctrl, text="Ecuaciones (m):", style="Sec.TLabel").grid(row=row, column=0, padx=(0,6), pady=4, sticky="w")
        ttk.Spinbox(ctrl, from_=1, to=10, textvariable=self.var_m, width=5).grid(row=row, column=1, padx=(0,16), pady=4)
        ttk.Label(ctrl, text="Incógnitas (n):", style="Sec.TLabel").grid(row=row, column=2, padx=(0,6), pady=4, sticky="w")
        ttk.Spinbox(ctrl, from_=1, to=10, textvariable=self.var_n, width=5).grid(row=row, column=3, padx=(0,16), pady=4)
        ttk.Checkbutton(ctrl, text="Fracciones exactas", variable=self.var_frac).grid(row=row, column=4, padx=(0,16), pady=4)
        ttk.Button(ctrl, text="Generar", style="Ghost.TButton", command=self._generar_grids).grid(row=row, column=5, padx=4, pady=4)
        ttk.Button(ctrl, text="Ejemplo", style="Ghost.TButton", command=self._cargar_ejemplo).grid(row=row, column=6, padx=4, pady=4)
        ttk.Button(ctrl, text="Limpiar", style="Ghost.TButton", command=self._limpiar_todo).grid(row=row, column=7, padx=4, pady=4)

        # Grillas A y b
        grids_shadow = tk.Frame(container, bg="#dfe7fb"); grids_shadow.pack(fill="x", pady=(14, 10))
        grids = ttk.Frame(grids_shadow, style="Card.TFrame", padding=16); grids.pack(fill="x", padx=1, pady=1)

        ttk.Label(grids, text="Matriz A (m×n)", style="Sec.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(grids, text="Vector b (m×1)", style="Sec.TLabel").grid(row=0, column=1, sticky="w", padx=(24,0))

        self.frameA = ttk.Frame(grids, style="Card.TFrame")
        self.frameB = ttk.Frame(grids, style="Card.TFrame")
        self.frameA.grid(row=1, column=0, sticky="w")
        self.frameB.grid(row=1, column=1, sticky="w", padx=(24,0))

        # Acciones
        actions_shadow = tk.Frame(container, bg="#dfe7fb"); actions_shadow.pack(fill="x")
        actions = ttk.Frame(actions_shadow, style="Card.TFrame", padding=12); actions.pack(fill="x", padx=1, pady=1)
        ttk.Button(actions, text="Resolver", style="Primary.TButton", command=self._resolver).pack(side="left")
        ttk.Button(actions, text="Regresar", style="Ghost.TButton", command=self._volver).pack(side="right")

        # ===== Resultados =====
        result_shadow = tk.Frame(container, bg="#dfe7fb")
        result_shadow.pack(fill="both", expand=True, pady=(14,0))
        result = ttk.Frame(result_shadow, style="Card.TFrame", padding=16)
        result.pack(fill="both", expand=True, padx=1, pady=1)

        # Izquierda: MATRIZ (sin scroll)
        self.left = ttk.Frame(result, style="Card.TFrame")
        self.left.pack(side="left", fill="both", expand=True, padx=(0,8))
        ttk.Label(self.left, text="Matriz Triangular", style="Sec.TLabel").pack(anchor="w")
        self.tbl = ttk.Treeview(self.left, show="headings", height=10)
        self.tbl.pack(fill="both", expand=True, pady=(6, 10))

        # Derecha: SOLUCIONES + LOGS con scroll único
        right_container = ttk.Frame(result, style="Card.TFrame")
        right_container.pack(side="left", fill="both", expand=True, padx=(8,0))

        self.r_canvas = tk.Canvas(right_container, highlightthickness=0, bg=self.card)
        self.r_scroll = ttk.Scrollbar(right_container, orient="vertical", command=self.r_canvas.yview)
        self.r_canvas.configure(yscrollcommand=self.r_scroll.set)
        self.r_canvas.pack(side="left", fill="both", expand=True)
        self.r_scroll.pack(side="right", fill="y")

        self.right = ttk.Frame(self.r_canvas, style="Card.TFrame", padding=0)
        self.r_window = self.r_canvas.create_window((0,0), window=self.right, anchor="nw")

        ttk.Label(self.right, text="Soluciones / Estado", style="Sec.TLabel").pack(anchor="w")
        self.txt_sol = tk.Text(self.right, height=8, relief="flat", bg="white", wrap="word")
        self.txt_sol.pack(fill="x", pady=(6, 12))

        ttk.Label(self.right, text="Pasos (log)", style="Sec.TLabel").pack(anchor="w")
        self.txt_log = tk.Text(self.right, height=14, relief="flat", bg="white", wrap="none")
        self.txt_log.pack(fill="both", expand=True, pady=(6, 0))

        # Eventos de scroll/resize solo para el panel derecho
        self.right.bind("<Configure>", self._on_right_configure)
        self.r_canvas.bind("<Configure>", self._on_canvas_configure)
        self._bind_mousewheel(self.r_canvas)

        # Grillas iniciales
        self._generar_grids()

    # ----- scroll helpers (solo derecho) -----
    def _on_right_configure(self, _evt):
        self.r_canvas.configure(scrollregion=self.r_canvas.bbox("all"))

    def _on_canvas_configure(self, evt):
        self.r_canvas.itemconfigure(self.r_window, width=evt.width)

    def _bind_mousewheel(self, widget):
        widget.bind_all("<MouseWheel>", self._on_mousewheel)      # Win/Mac
        widget.bind_all("<Button-4>", self._on_mousewheel_linux)  # Linux up
        widget.bind_all("<Button-5>", self._on_mousewheel_linux)  # Linux down

    def _on_mousewheel(self, event):
        self.r_canvas.yview_scroll(int(-event.delta/120), "units")

    def _on_mousewheel_linux(self, event):
        self.r_canvas.yview_scroll(-1 if event.num == 5 else 1, "units")

    def _scroll_to_top(self):
        self.r_canvas.yview_moveto(0)

    # ----- acciones UI -----
    def _volver(self):
        if callable(self.on_back): self.on_back()

    def _limpiar_todo(self):
        for w in self.frameA.winfo_children(): w.destroy()
        for w in self.frameB.winfo_children(): w.destroy()
        self._generar_grids()
        self._render_triangular([])
        self._set_text(self.txt_sol, ""); self._set_text(self.txt_log, "")
        self._scroll_to_top()

    def _generar_grids(self):
        for w in self.frameA.winfo_children(): w.destroy()
        for w in self.frameB.winfo_children(): w.destroy()
        m = max(1, int(self.var_m.get())); n = max(1, int(self.var_n.get()))
        self.ent_A: list[list[tk.Entry]] = []; self.ent_b: list[tk.Entry] = []
        for i in range(m):
            row_entries = []
            for j in range(n):
                e = tk.Entry(self.frameA, width=7, justify="center", font=("Consolas", 11))
                e.grid(row=i, column=j, padx=4, pady=4); e.insert(0, "0"); row_entries.append(e)
            self.ent_A.append(row_entries)
            eb = tk.Entry(self.frameB, width=7, justify="center", font=("Consolas", 11))
            eb.grid(row=i, column=0, padx=4, pady=4); eb.insert(0, "0"); self.ent_b.append(eb)
        self._render_triangular([])

    def _cargar_ejemplo(self):
        self.var_m.set(3); self.var_n.set(3)
        self._generar_grids()
        datosA = [["2","1","-1"], ["-3","-1","2"], ["-2","1","2"]]; datosb = ["8","-11","-3"]
        for i in range(3):
            for j in range(3):
                self.ent_A[i][j].delete(0,"end"); self.ent_A[i][j].insert(0, datosA[i][j])
            self.ent_b[i].delete(0,"end"); self.ent_b[i].insert(0, datosb[i])

    def _leer_matriz(self) -> List[List[Number]]:
        m = len(self.ent_A); n = len(self.ent_A[0]) if m else 0
        usar_frac = self.var_frac.get(); M: List[List[Number]] = []
        for i in range(m):
            fila: List[Number] = []
            for j in range(n):
                txt = self.ent_A[i][j].get().strip()
                fila.append(Fraction(txt) if usar_frac else float(txt))
            btxt = self.ent_b[i].get().strip()
            fila.append(Fraction(btxt) if usar_frac else float(btxt))
            M.append(fila)
        return M

    def _resolver(self):
        """Resolver: triangulariza + soluciones y muestra logs."""
        try:
            M = self._leer_matriz()
        except Exception as e:
            messagebox.showerror("Entrada inválida", f"Revisa los valores: {e}"); return
        res = gauss_resolver(M, usar_tol=not self.var_frac.get())
        self._render_triangular(res.triangular)

        # Soluciones / Estado
        sol_txt = self._texto_estado(res)
        if res.estado == "unica":
            for i, v in enumerate(res.soluciones, 1): sol_txt += f"\nx{i} = {formatear_num(v)}"
        elif res.estado == "infinitas" and res.variables_libres:
            sol_txt += "\nVariables libres: " + ", ".join(f"x{j+1}" for j in res.variables_libres)
        self._set_text(self.txt_sol, sol_txt)

        # Logs
        self._set_text(self.txt_log, "\n".join(res.logs))
        self._scroll_to_top()

    # ----- helpers render -----
    def _render_triangular(self, T: List[List[Number]]):
        for c in self.tbl.get_children(): self.tbl.delete(c)
        self.tbl["columns"] = ()
        if not T: return
        cols = len(T[0]); self.tbl["columns"] = [f"c{k}" for k in range(cols)]
        for k in range(cols):
            hdr = f"a{k+1}" if k < cols-1 else "b"
            self.tbl.heading(f"c{k}", text=hdr); self.tbl.column(f"c{k}", width=90, anchor="center")
        for row in T: self.tbl.insert("", "end", values=[formatear_num(x) for x in row])

    def _set_text(self, widget: tk.Text, text: str):
        widget.configure(state="normal"); widget.delete("1.0","end"); widget.insert("1.0", text); widget.configure(state="disabled")

    def _texto_estado(self, res: GaussResultado) -> str:
        if res.estado == "incompatible": return "Conclusión: sistema INCOMPATIBLE (sin solución)."
        if res.estado == "infinitas":     return "Conclusión: sistema con INFINITAS soluciones."
        return "Conclusión: sistema con SOLUCIÓN ÚNICA."

# ---------- API pública ----------
def mount_gauss(parent, on_back=None):
    view = GaussView(parent, on_back=on_back)
    view.pack(fill="both", expand=True)
    return view
