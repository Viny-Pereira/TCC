import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from building_design import BuildingDesignParameters
from AG import GeneticAlgorithm
from ImpressaoEmArquivo import FileManager
import matplotlib.pyplot as plt  # Importa matplotlib para os gráficos
from DwgGenerator import PavementDesign, TBeamDrawingDWG
import numpy as np


class DesignApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SATD")
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
            text="Calcular e Salvar resultados",
            command=self.calculate_and_show_summary,
        ).grid(row=len(labels), column=0, columnspan=2)
        tk.Button(root, text="Salvar Configuração", command=self.save_parameters).grid(
            row=len(labels) + 1, column=0, columnspan=2
        )
        tk.Button(
            root, text="Carregar Configuração", command=self.load_parameters
        ).grid(row=len(labels) + 2, column=0, columnspan=2)
        tk.Button(root, text="Carregar Individuo", command=self.load_individual).grid(
            row=len(labels) + 3, column=0, columnspan=2
        )

        tk.Button(root, text="Gerar desenhos", command=self.generate_dwg).grid(
            row=len(labels) + 4, column=0, columnspan=2
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
            self.run_genetic_algorithm()
            self.write_file()

        except ValueError as e:
            messagebox.showerror(
                "Erro de Entrada",
                "Por favor, insira valores válidos para todos os campos.\n" + str(e),
            )

    def get_parameters(self):
        return self.parameters_dict

    def display_best_individual(self, json_file="individuos.json"):
        """
        Carrega os dados do primeiro indivíduo de um arquivo JSON e exibe em uma interface gráfica.

        :param json_file: Caminho para o arquivo JSON contendo os indivíduos.
        """
        # Abrir e carregar o arquivo JSON
        with open(json_file, "r") as file:
            data = json.load(file)

        # Obter o primeiro indivíduo do JSON
        if data:
            first_individual = data[0]  # O primeiro indivíduo da lista
        else:
            tk.messagebox.showerror("Erro", "O arquivo JSON está vazio!")
            return

        # Criar um dicionário com as informações do primeiro indivíduo
        self.parameters_dict = {
            "Individual": first_individual.get("individual"),
            **{f"{k}": v for k, v in first_individual.get("variables", {}).items()},
            **{f"{k}": v for k, v in first_individual.get("costs", {}).items()},
            **{f"{k}": v for k, v in first_individual.get("slab_data", {}).items()},
            **{f"{k}": v for k, v in first_individual.get("beam_data", {}).items()},
        }

        # Criar uma nova janela para exibir o resumo
        top = tk.Toplevel(self.root)
        top.title("Resumo do Primeiro Indivíduo")
        tree = ttk.Treeview(
            top, columns=["Parâmetro", "Valor"], show="headings", height=20
        )
        tree.heading("Parâmetro", text="Parâmetro")
        tree.heading("Valor", text="Valor")
        tree.pack(fill=tk.BOTH, expand=True)

        # Inserir os dados do dicionário na interface
        for key, value in self.parameters_dict.items():
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

    def load_individual(self):
        """
        Abre um diálogo para o usuário selecionar um arquivo JSON contendo os indivíduos.
        Salva o caminho do arquivo para uso posterior.
        """
        try:
            # Abrir diálogo para selecionar o arquivo
            file_path = filedialog.askopenfilename(
                filetypes=[("JSON Files", "*.json")], title="Selecione o arquivo JSON"
            )
            if not file_path:
                messagebox.showinfo("Cancelado", "Operação cancelada pelo usuário.")
                return
            self.display_best_individual(file_path)

        except (json.JSONDecodeError, ValueError) as e:
            messagebox.showerror("Erro", f"Erro ao carregar o arquivo JSON: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")

    def run_genetic_algorithm(self):
        """
        Executes the genetic algorithm for optimization and displays the results.

        This function creates an instance of the `GeneticAlgorithm` class using the
        current design parameters (`self.params`), runs the optimization process,
        and retrieves the best solution and its fitness value. The results are displayed
        in a message box for the user.

        Steps:
            1. Instantiate the genetic algorithm (`GeneticAlgorithm`) with the current parameters.
            2. Run the `evolve()` method to perform the optimization.
            3. Retrieve the best individual and its fitness value using `get_best_individual()`.
            4. Store the final population for further analysis or visualization.
            5. Display the best individual's details in a message box.

        If an error occurs during the execution, an error message is displayed in a
        message box for the user.

        Exceptions:
            - Catches any exception raised during the execution of the genetic algorithm
            and displays an error message with the exception details.

        User Feedback:
            - Shows an information message with the best solution and its fitness value
            if the algorithm runs successfully.
            - Displays an error message if the algorithm encounters any issues.

        Example Usage:
            self.run_genetic_algorithm()
        """
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
        self.file_manager = FileManager()
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
            json_info_list = []

            for individual in sorted_population:
                count += 1
                self.ga.evaluation.initialize_individual(individual)

                # Obtém os detalhes para o indivíduo
                individual_info = self.ga.evaluation.display_results(count)
                result_content.extend(
                    individual_info
                )  # Adiciona ao conteúdo para o arquivo
                json_info = self.ga.evaluation.get_results_as_dict(count)
                json_info_list.append(json_info)

            # Chama o FileManager para salvar o arquivo
            self.file_manager.save_txt_file(result_content)
            self.file_manager.save_json_file(json_info_list)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar os resultados: {e}")

    def generate_dwg(self):
        """
        Generates DWG files for the structural design, including a labeled floor plan
        and a T-beam cross-section drawing. Prompts the user to choose the save location
        and filenames for the DWG files.
        """
        try:
            # Initialize the best individual for evaluation
            best_individual = self.parameters_dict["Individual"]
            best_individual = np.array(
                [int(x) for x in best_individual.strip("[]").split()]
            )
            self.ga.evaluation.initialize_individual(best_individual)

            # Get parameters for floor plan and T-beam drawings
            (
                DL,
                NA,
                NB,
                NPT,
                BV,
                HV,
                HL,
                LP,
                span_x,
                span_y,
                divisions_x,
                divisions_y,
            ) = self.ga.evaluation.get_location_drawing_data()
            # Ajuste de unidades
            BV = int(BV * 100)
            HV = int(HV * 100)
            HL = int(HL * 100)
            LP = int(LP * 100)
            span_x = span_x * 100
            span_y = span_y * 100

            # Ask user where to save the floor plan DWG
            floor_plan_path = filedialog.asksaveasfilename(
                defaultextension=".dxf",
                filetypes=[("DXF files", "*.dxf")],
                title="Save Floor Plan Drawing As",
                initialfile="floor_plan_with_labels.dxf",
            )
            if not floor_plan_path:
                messagebox.showinfo("Cancelado", "Operação de salvar cancelada.")
                return

            # Generate floor plan with labels
            plant = PavementDesign(
                filename=floor_plan_path,
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

            # Ask user where to save the T-beam cross-section DWG
            tbeam_path = filedialog.asksaveasfilename(
                defaultextension=".dxf",
                filetypes=[("DXF files", "*.dxf")],
                title="Save T-Beam Drawing As",
                initialfile="tbeam_cross_section.dxf",
            )
            if not tbeam_path:
                messagebox.showinfo("Cancelado", "Operação de salvar cancelada.")
                return

            # Generate T-beam cross-section drawing
            tbeam = TBeamDrawingDWG(BV, HL, HV, NA, NB, NPT, tbeam_path)
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
