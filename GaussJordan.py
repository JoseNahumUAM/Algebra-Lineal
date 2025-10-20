#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GaussJordan.py — RREF (Gauss-Jordan) con UI estilo UAM
• Izquierda: matriz en RREF
• Derecha: Soluciones/Estado + Paso a paso (logs) con un solo scroll
• Botones: Resolver | Regresar
"""

from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass
from typing import List, Union, Dict, Tuple
from fractions import Fraction

Number = Union[Fraction, float]
UI_SCALE = 1.25

# ===================== utils numéricas =====================
def is_zero(x: Number, tol: float = 1e-12) -> bool:
    if isinstance(x, Fraction):
        return x == 0
    return abs(float(x)) < tol

def fmt(x: Number, dec: int = 6) -> str:
    if isinstance(x, Fraction):
        return str(x) if x.denominator != 1 else str(x.numerator)
    s = f"{float(x):.{dec}f}"
    s = s.rstrip("0").rstrip(".") if "." in s else s
    return s if s else "0"

def deepcopy_matrix(M: List[List[Number]]) -> List[List[Number]]:
    return [row[:] for row in M]

# ===================== resultados =====================
@dataclass
class GJResult:
    rref: List[List[Number]]
    pivot_cols: List[int]
    col_to_row: Dict[int, int]
    state: str                     # "unica" | "infinitas" | "inconsistente"
    solutions: List[Number] | Tuple[Dict[int, str], List[int]] | None
    logs: List[str]

# ===================== núcleo Gauss-Jordan =====================
def rref_with_logs(M: List[List[Number]], use_tol: bool = True) -> GJResult:
    A = deepcopy_matrix(M)
    m = len(A)
    n = len(A[0]) - 1
    row = 0
    pivot_cols: List[int] = []
    col_to_row: Dict[int, int] = {}
    logs: List[str] = []

    def z(v: Number) -> bool:
        return is_zero(v, 1e-12 if use_tol else 0.0)

    logs.append("Matriz inicial:")
    for r in A:
        logs.append("  [ " + "  ".join(fmt(x) for x in r[:-1]) + " | " + fmt(r[-1]) + " ]")

    for col in range(n):
        if row >= m:
            break

        # buscar pivote (primer valor != 0 desde 'row')
        sel = None
        for r in range(row, m):
            if not z(A[r][col]):
                sel = r
                break
        if sel is None:
            continue

        # swap si hace falta
        if sel != row:
            A[row], A[sel] = A[sel], A[row]
            logs.append(f"Swap: F{row+1} ↔ F{sel+1}")

        # normalizar pivote a 1
        piv = A[row][col]
        if not (isinstance(piv, Fraction) and piv == 1) and not (not isinstance(piv, Fraction) and abs(float(piv)-1.0) < 1e-15):
            factor = (Fraction(1, 1) / piv) if isinstance(piv, Fraction) else 1.0/float(piv)
            A[row] = [x * factor for x in A[row]]
            logs.append(f"F{row+1} = ({fmt(factor)}) · F{row+1}")

        # eliminar arriba y abajo
        for r in range(m):
            if r == row:
                continue
            fac = A[r][col]
            if z(fac):
                continue
            A[r] = [a - fac * b for a, b in zip(A[r], A[row])]
            logs.append(f"F{r+1} = F{r+1} - ({fmt(fac)}) · F{row+1}")

        pivot_cols.append(col)
        col_to_row[col] = row
        row += 1

    logs.append("Matriz en RREF:")
    for r in A:
        logs.append("  [ " + "  ".join(fmt(x) for x in r[:-1]) + " | " + fmt(r[-1]) + " ]")

    # analizar
    # inconsistente: fila coef=0 y término != 0
    for r in range(m):
        if all(is_zero(A[r][c]) for c in range(n)) and not is_zero(A[r][-1]):
            return GJResult(A, pivot_cols, col_to_row, "inconsistente", None, logs)

    free = [c for c in range(n) if c not in pivot_cols]
    if free:
        # infinitas: construir expresiones
        param_names = {c: f"t{idx+1}" for idx, c in enumerate(free)}
        expr: Dict[int, str] = {}

        # libres = su parámetro
        for c in free:
            expr[c] = param_names[c]

        # pivote en función de libres
        for c in pivot_cols:
            r = col_to_row[c]
            terms: List[str] = []
            const = A[r][-1]
            if not is_zero(const):
                terms.append(fmt(const))
            for lf in free:
                coef = A[r][lf]
                if not is_zero(coef):
                    terms.append(f"{fmt(-coef)}*{param_names[lf]}")
            s = " + ".join(terms).replace("+ -", "- ")
            if s.strip() == "":
                s = "0"
            expr[c] = s

        return GJResult(A, pivot_cols, col_to_row, "infinitas", (expr, free), logs)

    # única
    sol = [Fraction(0) if all(isinstance(x, Fraction) for row in A for x in row) else 0.0 for _ in range(n)]
    for c in pivot_cols:
        r = col_to_row[c]
        sol[c] = A[r][-1]
    return GJResult(A, pivot_cols, col_to_row, "unica", sol, logs)

# ===================== UI =====================
class GaussJordanView(ttk.Frame):
    def __init__(self, parent, on_back=None):
        super().__init__(parent)
        self.on_back = on_back
        try: self.tk.call("tk", "scaling", UI_SCALE)
        except tk.TclError: pass

        # paleta
        self.bg="#eef4ff"; self.card="#ffffff"; self.primary="#1f4fd6"
        self.text="#0f172a"; self.muted="#475569"

        self._build_styles()
        self._build_ui()

    def _build_styles(self):
        s = ttk.Style(self)
        try: s.theme_use("clam")
        except tk.TclError: pass

        s.configure("Root.TFrame", background=self.bg)
        s.configure("Card.TFrame", background=self.card)
        s.configure("HdrTitle.TLabel", font=("Segoe UI", 22, "bold"), background=self.card, foreground=self.text)
        s.configure("HdrSub.TLabel",   font=("Segoe UI", 11), background=self.card, foreground=self.muted)
        s.configure("Sec.TLabel",      font=("Segoe UI", 11, "bold"), background=self.card, foreground=self.text)
        s.configure("Primary.TButton", font=("Segoe UI", 12, "bold"), padding=10)
        s.map("Primary.TButton",
              background=[("!disabled", self.primary), ("active", "#1a43b5")],
              foreground=[("!disabled", "white")])
        s.configure("Ghost.TButton",   font=("Segoe UI", 11), padding=10)
        s.map("Ghost.TButton",
              background=[("!disabled", self.card), ("active", "#eef2ff")])

        self.configure(style="Root.TFrame")

    def _build_ui(self):
        container = tk.Frame(self, bg=self.bg)
        container.pack(fill="both", expand=True, padx=30, pady=30)

        # Header
        hshadow = tk.Frame(container, bg="#dfe7fb"); hshadow.pack(fill="x", pady=(0,14))
        header  = ttk.Frame(hshadow, style="Card.TFrame", padding=18); header.pack(fill="x", padx=1, pady=1)
        ttk.Label(header, text="Gauss-Jordan — RREF (Ax = b)", style="HdrTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(header, text="Ingrese A (m×n) y b (m×1). Enteros, decimales o fracciones (p. ej. 1/2).",
                  style="HdrSub.TLabel").grid(row=1, column=0, sticky="w")

        # Controles
        cshadow = tk.Frame(container, bg="#dfe7fb"); cshadow.pack(fill="x")
        ctrl = ttk.Frame(cshadow, style="Card.TFrame", padding=12); ctrl.pack(fill="x", padx=1, pady=1)
        self.var_m = tk.IntVar(value=3)
        self.var_n = tk.IntVar(value=3)
        self.var_frac = tk.BooleanVar(value=True)

        row = 0
        ttk.Label(ctrl, text="Ecuaciones (m):", style="Sec.TLabel").grid(row=row, column=0, padx=(0,6), pady=4, sticky="w")
        ttk.Spinbox(ctrl, from_=1, to=10, textvariable=self.var_m, width=5).grid(row=row, column=1, padx=(0,16), pady=4)
        ttk.Label(ctrl, text="Incógnitas (n):", style="Sec.TLabel").grid(row=row, column=2, padx=(0,6), pady=4, sticky="w")
        ttk.Spinbox(ctrl, from_=1, to=10, textvariable=self.var_n, width=5).grid(row=row, column=3, padx=(0,16), pady=4)
        ttk.Checkbutton(ctrl, text="Fracciones exactas", variable=self.var_frac).grid(row=row, column=4, padx=(0,16), pady=4)
        ttk.Button(ctrl, text="Generar", style="Ghost.TButton", command=self._generar).grid(row=row, column=5, padx=4, pady=4)
        ttk.Button(ctrl, text="Ejemplo", style="Ghost.TButton", command=self._ejemplo).grid(row=row, column=6, padx=4, pady=4)
        ttk.Button(ctrl, text="Limpiar",  style="Ghost.TButton", command=self._limpiar).grid(row=row, column=7, padx=4, pady=4)

        # Grids A y b
        gshadow = tk.Frame(container, bg="#dfe7fb"); gshadow.pack(fill="x", pady=(14,10))
        grids   = ttk.Frame(gshadow, style="Card.TFrame", padding=16); grids.pack(fill="x", padx=1, pady=1)
        ttk.Label(grids, text="Matriz A (m×n)", style="Sec.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(grids, text="Vector b (m×1)", style="Sec.TLabel").grid(row=0, column=1, sticky="w", padx=(24,0))
        self.frameA = ttk.Frame(grids, style="Card.TFrame"); self.frameA.grid(row=1, column=0, sticky="w")
        self.frameB = ttk.Frame(grids, style="Card.TFrame"); self.frameB.grid(row=1, column=1, sticky="w", padx=(24,0))

        # Acciones
        ashadow = tk.Frame(container, bg="#dfe7fb"); ashadow.pack(fill="x")
        actions = ttk.Frame(ashadow, style="Card.TFrame", padding=12); actions.pack(fill="x", padx=1, pady=1)
        ttk.Button(actions, text="Resolver", style="Primary.TButton", command=self._resolver).pack(side="left")
        ttk.Button(actions, text="Regresar", style="Ghost.TButton", command=self._back).pack(side="right")

        # Resultados
        rshadow = tk.Frame(container, bg="#dfe7fb"); rshadow.pack(fill="both", expand=True, pady=(14,0))
        result  = ttk.Frame(rshadow, style="Card.TFrame", padding=16); result.pack(fill="both", expand=True, padx=1, pady=1)

        # izquierda: RREF sin scroll
        self.left = ttk.Frame(result, style="Card.TFrame"); self.left.pack(side="left", fill="both", expand=True, padx=(0,8))
        ttk.Label(self.left, text="Matriz RREF", style="Sec.TLabel").pack(anchor="w")
        self.tbl = ttk.Treeview(self.left, show="headings", height=10); self.tbl.pack(fill="both", expand=True, pady=(6,10))

        # derecha: soluciones + logs con un solo scroll
        rc = ttk.Frame(result, style="Card.TFrame"); rc.pack(side="left", fill="both", expand=True, padx=(8,0))
        self.canvas = tk.Canvas(rc, highlightthickness=0, bg=self.card)
        vbar = ttk.Scrollbar(rc, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vbar.set)
        self.canvas.pack(side="left", fill="both", expand=True); vbar.pack(side="right", fill="y")

        self.right = ttk.Frame(self.canvas, style="Card.TFrame", padding=0)
        self._win = self.canvas.create_window((0,0), window=self.right, anchor="nw")

        ttk.Label(self.right, text="Soluciones / Estado", style="Sec.TLabel").pack(anchor="w")
        self.txt_sol = tk.Text(self.right, height=8, relief="flat", bg="white", wrap="word")
        self.txt_sol.pack(fill="x", pady=(6,12))

        ttk.Label(self.right, text="Pasos (log)", style="Sec.TLabel").pack(anchor="w")
        self.txt_log = tk.Text(self.right, height=14, relief="flat", bg="white", wrap="none")
        self.txt_log.pack(fill="both", expand=True, pady=(6,0))

        # eventos de scroll
        self.right.bind("<Configure>", self._on_right_config)
        self.canvas.bind("<Configure>", self._on_canvas_config)
        self._bind_mousewheel(self.canvas)

        # inicial
        self._generar()

    # -------- scroll helpers --------
    def _on_right_config(self, _e):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    def _on_canvas_config(self, e):
        self.canvas.itemconfigure(self._win, width=e.width)
    def _bind_mousewheel(self, widget):
        widget.bind_all("<MouseWheel>", self._mw)
        widget.bind_all("<Button-4>", self._mw_linux)
        widget.bind_all("<Button-5>", self._mw_linux)
    def _mw(self, e): self.canvas.yview_scroll(int(-e.delta/120), "units")
    def _mw_linux(self, e): self.canvas.yview_scroll(-1 if e.num == 5 else 1, "units")
    def _scroll_top(self): self.canvas.yview_moveto(0)

    # -------- ui actions --------
    def _back(self):
        if callable(self.on_back):
            self.on_back()

    def _limpiar(self):
        for w in self.frameA.winfo_children(): w.destroy()
        for w in self.frameB.winfo_children(): w.destroy()
        self._generar()
        self._render_rref([])
        self._set_text(self.txt_sol, ""); self._set_text(self.txt_log, "")
        self._scroll_top()

    def _generar(self):
        for w in self.frameA.winfo_children(): w.destroy()
        for w in self.frameB.winfo_children(): w.destroy()
        m = max(1, int(self.var_m.get()))
        n = max(1, int(self.var_n.get()))
        self.ent_A: List[List[tk.Entry]] = []
        self.ent_b: List[tk.Entry] = []

        for i in range(m):
            row_e: List[tk.Entry] = []
            for j in range(n):
                e = tk.Entry(self.frameA, width=7, justify="center", font=("Consolas", 11))
                e.grid(row=i, column=j, padx=4, pady=4); e.insert(0, "0")
                row_e.append(e)
            self.ent_A.append(row_e)
            eb = tk.Entry(self.frameB, width=7, justify="center", font=("Consolas", 11))
            eb.grid(row=i, column=0, padx=4, pady=4); eb.insert(0, "0")
            self.ent_b.append(eb)

        self._render_rref([])

    def _ejemplo(self):
        self.var_m.set(3); self.var_n.set(3)
        self._generar()
        A = [["1","2","-1"], ["0","3","2"], ["0","0","-1"]]
        B = ["3","9","8"]
        for i in range(3):
            for j in range(3):
                self.ent_A[i][j].delete(0,"end"); self.ent_A[i][j].insert(0, A[i][j])
            self.ent_b[i].delete(0,"end"); self.ent_b[i].insert(0, B[i])

    def _leer(self) -> List[List[Number]]:
        m = len(self.ent_A); n = len(self.ent_A[0]) if m else 0
        use_frac = self.var_frac.get()
        M: List[List[Number]] = []
        for i in range(m):
            row: List[Number] = []
            for j in range(n):
                t = self.ent_A[i][j].get().strip()
                row.append(Fraction(t) if use_frac else float(t))
            tb = self.ent_b[i].get().strip()
            row.append(Fraction(tb) if use_frac else float(tb))
            M.append(row)
        return M

    def _resolver(self):
        try:
            M = self._leer()
        except Exception as e:
            messagebox.showerror("Entrada inválida", f"Revisa los valores: {e}")
            return
        res = rref_with_logs(M, use_tol=not self.var_frac.get())
        self._render_rref(res.rref)

        # soluciones / estado
        if res.state == "inconsistente":
            sol_txt = "Conclusión: sistema INCONSISTENTE (sin solución)."
        elif res.state == "unica":
            sol_txt = "Conclusión: sistema con SOLUCIÓN ÚNICA."
            for i, v in enumerate(res.solutions, 1):  # type: ignore
                sol_txt += f"\nx{i} = {fmt(v)}"
        else:
            exprs, free = res.solutions  # type: ignore
            sol_txt = "Conclusión: sistema con INFINITAS soluciones."
            if free:
                sol_txt += "\nVariables libres: " + ", ".join(f"x{c+1}" for c in free)
            sol_txt += "\n\nExpresiones:"
            n = len(res.rref[0]) - 1
            for c in range(n):
                if isinstance(exprs, dict) and c in exprs:  # type: ignore
                    sol_txt += f"\n x{c+1} = {exprs[c]}"   # type: ignore
                else:
                    sol_txt += f"\n x{c+1} = 0"

        self._set_text(self.txt_sol, sol_txt)
        self._set_text(self.txt_log, "\n".join(res.logs))
        self._scroll_top()

    # -------- render helpers --------
    def _render_rref(self, T: List[List[Number]]):
        for c in self.tbl.get_children(): self.tbl.delete(c)
        self.tbl["columns"] = ()
        if not T: return
        cols = len(T[0])
        self.tbl["columns"] = [f"c{k}" for k in range(cols)]
        for k in range(cols):
            hdr = f"a{k+1}" if k < cols-1 else "b"
            self.tbl.heading(f"c{k}", text=hdr)
            self.tbl.column(f"c{k}", width=90, anchor="center")
        for row in T:
            self.tbl.insert("", "end", values=[fmt(x) for x in row])

    def _set_text(self, widget: tk.Text, text: str):
        widget.configure(state="normal")
        widget.delete("1.0","end")
        widget.insert("1.0", text)
        widget.configure(state="disabled")

# ===================== API pública =====================
def mount_gauss_jordan(parent, on_back=None):
    """<< ESTA FUNCIÓN ES LA QUE IMPORTA Calculadora.py >>"""
    parent.winfo_toplevel().title("UAM — Gauss-Jordan (RREF)")
    view = GaussJordanView(parent, on_back=on_back)
    view.pack(fill="both", expand=True)
    return view
