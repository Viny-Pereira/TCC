import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import json

class BuildingDesignParameters:
    CONCRETE_COSTS_CML = np.array([147, 158, 171, 185])
    CONCRETE_COSTS_CPM = np.array([185, 200, 216, 233])
    STEEL_COST_PRESTRESSED = 7
    STEEL_COST_PASSIVE = 4
    
    def __init__(self, arqout, numpav, dminx, dminy, lx, ly, hmax, bmax, q, gpr, gpl,
                 numind, elit, maxger, cruz_taxa, pmut):
        self.arqout = arqout
        self.numpav = numpav
        self.dminx = dminx
        self.dminy = dminy
        self.lx = lx
        self.ly = ly
        self.hmax = hmax
        self.bmax = bmax
        self.q = q
        self.gpr = gpr
        self.gpl = gpl
        self.numind = numind
        self.elit = elit
        self.maxger = maxger
        self.cruz_taxa = cruz_taxa
        self.pmut = pmut / 100

        # Calculando parâmetros
        self.cruz = self.calculate_cruzamento(numind, cruz_taxa)
        self.nxmax = self.calculate_max_dimension(lx, dminx)
        self.nymax = self.calculate_max_dimension(ly, dminy)
        self.nvv = 5 if bmax > 0.60 else 4
        self.numgen = 21 + self.nxmax + self.nymax + self.nvv

    def calculate_cruzamento(self, numind, cruz_taxa):
        cruz = (cruz_taxa * numind) // 100
        return cruz if cruz % 2 == 0 else cruz + 1

    def calculate_max_dimension(self, dimension, dmin):
        aj = dimension / dmin
        if aj < 9:
            return 3
        elif aj >= 9:
            return 4
        return 2

    def get_parameters(self):
        """
        Retorna todos os parâmetros de entrada e valores calculados em formato de dicionário.
        """
        return {
            "arqout": self.arqout,
            "numpav": self.numpav,
            "dminx": self.dminx,
            "dminy": self.dminy,
            "lx": self.lx,
            "ly": self.ly,
            "hmax": self.hmax,
            "bmax": self.bmax,
            "q": self.q,
            "gpr": self.gpr,
            "gpl": self.gpl,
            "numind": self.numind,
            "elit": self.elit,
            "maxger": self.maxger,
            "cruz_taxa": self.cruz_taxa,
            "pmut": self.pmut,
            "cruz": self.cruz,
            "nxmax": self.nxmax,
            "nymax": self.nymax,
            "nvv": self.nvv,
            "numgen": self.numgen,
            "CONCRETE_COSTS_CML": self.CONCRETE_COSTS_CML.tolist(),
            "CONCRETE_COSTS_CPM": self.CONCRETE_COSTS_CPM.tolist(),
            "STEEL_COST_PRESTRESSED": self.STEEL_COST_PRESTRESSED,
            "STEEL_COST_PASSIVE": self.STEEL_COST_PASSIVE,
        }


class DesignApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Parâmetros de Design de Edifício")
        
        # Campos de entrada e rótulos
        self.entries = {}
        labels = [
            "Nome do arquivo de saída", "Número de pavimentos", "Distância mínima X (m)", "Distância mínima Y (m)",
            "Dimensão pavimento X (m)", "Dimensão pavimento Y (m)", "Altura máxima (m)", "Largura máxima da viga (m)",
            "Sobre-carga (Tf/m²)", "Carga permanente - Pavimento (Tf/m²)", "Carga permanente - Paredes (Tf/m²)",
            "Número de indivíduos", "Número para elitismo", "Número de gerações", "Taxa de cruzamento (%)", "Taxa de mutação (%)"
        ]
        
        # Criação de entradas para cada rótulo
        for idx, label in enumerate(labels):
            tk.Label(root, text=label).grid(row=idx, column=0, sticky="e")
            entry = tk.Entry(root)
            entry.grid(row=idx, column=1)
            self.entries[label] = entry

        # Botão para calcular e mostrar o resumo
        tk.Button(root, text="Calcular e Exibir Resumo", command=self.calculate_and_show_summary).grid(row=len(labels), column=0, columnspan=2)

        # Botão para salvar e carregar configurações
        tk.Button(root, text="Salvar Configuração", command=self.save_parameters).grid(row=len(labels) + 1, column=0, columnspan=2)
        tk.Button(root, text="Carregar Configuração", command=self.load_parameters).grid(row=len(labels) + 2, column=0, columnspan=2)

    def validate_input(self, numpav, dminx, dminy, lx, ly, hmax, bmax, q, gpr, gpl, numind, elit, maxger, cruz_taxa, pmut):
        if numpav <= 0 or dminx <= 0 or dminy <= 0 or lx <= 0 or ly <= 0 or hmax <= 0 or bmax <= 0:
            raise ValueError("Valores de dimensões e pavimentos devem ser positivos.")
        if numind <= 0 or elit < 0 or maxger <= 0 or cruz_taxa < 0 or cruz_taxa > 100 or pmut < 0 or pmut > 100:
            raise ValueError("Valores de parâmetros de otimização devem ser válidos (positivos e dentro dos intervalos corretos).")

    def calculate_and_show_summary(self):
        try:
            # Capturando valores das entradas
            arqout = self.entries["Nome do arquivo de saída"].get() + ".sai"
            numpav = int(self.entries["Número de pavimentos"].get())
            dminx = float(self.entries["Distância mínima X (m)"].get())
            dminy = float(self.entries["Distância mínima Y (m)"].get())
            lx = float(self.entries["Dimensão pavimento X (m)"].get())
            ly = float(self.entries["Dimensão pavimento Y (m)"].get())
            hmax = float(self.entries["Altura máxima (m)"].get())
            bmax = float(self.entries["Largura máxima da viga (m)"].get())
            q = float(self.entries["Sobre-carga (Tf/m²)"].get())
            gpr = float(self.entries["Carga permanente - Pavimento (Tf/m²)"].get())
            gpl = float(self.entries["Carga permanente - Paredes (Tf/m²)"].get())
            numind = int(self.entries["Número de indivíduos"].get())
            elit = int(self.entries["Número para elitismo"].get())
            maxger = int(self.entries["Número de gerações"].get())
            cruz_taxa = int(self.entries["Taxa de cruzamento (%)"].get())
            pmut = float(self.entries["Taxa de mutação (%)"].get())

            # Validação de entradas
            self.validate_input(numpav, dminx, dminy, lx, ly, hmax, bmax, q, gpr, gpl, numind, elit, maxger, cruz_taxa, pmut)
            
            # Criando uma instância de BuildingDesignParameters
            params = BuildingDesignParameters(arqout, numpav, dminx, dminy, lx, ly, hmax, bmax, q, gpr, gpl, numind, elit, maxger, cruz_taxa, pmut)
            parameters_dict = params.get_parameters()
            
            # Exibindo o resumo em uma janela estruturada
            self.display_summary_window(parameters_dict)
        
        except ValueError as e:
            messagebox.showerror("Erro de Entrada", "Por favor, insira valores válidos para todos os campos.\n" + str(e))

    def display_summary_window(self, parameters_dict):
        top = tk.Toplevel(self.root)
        top.title("Resumo dos Parâmetros de Design")
        tree = ttk.Treeview(top, columns=["Parâmetro", "Valor"], show="headings", height=20)
        tree.heading("Parâmetro", text="Parâmetro")
        tree.heading("Valor", text="Valor")
        tree.pack(fill=tk.BOTH, expand=True)

        for key, value in parameters_dict.items():
            tree.insert("", tk.END, values=(key, value))

    def save_parameters(self):
        try:
            parameters = {label: self.entries[label].get() for label in self.entries}
            filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if filepath:
                with open(filepath, "w") as f:
                    json.dump(parameters, f)
                messagebox.showinfo("Sucesso", "Configuração salva com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar a configuração: {e}")

    def load_parameters(self):
        try:
            filepath = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
            if filepath:
                with open(filepath, "r") as f:
                    parameters = json.load(f)
                for label, value in parameters.items():
                    self.entries[label].delete(0, tk.END)
                    self.entries[label].insert(0, value)
                messagebox.showinfo("Sucesso", "Configuração carregada com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar a configuração: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DesignApp(root)
    root.mainloop()
