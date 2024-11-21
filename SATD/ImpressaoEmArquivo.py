import os


class ArquivoSaida:
    def __init__(self, arqou):
        """
        Inicializa a classe com o nome do arquivo de saída.

        :param arqou: Nome do arquivo de saída.
        """
        self.arqou = arqou
        self.file_handler = None

    def iniciar_arq_out(self):
        """
        Inicializa o arquivo de saída, verificando se ele já existe.
        Se o arquivo já existir, pergunta ao usuário se deseja sobrescrever ou escolher um novo nome.
        """
        while True:
            if os.path.exists(self.arqou):
                resposta = (
                    input(
                        f"O arquivo '{self.arqou}' já existe. Deseja sobrescrever? (s/n): "
                    )
                    .strip()
                    .lower()
                )
                if resposta == "s":
                    try:
                        self.file_handler = open(self.arqou, "w")
                        print(f"Arquivo '{self.arqou}' foi sobrescrito com sucesso.")
                        break
                    except Exception as e:
                        print(f"Erro ao abrir o arquivo para sobrescrita: {e}")
                        break
                else:
                    self.arqou = input(
                        "Informe um novo nome para o arquivo (inclua a extensão): "
                    ).strip()
            else:
                try:
                    self.file_handler = open(self.arqou, "w")
                    print(f"Novo arquivo '{self.arqou}' foi criado com sucesso.")
                    break
                except Exception as e:
                    print(f"Erro ao criar o arquivo: {e}")
                    break

        return self.file_handler


# Exemplo de uso:
arquivo = ArquivoSaida("saida_resultados.txt")
arquivo_iniciado = arquivo.iniciar_arq_out()

# Ao terminar de escrever no arquivo, o arquivo será fechado automaticamente ao usar 'with' ou pode ser fechado manualmente:
arquivo_iniciado.close()
