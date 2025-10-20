#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MatrizInversa.py — Cálculo de A⁻¹ (Gauss-Jordan) con interfaz UAM
• Izquierda: matriz A⁻¹ (tabla)
• Derecha: log de pasos y verificación A×A⁻¹ = I (scroll único)
• Botones: Calcular inversa | Verificar | Limpiar | Regresar
"""

from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox
from fractions import Fraction
from typing import List, Union, Tuple

# --------------------- tipos / config ---------------------
Number = Union[Fraction, float]
UI_SCALE = 1.25

# --------------------- helpers numéricos ---------------------
def is_zero(x: Number, tol: float = 1e-12) -> bool:
    if isinstance(x, Fraction):
        return x == 0
    return abs(float(x)) < tol

def to_str(x: Number, dec: int = 6) -> str:
    """Fracciones como 'p/q' o enteros; floats con trimming."""
    if isinstance(x, Fraction):
        return str(x) if x.denominator != 1 else str(x.numerator)
    s = f"{float(x):.{dec}f}"
    return s.rstrip("0").rstrip(".") if "." in s else s

def deepcopy(M: List[List[Number]]) -> List[List[Number]]:
    return [row[:] for row in M]

# --------------------- núcleo inversa con logs ---------------------
def inverse_with_logs(A_in: List[List[Number]], use_tol_for_float: bool = True
                      ) -> Tuple[List[List[Number]] | None, List[str], List[List[Number]]]:
    """
    Devuelve (A_inv, logs, augmented_final). Si no es invertible, A_inv=None.
    Mantiene exactitud si todos los elementos son Fraction.
    """
    A = deepcopy(A_in)
    n = len(A)
    logs: List[str] = []

    # construir aumentada [A | I] preservando tipo
    aug: List[List[Number]] = []
    for i in range(n):
        left = A[i][:]
        if all(isinstance(x, Fraction) for x in left):
            right = [Fraction(1 if j == i else 0, 1) for j in range(n)]
        else:
            right = [1.0 if j == i else 0.0 for j in range(n)]
        aug.append(left + right)

    def z(v: Number) -> bool:
        return is_zero(v, 1e-12 if use_tol_for_float else 0.0)

    logs.append("Matriz aumentada inicial [A | I]:")
    for r in aug:
        logs.append("  [ " + "  ".join(to_str(x) for x in r[:n]) + " | " +
                    "  ".join(to_str(x) for x in r[n:]) + " ]")

    row = 0
    for col in range(n):
        if row >= n:
            break

        # buscar pivote
        sel = None
        for r in range(row, n):
            if not z(aug[r][col]):
                sel = r
                break
        if sel is None:
            logs.append(f"Columna {col+1}: sin pivote → matriz NO invertible.")
            return None, logs, aug

        # swap si hace falta
        if sel != row:
            aug[row], aug[sel] = aug[sel], aug[row]
            logs.append(f"Swap: F{row+1} ↔ F{sel+1}")

        # normalizar pivote a 1
        piv = aug[row][col]
        piv_is_one = (isinstance(piv, Fraction) and piv == 1) or (not isinstance(piv, Fraction) and abs(float(piv) - 1.0) < 1e-15)
        if not piv_is_one:
            factor = (Fraction(1, 1) / piv) if isinstance(piv, Fraction) else 1.0 / float(piv)
            aug[row] = [x * factor for x in aug[row]]
            logs.append(f"F{row+1} = ({to_str(factor)}) · F{row+1}")

        # eliminar arriba y abajo
        for r in range(n):
            if r == row:
                continue
            fac = aug[r][col]
            if z(fac):
                continue
            aug[r] = [a - fac * b for a, b in zip(aug[r], aug[row])]
            logs.append(f"F{r+1} = F{r+1} - ({to_str(fac)}) · F{row+1}")

        row += 1

    logs.append("Aumentada final (debería ser [I | A⁻¹]):")
    for r in aug:
        logs.append("  [ " + "  ".join(to_str(x) for x in r[:n]) + " | " +
                    "  ".join(to_str(x) for x in r[n:]) + " ]")

    # extraer A^-1
    Ainv = [r[n:] for r in aug]
    logs.append("La matriz ES invertible. A⁻¹ extraída de la parte derecha.")
    return Ainv, logs, aug

def matmul(A: List[List[Number]], B: List[List[Number]]) -> List[List[Number]]:
    m, k, n = len(A), len(A[0]), len(B[0])
    use_frac = all(isinstance(x, Fraction) for row in A for x in row) and \
               all(isinstance(x, Fraction) for row in B for x in row)
    out: List[List[Number]] = []
    for i in range(m):
        row: List[Number] = []
        for j in range(n):
            s: Number = Fraction(0, 1) if use_frac else 0.0
            for t in range(k):
                ai, bj = A[i][t], B[t][j]
                if use_frac:
                    if not isinstance(ai, Fraction): ai = Fraction(ai)
                    if not isinstance(bj, Fraction): bj = Fraction(bj)
                s = s + ai * bj  # type: ignore
            row.append(s)
        out.append(row)
    return out

def is_identity(M: List[List[Number]], tol: float = 1e-9) -> bool:
    n = len(M)
    use_frac = all(isinstance(x, Fraction) for row in M for x in row)
    for i in range(n):
        for j in range(n):
            if i == j:
                target: Number = Fraction(1, 1) if use_frac else 1.0
                if is_zero(M[i][j] - target, tol) is False:
                    return False
            else:
                if not is_zero(M[i][j], tol):
                    return False
    return True

# --------------------- UI ---------------------
class InversaView(ttk.Frame):
    def __init__(self, parent, on_back=None):
        super().__init__(parent)
        self.on_back = on_back
        try:
            self.tk.call("tk", "scaling", UI_SCALE)
        except tk.TclError:
            pass

        # paleta
        self.bg = "#eef4ff"; self.card = "#ffffff"; self.primary = "#1f4fd6"
        self.text = "#0f172a"; self.muted = "#475569"

        self._styles()
        self._ui()

    def _styles(self):
        s = ttk.Style(self)
        try: s.theme_use("clam")
        except tk.TclError: pass

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
        s.map("Ghost.TButton", background=[("!disabled", self.card), ("active", "#eef2ff")])

        self.configure(style="Root.TFrame")

    def _ui(self):
        container = tk.Frame(self, bg=self.bg)
        container.pack(fill="both", expand=True, padx=30, pady=30)

        # Header
        hshadow = tk.Frame(container, bg="#dfe7fb"); hshadow.pack(fill="x", pady=(0, 14))
        header  = ttk.Frame(hshadow, style="Card.TFrame", padding=18); header.pack(fill="x", padx=1, pady=1)
        ttk.Label(header, text="Matriz Inversa — Método Gauss-Jordan",
                  style="HdrTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(header, text="Ingrese A (n×n). Enteros, decimales o fracciones (p. ej. 1/2).",
                  style="HdrSub.TLabel").grid(row=1, column=0, sticky="w")

        # Controles
        cshadow = tk.Frame(container, bg="#dfe7fb"); cshadow.pack(fill="x")
        ctrl = ttk.Frame(cshadow, style="Card.TFrame", padding=12); ctrl.pack(fill="x", padx=1, pady=1)

        self.var_n = tk.IntVar(value=3)
        self.var_frac = tk.BooleanVar(value=True)
        ttk.Label(ctrl, text="Tamaño n:", style="Sec.TLabel").grid(row=0, column=0, padx=(0, 6))
        ttk.Spinbox(ctrl, from_=1, to=8, textvariable=self.var_n, width=5).grid(row=0, column=1, padx=(0, 16))
        ttk.Checkbutton(ctrl, text="Fracciones exactas", variable=self.var_frac).grid(row=0, column=2, padx=(0, 16))
        ttk.Button(ctrl, text="Generar",  style="Ghost.TButton", command=self._generar).grid(row=0, column=3, padx=4)
        ttk.Button(ctrl, text="Ejemplo",  style="Ghost.TButton", command=self._ejemplo).grid(row=0, column=4, padx=4)
        ttk.Button(ctrl, text="Limpiar",   style="Ghost.TButton", command=self._limpiar).grid(row=0, column=5, padx=4)
        ttk.Button(ctrl, text="Regresar", style="Ghost.TButton", command=self._back).grid(row=0, column=6, padx=4)

        # Grid de A
        gshadow = tk.Frame(container, bg="#dfe7fb"); gshadow.pack(fill="x", pady=(14, 10))
        grids = ttk.Frame(gshadow, style="Card.TFrame", padding=16); grids.pack(fill="x", padx=1, pady=1)
        ttk.Label(grids, text="Matriz A (n×n)", style="Sec.TLabel").grid(row=0, column=0, sticky="w")
        self.frameA = ttk.Frame(grids, style="Card.TFrame"); self.frameA.grid(row=1, column=0, sticky="w")

        # Acciones
        ashadow = tk.Frame(container, bg="#dfe7fb"); ashadow.pack(fill="x")
        actions = ttk.Frame(ashadow, style="Card.TFrame", padding=12); actions.pack(fill="x", padx=1, pady=1)
        ttk.Button(actions, text="Calcular inversa", style="Primary.TButton", command=self._calcular).pack(side="left")
        ttk.Button(actions, text="Verificar A×A⁻¹", style="Ghost.TButton", command=self._verificar).pack(side="left", padx=(8, 0))

        # Resultados
        rshadow = tk.Frame(container, bg="#dfe7fb"); rshadow.pack(fill="both", expand=True, pady=(14, 0))
        result  = ttk.Frame(rshadow, style="Card.TFrame", padding=16); result.pack(fill="both", expand=True, padx=1, pady=1)

        # izquierda: A^-1
        left = ttk.Frame(result, style="Card.TFrame"); left.pack(side="left", fill="both", expand=True, padx=(0, 8))
        ttk.Label(left, text="Matriz A⁻¹", style="Sec.TLabel").pack(anchor="w")
        self.tbl_inv = ttk.Treeview(left, show="headings", height=12); self.tbl_inv.pack(fill="both", expand=True, pady=(6, 10))

        # derecha: log + verificación (scroll único)
        rc = ttk.Frame(result, style="Card.TFrame"); rc.pack(side="left", fill="both", expand=True, padx=(8, 0))
        self.canvas = tk.Canvas(rc, bg=self.card, highlightthickness=0)
        vbar = ttk.Scrollbar(rc, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vbar.set)
        self.canvas.pack(side="left", fill="both", expand=True); vbar.pack(side="right", fill="y")
        self.right = ttk.Frame(self.canvas, style="Card.TFrame")
        self._win = self.canvas.create_window((0, 0), window=self.right, anchor="nw")

        ttk.Label(self.right, text="Pasos (log)", style="Sec.TLabel").pack(anchor="w")
        self.txt_log = tk.Text(self.right, height=18, relief="flat", bg="white", wrap="word")
        self.txt_log.pack(fill="both", expand=True, pady=(6, 12))

        ttk.Label(self.right, text="Verificación A × A⁻¹ = I", style="Sec.TLabel").pack(anchor="w")
        self.txt_ver = tk.Text(self.right, height=6, relief="flat", bg="white", wrap="word")
        self.txt_ver.pack(fill="both", expand=False, pady=(6, 0))

        # scroll events
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
    def _mw(self, e): self.canvas.yview_scroll(int(-e.delta / 120), "units")
    def _mw_linux(self, e): self.canvas.yview_scroll(-1 if e.num == 5 else 1, "units")
    def _scroll_top(self): self.canvas.yview_moveto(0)

    # -------- acciones UI --------
    def _back(self):
        if callable(self.on_back):
            self.on_back()

    def _limpiar(self):
        for w in self.frameA.winfo_children(): w.destroy()
        self._generar()
        self._render_inv([])
        self._set_text(self.txt_log, "")
        self._set_text(self.txt_ver, "")
        self._scroll_top()

    def _generar(self):
        for w in self.frameA.winfo_children(): w.destroy()
        n = max(1, int(self.var_n.get()))
        self.ent_A: List[List[tk.Entry]] = []
        for i in range(n):
            row_e: List[tk.Entry] = []
            for j in range(n):
                e = tk.Entry(self.frameA, width=7, justify="center", font=("Consolas", 11))
                e.grid(row=i, column=j, padx=4, pady=4)
                e.insert(0, "0")
                row_e.append(e)
            self.ent_A.append(row_e)
        self._render_inv([])

    def _ejemplo(self):
        self.var_n.set(3); self._generar()
        A = [["1", "-1", "-1"],
             ["0", "3", "-1/2"],
             ["1", "2", "1"]]
        for i in range(3):
            for j in range(3):
                self.ent_A[i][j].delete(0, "end")
                self.ent_A[i][j].insert(0, A[i][j])

    def _leer_A(self) -> List[List[Number]]:
        n = len(self.ent_A)
        use_frac = self.var_frac.get()
        M: List[List[Number]] = []
        for i in range(n):
            row: List[Number] = []
            for j in range(n):
                t = self.ent_A[i][j].get().strip()
                if t == "":
                    t = "0"
                row.append(Fraction(t) if use_frac else float(t))
            M.append(row)
        return M

    def _calcular(self):
        try:
            A = self._leer_A()
        except Exception as e:
            messagebox.showerror("Entrada inválida", f"Revisa los valores: {e}")
            return
        inv, logs, _aug = inverse_with_logs(A, use_tol_for_float=not self.var_frac.get())
        if inv is None:
            self._render_inv([])
            self._set_text(self.txt_log, "\n".join(logs) + "\n\nConclusión: la matriz NO es invertible.")
            self._set_text(self.txt_ver, "")
            self._scroll_top()
            return
        self._render_inv(inv)
        self._set_text(self.txt_log, "\n".join(logs))
        self._set_text(self.txt_ver, "Aún no verificado. Presione “Verificar A×A⁻¹”.")
        self._scroll_top()

    def _verificar(self):
        try:
            A = self._leer_A()
        except Exception as e:
            messagebox.showerror("Entrada inválida", f"Revisa los valores: {e}")
            return
        vals = [self.tbl_inv.item(iid, "values") for iid in self.tbl_inv.get_children()]
        if not vals:
            messagebox.showinfo("Verificar", "Primero calcule A⁻¹.")
            return
        # reconstruir Ainv desde tabla
        Ainv: List[List[Number]] = []
        use_frac = self.var_frac.get()
        for row in vals:
            Ainv.append([Fraction(x) if use_frac else float(x) for x in row])

        P = matmul(A, Ainv)
        ok = is_identity(P)
        txt = "Resultado de A × A⁻¹:\n"
        for r in P:
            txt += "[ " + "  ".join(to_str(x) for x in r) + " ]\n"
        txt += "\n✅ Verificación EXITOSA: A × A⁻¹ = I" if ok else "\n❌ No es la identidad."
        self._set_text(self.txt_ver, txt)
        self._scroll_top()

    # -------- render helpers --------
    def _render_inv(self, M: List[List[Number]]):
        for c in self.tbl_inv.get_children():
            self.tbl_inv.delete(c)
        self.tbl_inv["columns"] = ()
        if not M:
            return
        n = len(M[0])
        self.tbl_inv["columns"] = [f"c{k}" for k in range(n)]
        for k in range(n):
            self.tbl_inv.heading(f"c{k}", text=f"a{k+1}")
            self.tbl_inv.column(f"c{k}", width=80, anchor="center")
        for row in M:
            self.tbl_inv.insert("", "end", values=[to_str(x) for x in row])

    def _set_text(self, widget: tk.Text, text: str):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", text)
        widget.configure(state="disabled")


# --------------------- API pública ---------------------
def mount_inversa(parent, on_back=None):
    parent.winfo_toplevel().title("UAM — Matriz Inversa")
    view = InversaView(parent, on_back=on_back)
    view.pack(fill="both", expand=True)
    return view


# --------------------- demo directa ---------------------
if __name__ == "__main__":
    root = tk.Tk()
    try:
        root.state("zoomed")
    except Exception:
        pass
    mount_inversa(root, on_back=root.destroy)
    root.mainloop()
