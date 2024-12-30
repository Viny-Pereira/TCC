from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox
import json
import numpy as np


class FileManager:
    def __init__(self):
        self.file_path = asksaveasfilename(title="Salvar Arquivo")
        
        # Verifique se o usuário cancelou o salvamento
        if not self.file_path:
            # Se cancelar, exibe uma mensagem perguntando se tem certeza
            cancel_confirmation = messagebox.askyesno(
                "Confirmação",
                "Você tem certeza que deseja cancelar o salvamento? O arquivo não será salvo.",
            )
            if cancel_confirmation:  # Se clicar em 'Sim'
                messagebox.showinfo("Cancelado", "Operação cancelada. Nenhum arquivo foi salvo.")
                return  # Sai da função e não faz mais nada
    def is_valid_path(self):
        return bool(self.file_path)  # Verifica se o file_path não é vazio    

    def save_txt_file(self, content):
        if not self.is_valid_path():  # Se o caminho do arquivo estiver vazio, não faz nada
            messagebox.showinfo("Cancelado", "O salvamento foi cancelado.")
            return
        try:
            file_path = self.file_path if self.file_path.endswith(".txt") else f"{self.file_path}.txt"
            # Salvar o conteúdo no arquivo escolhido
            with open(file_path, "w", encoding="utf-8") as file:
                if isinstance(content, list):
                    file.writelines(content)
                else:
                    raise ValueError("Conteúdo inválido para arquivo de texto.")
            messagebox.showinfo(
                "Sucesso", f"Arquivo salvo com sucesso em {self.file_path}"
            )
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar o arquivo: {e}")

    def save_json_file(self, content):
        if not self.is_valid_path():  # Se o caminho do arquivo estiver vazio, não faz nada
            messagebox.showinfo("Cancelado", "O salvamento foi cancelado.")
            return
        try:
            file_path = self.file_path if self.file_path.endswith(".json") else f"{self.file_path}.json"
            # Abre o arquivo JSON e carrega os dados existentes, se houver
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    existing_content = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                existing_content = (
                    []
                )  # Se o arquivo não existir ou estiver vazio, inicia uma lista vazia

            # Adiciona o novo conteúdo à lista existente
            existing_content.extend(content)

            # Salva o conteúdo atualizado no arquivo JSON
            with open(file_path, "w", encoding="utf-8") as file:
                # Converte valores do tipo NumPy para tipos nativos do Python
                existing_content = self.convert_np_types(existing_content)
                json.dump(existing_content, file, indent=4)

            messagebox.showinfo(
                "Sucesso", f"Arquivo JSON salvo com sucesso em {self.file_path}"
            )
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar o arquivo: {e}")

    def convert_np_types(self, data):
        """
        Converte tipos do NumPy para tipos nativos do Python (como int, float).
        """
        if isinstance(data, dict):
            return {key: self.convert_np_types(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.convert_np_types(item) for item in data]
        elif isinstance(data, np.int32) or isinstance(data, np.int64):
            return int(data)  # Converte para int nativo do Python
        elif isinstance(data, np.float32) or isinstance(data, np.float64):
            return float(data)  # Converte para float nativo do Python
        elif isinstance(data, np.generic):
            return data.item()  # Converte tipos NumPy para tipos nativos
        else:
            return data

    def get_file_path(self):
        return self.file_path
