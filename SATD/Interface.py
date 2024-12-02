import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from building_design import BuildingDesignParameters
from AG import GeneticAlgorithm
from ImpressaoEmArquivo import FileManager
import matplotlib.pyplot as plt  # Importa matplotlib para os gráficos
from DwgGenerator import PavementDesign, TBeamDrawingDWG


class DesignApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SATD")
        self.file_manager = FileManager()
        # Define o ícone da janela
        self.set_window_icon()

        # Campos de entrada e rótulos
        self.entries = {}
        labels = [
            "Número de pavimentos",
            "Distância mínima entre pilares X (m)",
            "Distância mínima entre pilares Y (m)",
            "Dimensão pavimento X (m)",
            "Dimensão pavimento Y (m)",
            "Altura máxima da viga (m)",
            "Largura máxima da viga (m)",
            "Sobre-carga (Tf/m²)",
            "Carga permanente - Pavimento (Tf/m²)",
            "Carga permanente - Paredes (Tf/m²)",
            "Número de indivíduos",
            "Número de indivíduos para elitismo",
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

        tk.Button(root, text="Salvar Resultados", command=self.write_file).grid(
            row=len(labels) + 4, column=0, columnspan=2
        )
        tk.Button(root, text="Mostrar Evolução", command=self.plot_evolution).grid(
            row=len(labels) + 5, column=0, columnspan=2
        )
        tk.Button(root, text="Generate DWG", command=self.generate_dwg).grid(
            row=len(labels) + 6, column=0, columnspan=2
        )

    def set_window_icon(self):
        """
        Define o ícone da janela principal usando uma imagem na pasta 'img'.
        """
        try:
            icon_path = (
                r"SATD\img\brasao_ufc_icon.png"  # Coloque o caminho do seu ícone aqui
            )
            self.icon = tk.PhotoImage(file=icon_path)
            self.root.iconphoto(True, self.icon)  # Define o ícone da janela
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar o ícone: {e}")

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
            self.params = BuildingDesignParameters(
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
            parameters_dict = self.params.get_parameters()
            self.parameters_dict = parameters_dict
            # Exibindo o resumo em uma janela estruturada
            self.display_summary_window(parameters_dict)
            self.run_genetic_algorithm()

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
            self.ga = GeneticAlgorithm(self.params)

            # Rodando o algoritmo genético
            self.ga.evolve()

            # Obtendo o melhor indivíduo
            self.best_individual, best_fitness = self.ga.get_best_individual()

            self.population = self.ga.population

            messagebox.showinfo(
                "Resultado do Algoritmo Genético",
                f"Melhor indivíduo: {self.best_individual}\nAptidão: {best_fitness:.2f}",
            )

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao rodar o algoritmo genético: {e}")

    def write_file(self):
        """
        Gerencia o processo de salvar os resultados em um arquivo.
        Chama o FileManager para escolher e salvar o arquivo.
        """
        try:
            # Organiza os dados a serem salvos
            sorted_population = self.ga.sort_population_by_fitness()

            # Counter para o índice dos indivíduos
            count = 0
            result_content = []

            for individual in sorted_population:
                count += 1
                self.ga.evaluation.initialize_individual(individual)

                # Obtém os detalhes para o indivíduo
                individual_info = self.ga.evaluation.mostrar_resultados(count)
                result_content.extend(
                    individual_info
                )  # Adiciona ao conteúdo para o arquivo

            # Chama o FileManager para salvar o arquivo
            self.file_manager.save_file(result_content)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar os resultados: {e}")

    def generate_dwg(self):
        """
        Generates DWG files for the structural design, including a labeled floor plan
        and a T-beam cross-section drawing. Uses the best individual from the genetic
        algorithm's results to initialize design parameters.

        Steps:
            1. Retrieves drawing data from the genetic algorithm's evaluation for the best individual.
            2. Generates a labeled floor plan (DXF file) with beam orientations, dimensions,
            and layout information using the `PavementDesign` class.
            3. Creates a T-beam cross-section drawing (DXF file) with dimensions and node
            information using the `TBeamDrawingDWG` class.

        Raises:
            Exception: If there is an issue during the drawing generation process.
        """
        try:
            # Initialize the best individual for evaluation
            self.ga.evaluation.initialize_individual(self.best_individual)

            # Get parameters for floor plan and T-beam drawings
            DL, NA, NB, BV, HV, HL, LP, span_x, span_y, divisions_x, divisions_y = (
                self.ga.evaluation.get_location_drawing_data()
            )
            # Ajuste de unidades
            BV = BV * 100
            HV = HV * 100
            HL = HL * 100
            LP = LP * 100
            span_x = span_x * 100
            span_y = span_y * 100
            # Generate floor plan with labels
            plant = PavementDesign(
                filename="planta_com_labels.dxf",
                beam_orientation=DL,
                beam_width=BV,
                beam_height=HV,
                pillar_size=LP,
                span_x=span_x,
                span_y=span_y,
                num_divisions_x=divisions_x,
                num_divisions_y=divisions_y,
            )
            plant.generate_drawing()

            # Generate T-beam cross-section drawing
            tbeam = TBeamDrawingDWG(BV, HL, HV, NA, NB)
            tbeam.generate_drawing()

            messagebox.showinfo("Success", "DWG files generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error generating DWG files: {e}")

    def plot_evolution(self):
        """
        Plota o gráfico da evolução das gerações com base no histórico de aptidões.
        """
        try:
            if not hasattr(self.ga, "fitness_history"):
                raise ValueError("O algoritmo genético ainda não foi executado.")
            generations = range(len(self.ga.fitness_history))
            fitness_values = self.ga.fitness_history

            plt.figure(figsize=(10, 6))
            plt.plot(generations, fitness_values, marker="o", label="Aptidão Máxima")
            plt.title("Evolução da Aptidão ao Longo das Gerações")
            plt.xlabel("Geração")
            plt.ylabel("Aptidão Máxima")
            plt.grid(True)
            plt.legend()
            plt.show()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar o gráfico: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DesignApp(root)
    root.mainloop()
