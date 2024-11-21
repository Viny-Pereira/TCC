import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from building_design import BuildingDesignParameters
from AG import GeneticAlgorithm


class DesignApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Parâmetros de Design de Edifício")

        # Campos de entrada e rótulos
        self.entries = {}
        labels = [
            "Nome do arquivo de saída",
            "Número de pavimentos",
            "Distância mínima X (m)",
            "Distância mínima Y (m)",
            "Dimensão pavimento X (m)",
            "Dimensão pavimento Y (m)",
            "Altura máxima (m)",
            "Largura máxima da viga (m)",
            "Sobre-carga (Tf/m²)",
            "Carga permanente - Pavimento (Tf/m²)",
            "Carga permanente - Paredes (Tf/m²)",
            "Número de indivíduos",
            "Número para elitismo",
            "Número de gerações",
            "Taxa de cruzamento (%)",
            "Taxa de mutação (%)",
        ]

        # Criação de entradas para cada rótulo
        for idx, label in enumerate(labels):
            tk.Label(root, text=label).grid(row=idx, column=0, sticky="e")
            entry = tk.Entry(root)
            entry.grid(row=idx, column=1)
            self.entries[label] = entry

        # Botões para interações
        tk.Button(
            root,
            text="Calcular e Exibir Resumo",
            command=self.calculate_and_show_summary,
        ).grid(row=len(labels), column=0, columnspan=2)
        tk.Button(root, text="Salvar Configuração", command=self.save_parameters).grid(
            row=len(labels) + 1, column=0, columnspan=2
        )
        tk.Button(
            root, text="Carregar Configuração", command=self.load_parameters
        ).grid(row=len(labels) + 2, column=0, columnspan=2)

        # Novo botão para rodar o algoritmo genético
        tk.Button(
            root, text="Rodar Algoritmo Genético", command=self.run_genetic_algorithm
        ).grid(row=len(labels) + 3, column=0, columnspan=2)

    def validate_input(
        self,
        numpav,
        dminx,
        dminy,
        lx,
        ly,
        hmax,
        bmax,
        q,
        gpr,
        gpl,
        numind,
        elit,
        maxger,
        cruz_taxa,
        pmut,
    ):
        if (
            numpav <= 0
            or dminx <= 0
            or dminy <= 0
            or lx <= 0
            or ly <= 0
            or hmax <= 0
            or bmax <= 0
        ):
            raise ValueError("Valores de dimensões e pavimentos devem ser positivos.")
        if (
            numind <= 0
            or elit < 0
            or maxger <= 0
            or cruz_taxa < 0
            or cruz_taxa > 100
            or pmut < 0
            or pmut > 100
        ):
            raise ValueError(
                "Valores de parâmetros de otimização devem ser válidos (positivos e dentro dos intervalos corretos)."
            )

    def calculate_and_show_summary(self):
        try:
            # Capturando valores das entradas
            arqout = self.entries["Nome do arquivo de saída"].get() + ".sai"
            numpav = int(self.entries["Número de pavimentos"].get())
            dminx = float(self.entries["Distância mínima entre pilares X (m)"].get())
            dminy = float(self.entries["Distância mínima entre pilares Y (m)"].get())
            lx = float(self.entries["Dimensão pavimento X (m)"].get())
            ly = float(self.entries["Dimensão pavimento Y (m)"].get())
            hmax = float(self.entries["Altura máxima da viga (m)"].get())
            bmax = float(self.entries["Largura máxima da viga (m)"].get())
            q = float(self.entries["Sobre-carga (Tf/m²)"].get())
            gpr = float(self.entries["Carga permanente - Pavimento (Tf/m²)"].get())
            gpl = float(self.entries["Carga permanente - Paredes (Tf/m²)"].get())
            numind = int(self.entries["Número de indivíduos"].get())
            elit = int(self.entries["Número de indivíduos para elitismo"].get())
            maxger = int(self.entries["Número de gerações"].get())
            cruz_taxa = int(self.entries["Taxa de cruzamento (%)"].get())
            pmut = float(self.entries["Taxa de mutação (%)"].get())

            # Validação de entradas
            self.validate_input(
                numpav,
                dminx,
                dminy,
                lx,
                ly,
                hmax,
                bmax,
                q,
                gpr,
                gpl,
                numind,
                elit,
                maxger,
                cruz_taxa,
                pmut,
            )

            # Criando uma instância de BuildingDesignParameters
            params = BuildingDesignParameters(
                arqout,
                numpav,
                dminx,
                dminy,
                lx,
                ly,
                hmax,
                bmax,
                q,
                gpr,
                gpl,
                numind,
                elit,
                maxger,
                cruz_taxa,
                pmut,
            )
            self.params = params
            parameters_dict = params.get_parameters()
            self.parameters_dict = parameters_dict
            # Exibindo o resumo em uma janela estruturada
            self.display_summary_window(parameters_dict)

        except ValueError as e:
            messagebox.showerror(
                "Erro de Entrada",
                "Por favor, insira valores válidos para todos os campos.\n" + str(e),
            )

    def get_parameters(self):
        return self.parameters_dict

    def display_summary_window(self, parameters_dict):
        top = tk.Toplevel(self.root)
        top.title("Resumo dos Parâmetros de Design")
        tree = ttk.Treeview(
            top, columns=["Parâmetro", "Valor"], show="headings", height=20
        )
        tree.heading("Parâmetro", text="Parâmetro")
        tree.heading("Valor", text="Valor")
        tree.pack(fill=tk.BOTH, expand=True)

        for key, value in parameters_dict.items():
            tree.insert("", tk.END, values=(key, value))

    def save_parameters(self):
        try:
            parameters = {label: self.entries[label].get() for label in self.entries}
            filepath = filedialog.asksaveasfilename(
                defaultextension=".json", filetypes=[("JSON files", "*.json")]
            )
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
            messagebox.showerror(
                "Erro", f"Não foi possível carregar a configuração: {e}"
            )

    def run_genetic_algorithm(self):
        try:
            # Criando uma instância do algoritmo genético
            ga = GeneticAlgorithm(self.params)

            # Rodando o algoritmo genético
            ga.evolve()

            # Obtendo o melhor indivíduo
            best_individual, best_fitness = ga.get_best_individual()


            messagebox.showinfo(
                "Resultado do Algoritmo Genético",
                f"Melhor indivíduo: {best_individual}\nAptidão: {best_fitness:.2f}",
            )

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao rodar o algoritmo genético: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DesignApp(root)
    root.mainloop()
