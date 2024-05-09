from utils import os, subprocess, platform
def convert_file(file_path, file_name):
    """
    Converte um arquivo removendo espaços em branco e tabulações de cada linha.

    Args:
        file_path (str): Caminho do diretório onde o arquivo está localizado.
        file_name (str): Nome do arquivo a ser convertido.

    """
    # Nome do arquivo de saída
    arquivo_saida = replace_extension(file_name)

    # Abrir o arquivo de entrada para leitura
    with open(f'{file_path}{arquivo_saida}', 'r') as entrada:
        # Ler o conteúdo do arquivo
        linhas = entrada.readlines()

    # Remover espaços em branco e tabulações de cada linha
    linhas_sem_identacao = [linha.strip() for linha in linhas]

    # Juntar as linhas sem identação em uma string
    conteudo_sem_identacao = '\n'.join(linhas_sem_identacao)

    # Abrir o arquivo de saída para escrita
    with open(f'{file_path}/{arquivo_saida}', 'w') as saida:
        # Escrever o conteúdo sem identação no arquivo de saída
        saida.write(conteudo_sem_identacao)

def replace_extension(file_name):
    """
    Substitui a extensão do arquivo por '.txt'.

    Args:
        file_name (str): Nome do arquivo.

    Returns:
        str: Novo nome de arquivo com extensão .txt.

    """
    # Encontra a posição do último ponto na string
    last_dot_index = file_name.rfind('.')
    if last_dot_index != -1:
        # Substitui a extensão pelo nova extensão
        new_file_name = file_name[:last_dot_index] + ".txt"
        return new_file_name
    else:
        return file_name

def AFR_conversion(directory, file_name):
    """
    Converte um arquivo .stp em .txt usando AFR_script (Automated Feature Recognition Software).

    Args:
        directory (str): Diretório onde o arquivo .stp está localizado.
        file_name (str): Nome do arquivo .stp a ser convertido.

    Returns:
        tuple: Caminho do arquivo convertido, diretório e novo nome de arquivo.

    """
    current_path = os.getcwd()
    if platform.system() == 'Darwin':  # macOS
        script_path = os.path.join(current_path, 'AFR_script')
    # elif platform.system() == 'Linux':  # Linux
    #     script_path = os.path.join(current_path, 'AFR_script_linux')
    # elif platform.system() == 'Windows':  # Windows
    #     script_path = os.path.join(current_path, 'AFR_script_windows')
    else:
        print("Sistema operacional não suportado.")
        return

    try:
        subprocess.run([script_path, directory, file_name, current_path])
        convert_file(f'{current_path}/AFR_Output/', file_name)
        print("Arquivo convertido com sucesso!")
    except:
        print("Erro na conversão do arquivo!")
        return

    # Troca as últimas três letras de ".stp" para ".txt"
    new_file_name = replace_extension(file_name)
    directory = f'{current_path}/AFR_Output/'
    file_path = f'{directory}{new_file_name}'
    return file_path, directory, new_file_name


