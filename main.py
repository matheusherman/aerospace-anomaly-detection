from utils import *

# Specify the path for ontology creation
onto, onto_path, onto_directory, onto_file_name = None, None, None, None
part_file_path, part_directory, part_file_name  = None, None, None
current_path = os.getcwd()

def main():
    """
    Função principal responsável por gerenciar a interface gráfica e as interações do usuário.

    A função cria uma janela de interface gráfica com botões para várias operações, como criar uma ontologia,
    inserir dados em uma ontologia, carregar uma ontologia existente, visualizar uma peça, converter um arquivo
    .stp em .txt, testar uma anomalia e fechar o programa.

    Cada botão está associado a uma função específica que executa a operação correspondente quando acionada.

    A função principal utiliza a biblioteca Tkinter para criar a interface gráfica e gerenciar os eventos do usuário.

    O programa continua em execução até que o usuário feche a janela da interface gráfica.

    """

    global onto

    '''
    CRIA UMA ONTOLOGIA
    '''
    def criar():
        path = f'{os.getcwd()}/AFR_Output/'
        global onto
        nome_ontologia = simpledialog.askstring("Nome da Ontologia", "Digite o nome da ontologia:")
        if nome_ontologia:
            onto = get_ontology(f'{nome_ontologia}.owl')
            messagebox.showinfo("Sucesso", f"Criando ontologia {nome_ontologia}.owl")
            create_ontology(onto, nome_ontologia)
            onto.load()
            pasta = os.listdir(path)
            for arquivos in pasta:
                file_path = f'{path}{arquivos}'
                insert_data(onto, file_path)
            onto.save(file=f'{nome_ontologia}.owl')
            messagebox.showinfo("Sucesso", f"Ontologia criada e salva como {nome_ontologia}.owl")
        else:
            messagebox.showerror("Erro", "Nenhum nome foi digitado!")

    '''
    INSERE UMA PEÇA NA ONTOLOGIA ESCOLHIDA
    '''
    def inserir():
        global onto
        if onto is None:
            messagebox.showinfo("Selecione", f"Selecione a ontologia!")
            onto_path, onto_directory, onto_name = choose_file()
            if not onto_name.endswith('.owl'):
                messagebox.showerror("Erro", "O arquivo selecionado não é um arquivo .owl!")
                return

            onto = get_ontology(f'file://{onto_path}')

        onto.load()
        messagebox.showinfo("Selecione", f"Selecione a Peça .STP que deseja inserir!")
        part_path, part_directory, part_file_name = choose_file()
        if not part_file_name.endswith('.stp') and not part_file_name.endswith('.txt'):
            messagebox.showerror("Erro", "O arquivo selecionado não é um arquivo .stp nem .txt!")
            return

        if part_file_name.endswith('.stp'):
            part_path, part_directory, part_file_name = AFR_conversion(part_directory, part_file_name)

        insert_data(onto, part_path)
        onto.save(file=f'{onto_name}')
        save_ontology(f'{onto_name}', f'Público/{onto_name}')
        messagebox.showinfo("Sucesso", f"Arquivos inseridos na ontologia e salva como {onto_name}")

    '''
    CARREGA UMA ONTOLOGIA
    '''
    def carregar_onto():
        global onto, onto_path, onto_directory, onto_file_name
        messagebox.showinfo("Selecione", f"Selecione a ontologia!")
        onto_path, onto_directory, onto_file_name = choose_file()
        if not onto_file_name.endswith('.owl'):
            messagebox.showerror("Erro", "O arquivo selecionado não é um arquivo .owl!")
            return

        onto = get_ontology(f'file://{onto_path}')
        onto.load()
        messagebox.showinfo("Sucesso", "Ontologia carregada")
        return onto_path, onto_directory, onto_file_name

    '''
    ABRE A VISUALIZAÇÃO 3D DE UMA PEÇA
    '''
    def visualizar_peca():
        open_file_dialog()

    '''
    CONVERTER O STP EM TXT
    '''
    def converter():
        global part_file_name, part_file_path, peca_directory
        messagebox.showwarning("Selecione", "Seleciona a Peça para conversão!")
        file_path, directory, file_name = choose_file()
        if not file_name.endswith('.stp'):
            messagebox.showerror("Erro", "O arquivo selecionado não é um arquivo .stp!")
            return
        part_file_path, part_directory, part_file_name = AFR_conversion(directory, file_name)
        messagebox.showinfo("Sucesso", "Peça Convertida para txt!")
        return part_file_path, part_directory, part_file_name

    '''
    SELECIONA UMA PEÇA E TESTA UMA ANOMALIA COMPARANDO COM INFORMAÇÕES DA ONTOLOGIA
    '''

    def testar():
        onto = get_ontology(f'parts.owl').load()

        file_path, file_directory, file_name = choose_file()

        if file_path.endswith('.stp'):
            file_path, file_directory, file_name = AFR_conversion(file_directory, file_name)
        elif not file_name.endswith('.txt'):
            messagebox.showerror("Erro", "O arquivo selecionado não é um arquivo .stp nem .txt!")
            return

        messagebox.showinfo("Aguarde", "Checando anomalias na peça")

        dados_peca = obter_dados_nova_peca(file_path)
        nome_peca = dados_peca.get('Part name')
        anomalias = detect_anomalies(dados_peca)

        if anomalias:
            chart_plot(anomalias, extract_data_from_ontology(onto))

            mensagem_anomalias = ""
            for classe, propriedades in anomalias.items():
                mensagem_classe = f"\nClass: {classe}\n"
                propriedades_anomalias = ""
                for propriedade, infos_anomalia in propriedades.items():
                    for info_anomalia in infos_anomalia:
                        if info_anomalia:
                            propriedades_anomalias += f" - Property: {propriedade}, Anomaly Value: {info_anomalia['value']}\n"
                if propriedades_anomalias:
                    mensagem_anomalias += mensagem_classe + propriedades_anomalias

            if mensagem_anomalias:
                messagebox.showwarning("Detected Anomalies", mensagem_anomalias)
                print(mensagem_anomalias)

                result = messagebox.askquestion("Anomalias Detectadas",
                                                "Ver opções de retrabalho?")
                if result == 'yes':
                    ver_opcoes_retrabalho(anomalias, nome_peca, file_path)

        else:
            messagebox.showinfo("Sucesso",
                                "Não foram encontradas anomalias na peça!\nSem necessidade de retrabalho, processo segue o roteiro.")
            print("Não foram encontradas anomalias.")

    def ver_opcoes_retrabalho(anomalias, nome_peca, file_path):
        onto2 = get_ontology('anomaly.owl').load()
        insert_data(onto2, file_path)
        onto2.save(file='anomaly.owl')
        sync_reasoner_pellet([onto2], infer_property_values=True)

        machine_suggestions = ""
        screw_suggestions = ""

        for classe, propriedades in anomalias.items():
            individuos_inferidos = onto2.search(type=onto2[classe])
            machine_suggestions += f"Máquina recomendada para corrigir o problema na Classe {classe}: \n"
            for individuo in individuos_inferidos:
                if individuo.hasName[0] == nome_peca:
                    for propriedade, infos_anomalia in propriedades.items():
                        valor_propriedade_individuo = getattr(individuo, propriedade)[0]
                        for info_anomalia in infos_anomalia:
                            if info_anomalia['value'] == valor_propriedade_individuo:
                                if hasattr(individuo, "recommendedMachine"):
                                    machine_suggestions += ", ".join(
                                        [machine.name for machine in individuo.recommendedMachine]) + "\n"
                                    if hasattr(individuo, "recommendedScrew") and individuo.recommendedScrew:
                                        screw_suggestions += "Parafuso recomendado para corrigir o problema: "
                                        screw_suggestions += ", ".join(
                                            [screw.name for screw in individuo.recommendedScrew]) + "\n"
                                else:
                                    machine_suggestions += f"Não foi encontrada possibilidade de retrabalho para {classe}: \n"

        suggestion_message = ""
        if machine_suggestions:
            suggestion_message += "Sugestões de Máquinas:\n\n" + machine_suggestions
        if screw_suggestions:
            suggestion_message += "\nSugestões de Parafusos:\n\n" + screw_suggestions

        if suggestion_message:
            messagebox.showinfo("Sugestões de Retrabalho", suggestion_message)
        else:
            messagebox.showinfo("Sugestões de Retrabalho", "Não foram encontradas sugestões de retrabalho.")

    '''
    ENCERRA O PROGRAMA
    '''
    def fechar_janela():
        root.destroy()

    root = tk.Tk()
    root.title("Menu")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_position = int((screen_width - 220) / 2)
    y_position = int((screen_height - 200) / 2)
    root.geometry(f"220x200+{x_position}+{y_position}")

    # Botões para cada opção
    btn_criar = tk.Button(root, text="Criar Ontologia", command=criar)
    btn_criar.pack()

    btn_carregar_onto = tk.Button(root, text="Carregar Ontologia", command=carregar_onto)
    btn_carregar_onto.pack()

    btn_visualizar_onto = tk.Button(root, text="Visualizar Peça", command=visualizar_peca)
    btn_visualizar_onto.pack()

    btn_converter_peca = tk.Button(root, text="Converter STEP para TXT", command=converter)
    btn_converter_peca.pack()

    btn_testar = tk.Button(root, text="Testar Anomalia", command=testar)
    btn_testar.pack()

    # Botão para fechar a janela
    btn_fechar = tk.Button(root, text="Fechar", command=fechar_janela)
    btn_fechar.config(bg="red")
    btn_fechar.pack()

    root.mainloop()

if __name__ == "__main__":
    main()