from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox


class FileManager:
    def __init__(self):
        pass

    def save_file(self, content):
        """
        Abre um diálogo para o usuário escolher onde salvar o arquivo e grava o conteúdo nele.
        """
        try:
            # Abre o diálogo para salvar o arquivo
            file_path = asksaveasfilename(
                title="Salvar Arquivo",
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            )

            if not file_path:
                return  # O usuário cancelou a operação

            # Salva o conteúdo no arquivo escolhido
            with open(file_path, "w", encoding="utf-8") as file:
                file.writelines(content)

            # Mensagem de sucesso
            messagebox.showinfo("Sucesso", f"Arquivo salvo com sucesso em {file_path}")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar o arquivo: {e}")
