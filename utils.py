'''
Instalar Dependências
'''
from owlready2 import *
import owlready2 as owl
from pyod.models.knn import KNN
import json
import re
import os
import platform
import numpy as np
import pickle
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.gp import gp_Ax1, gp_Pnt, gp_Dir
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Display.SimpleGui import init_display
from ftplib import FTP
from conversor import *
from KNN import *
from extract_and_insert import insert_data

pattern_web = re.compile(r'web \(ID: (\d+); Position point:\(([^,]+),([^,]+),([^)]+)\); Position normal:\(([^,]+),([^,]+),([^)]+)\)')
pattern_corner = re.compile(r'corner \(ID: (\d+); Parent ID: (\d+); Radius: ([^ ]+) mm\)')
pattern_lightening_hole = re.compile(r'lightening hole \(ID: (\d+); Parent ID: (\d+); Outer diameter: ([^ ]+) mm; Clearance diameter: ([^ ]+) mm; Height: ([^ ]+) mm; Angle: ([^ ]+) degree; Bend radius: ([^ ]+) mm; Position point:\(([^,]+),([^,]+),([^)]+)\); Position normal:\(([^,]+),([^,]+),([^)]+)\)')
pattern_tooling_hole = re.compile(r'tooling hole \(ID: (\d+); Parent ID: (\d+); Diameter: ([^ ]+) mm; Position point:\(([^,]+),([^,]+),([^)]+)\); Position normal:\(([^,]+),([^,]+),([^)]+)\)')
pattern_attachment_hole = re.compile(r'attachment hole \(ID: (\d+); Parent ID: (\d+); Diameter: ([^ ]+) mm; Position point:\(([^,]+),([^,]+),([^)]+)\); Position normal:\(([^,]+),([^,]+),([^)]+)\)')
pattern_attachment_flange = re.compile(r'attachment flange \(ID: (\d+); Parent ID: (\d+); Width: ([^ ]+) mm; Length: ([^ ]+) mm; Bend radius: ([^ ]+) mm; Type: (.*?); Position point:\(([^,]+),([^,]+),([^)]+)\); Position normal:\(([^,]+),([^,]+),([^)]+)\)', re.DOTALL)
pattern_stiffening_flange = re.compile(r'stiffening flange \(ID: (\d+); Parent ID: (\d+); Width: ([^ ]+) mm; Length: ([^ ]+) mm; Bend radius: ([^ ]+) mm; Type: (.*?); Position point:\(([^,]+),([^,]+),([^)]+)\); Position normal:\(([^,]+),([^,]+),([^)]+)\)', re.DOTALL)
pattern_deformed_flange = re.compile(r'deformed flange \(ID: (\d+); Parent ID: (\d+); Deformation length: ([^ ]+) mm\)')
pattern_deformed_flange2 = re.compile(r'deformed flange \(ID: (\d+); Parent ID: (\d+)\)')
pattern_joggle = re.compile(r'joggle \(ID: (\d+); Parent ID: (\d+); Runout: ([^ ]+) mm; Runout Direction:\(([^,]+),([^,]+),([^)]+)\); Depth: ([^ ]+) mm; Depth Direction:\(([^,]+),([^,]+),([^)]+)\); Bend radius 1: ([^ ]+) mm; Bend radius 2: ([^ ]+) mm; Type: (.*?)\)', re.DOTALL)
pattern_twin_joggle = re.compile(r'twin joggle \(ID: (\d+); Parent ID: (\d+); Runout: ([^ ]+) mm; Runout Direction:\(([^,]+),([^,]+),([^)]+)\); Depth: ([^ ]+) mm; Depth Direction:\(([^,]+),([^,]+),([^)]+)\); Bend radius 1: 3 mm; Bend radius 2: 3 mm; Type: (.*?)\)', re.DOTALL)
pattern_bend_relief = re.compile(r'bend relief \(ID: (\d+); Parents IDs: (\d+),(\d+) ; Radius: ([^ ]+) mm\)')
pattern_stringer_cutout = re.compile(r'stringer cutout \(ID: (\d+); Parent ID: (\d+); Profile: \(([^,]+),([^,]+),([^)]+)\)\(([^,]+),([^,]+),([^)]+)\)\(([^,]+),([^,]+),([^)]+)\)\(([^,]+),([^,]+),([^)]+)\)\(([^,]+),([^,]+),([^)]+)\)\(([^,]+),([^,]+),([^)]+)\)\)\n')
pattern_cutout = re.compile(r'cutout \(ID: (\d+); Parent ID: (\d+); Profile: \(([^,]+),([^,]+),([^)]+)\)\(([^,]+),([^,]+),([^)]+)\)\(([^,]+),([^,]+),([^)]+)\)\(([^,]+),([^,]+),([^)]+)\)\(([^,]+),([^,]+),([^)]+)\)\(([^,]+),([^,]+),([^)]+)\)\)')
pattern_bead = re.compile(r'bead \(ID: (\d+); Parent ID: (\d+); Width: ([^ ]+) mm; Depth: ([^ ]+) mm\)')
pattern_lip = re.compile(r'lip \(ID: (\d+); Parent ID: (\d+); Width: ([^ ]+) mm; Length: ([^ ]+) mm\)')



def load_step_file(filename):
    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(filename)
    if status == 0:  # Check se a leitura do arquivo teve sucesso
        messagebox.showerror("Erro",  "Não foi possível ler o arquivo .stp")
        return None
    step_reader.TransferRoots()
    return step_reader

def open_file_dialog():
    file_path = filedialog.askopenfilename()
    if file_path:
        messagebox.showinfo('Sucesso', 'Arquivo selecionado')
        step_reader = load_step_file(file_path)
        if step_reader:
            display, start_display, add_menu, add_function_to_menu = init_display()

            for i in range(step_reader.NbShapes()):
                shape = step_reader.Shape(i + 1)
                display.DisplayShape(shape)

            display.FitAll()
            display.ZoomFactor(1)

            # Exibe a cena
            start_display()
    else:
        messagebox.showerror("Erro", "Nenhum arquivo selecionado.")

def extract_data_from_ontology(onto):
    """
    Extrai dados de uma ontologia e os retorna em um formato estruturado.

    Args:
        onto: Ontologia da qual os dados serão extraídos.

    Returns:
        dict: Dados extraídos da ontologia em um formato estruturado.
    """

    onto.load()
    prop_values_dict = {}

    for classe in onto.classes():
        if not list(classe.instances()):
            continue
        prop_values_dict[classe.name] = {}

        for individual in classe.instances():
            for prop in individual.get_properties():
                prop_value = getattr(individual, prop.python_name)
                if prop.python_name not in prop_values_dict[classe.name]:
                    prop_values_dict[classe.name][prop.python_name] = []
                prop_values_dict[classe.name][prop.python_name].append(prop_value)

    return prop_values_dict

def obter_dados_nova_peca(part_file_path):
    dados_peca = {
        'Web': [],
        'Corner': [],
        'Lightening_Hole': [],
        'Tooling_Hole': [],
        'Attachment_Hole': [],
        'Attachment_Flange': [],
        'Stiffening_Flange': [],
        'Deformed_Flange': [],
        'Joggle': [],
        'Twin_Joggle': [],
        'Bend_Relief': [],
        'Stringer_Cutout': [],
        'Cutout': [],
        'Bead': [],
        'Lip': []
    }

    with open(part_file_path, 'r') as file:
        lines = file.readlines()

        for line in lines:

            if line.startswith('Part name'):
                name = re.compile(r'Part name: (.+)').match(line).group(1)
                dados_peca['Part name'] = name

            elif re.match(pattern_web, line):
                match = re.match(pattern_web, line)
                data = match.groups()
                dados_peca['Web'].append({
                    'hasID': int(data[0]),
                    'hasPosition_Point_X': float(data[1]),
                    'hasPosition_Point_Y': float(data[2]),
                    'hasPosition_Point_Z': float(data[3]),
                    'hasPosition_Normal_X': float(data[4]),
                    'hasPosition_Normal_Y': float(data[5]),
                    'hasPosition_Normal_Z': float(data[6])
                })

            elif re.match(pattern_corner, line):
                match = re.match(pattern_corner, line)
                data = match.groups()
                dados_peca['Corner'].append({
                    'hasID': int(data[0]),
                    'hasParentID': int(data[1]),
                    'hasRadius': float(data[2])
                })

            elif re.match(pattern_lightening_hole, line):
                match = re.match(pattern_lightening_hole, line)
                data = match.groups()
                dados_peca['Lightening_Hole'].append({
                    'hasID': int(data[0]),
                    'hasParentID': int(data[1]),
                    'hasOuter_Diameter': float(data[2]),
                    'hasClearance_Diameter': float(data[3]),
                    'hasHeight': float(data[4]),
                    'hasAngle': float(data[5]),
                    'hasBend_Radius': float(data[6]),
                    'hasPosition_Point_X': float(data[7]),
                    'hasPosition_Point_Y': float(data[8]),
                    'hasPosition_Point_Z': float(data[9]),
                    'hasPosition_Normal_X': float(data[10]),
                    'hasPosition_Normal_Y': float(data[11]),
                    'hasPosition_Normal_Z': float(data[12])
                })

            elif re.match(pattern_tooling_hole, line):
                match = re.match(pattern_tooling_hole, line)
                data = match.groups()
                dados_peca['Tooling_Hole'].append({
                    'hasID': int(data[0]),
                    'hasParentID': int(data[1]),
                    'hasDiameter': float(data[2]),
                    'hasPosition_Point_X': float(data[3]),
                    'hasPosition_Point_Y': float(data[4]),
                    'hasPosition_Point_Z': float(data[5]),
                    'hasPosition_Normal_X': float(data[6]),
                    'hasPosition_Normal_Y': float(data[7]),
                    'hasPosition_Normal_Z': float(data[8])
                })

            elif re.match(pattern_attachment_hole, line):
                match = re.match(pattern_attachment_hole, line)
                data = match.groups()
                dados_peca['Attachment_Hole'].append({
                    'hasID': int(data[0]),
                    'hasParentID': int(data[1]),
                    'hasDiameter': float(data[2]),
                    'hasPosition_Point_X': float(data[3]),
                    'hasPosition_Point_Y': float(data[4]),
                    'hasPosition_Point_Z': float(data[5]),
                    'hasPosition_Normal_X': float(data[6]),
                    'hasPosition_Normal_Y': float(data[7]),
                    'hasPosition_Normal_Z': float(data[8])
                })

            elif re.match(pattern_attachment_flange, line):
                match = re.match(pattern_attachment_flange, line)
                data = match.groups()
                dados_peca['Attachment_Flange'].append({
                    'hasID': int(data[0]),
                    'hasParentID': int(data[1]),
                    'hasWidth': float(data[2]),
                    'hasLength': float(data[3]),
                    'hasBend_Radius': float(data[4]),
                    'hasType': str(data[5]),
                    'hasPosition_Point_X': float(data[6]),
                    'hasPosition_Point_Y': float(data[7]),
                    'hasPosition_Point_Z': float(data[8]),
                    'hasPosition_Normal_X': float(data[9]),
                    'hasPosition_Normal_Y': float(data[10]),
                    'hasPosition_Normal_Z': float(data[11])
                })

            elif re.match(pattern_stiffening_flange, line):
                match = re.match(pattern_stiffening_flange, line)
                data = match.groups()
                dados_peca['Stiffening_Flange'].append({
                    'hasID': int(data[0]),
                    'hasParentID': int(data[1]),
                    'hasWidth': float(data[2]),
                    'hasLength': float(data[3]),
                    'hasBend_Radius': float(data[4]),
                    'hasType': str(data[5]),
                    'hasPosition_Point_X': float(data[6]),
                    'hasPosition_Point_Y': float(data[7]),
                    'hasPosition_Point_Z': float(data[8]),
                    'hasPosition_Normal_X': float(data[9]),
                    'hasPosition_Normal_Y': float(data[10]),
                    'hasPosition_Normal_Z': float(data[11])
                })

            elif re.match(pattern_deformed_flange, line):
                match = re.match(pattern_deformed_flange, line)
                if match:
                    data = match.groups()
                    last_deformation_length = float(data[2])
                    dados_peca['Deformed_Flange'].append({
                        'hasID': int(data[0]),
                        'hasParentID': int(data[1]),
                        'hasDeformation_length': float(data[2])
                    })
                else:
                    match = re.match(pattern_deformed_flange2, line)
                    data = match.groups()
                    dados_peca['Deformed_Flange'].append({
                        'hasID': int(data[0]),
                        'hasParentID': int(data[1]),
                        'hasDeformation_length': last_deformation_length
                    })

            elif re.match(pattern_joggle, line):
                match = re.match(pattern_joggle, line)
                data = match.groups()
                dados_peca['Joggle'].append({
                    'hasID': int(data[0]),
                    'hasParentID': int(data[1]),
                    'hasRunout': float(data[2]),
                    'hasRunout_Direction_X': float(data[3]),
                    'hasRunout_Direction_Y': float(data[4]),
                    'hasRunout_Direction_Z': float(data[5]),
                    'hasDepth': float(data[6]),
                    'hasDepth_Direction_X': float(data[7]),
                    'hasDepth_Direction_Y': float(data[8]),
                    'hasDepth_Direction_Z': float(data[9]),
                    'hasBend_Radius_1': float(data[10]),
                    'hasBend_Radius_2': float(data[11]),
                    'hasType': str(data[12])
                })

            elif re.match(pattern_twin_joggle, line):
                match = re.match(pattern_twin_joggle, line)
                data = match.groups()
                dados_peca['Twin_Joggle'].append({
                    'hasID': int(data[0]),
                    'hasParentID': int(data[1]),
                    'hasRunout': float(data[2]),
                    'hasRunout_Direction_X': float(data[3]),
                    'hasRunout_Direction_Y': float(data[4]),
                    'hasRunout_Direction_Z': float(data[5]),
                    'hasDepth': float(data[6]),
                    'hasDepth_Direction_X': float(data[7]),
                    'hasDepth_Direction_Y': float(data[8]),
                    'hasDepth_Direction_Z': float(data[9]),
                    'hasBend_Radius_1': float(data[10]),
                    'hasBend_Radius_2': float(data[11]),
                    'hasType': str(data[12])
                })

            elif re.match(pattern_bend_relief, line):
                match = re.match(pattern_bend_relief, line)
                data = match.groups()
                dados_peca['Bend_Relief'].append({
                    'hasID': int(data[0]),
                    'hasParentID': int(data[1]).split(','),  # Convert comma-separated parents to a list
                    'hasRadius': float(data[2])
                })

            elif re.match(pattern_stringer_cutout, line):
                match = re.match(pattern_stringer_cutout, line)
                data = match.groups()
                points = []
                for i in range(0, 18, 3):
                    points.append((float(data[i]), float(data[i + 1]), float(data[i + 2])))
                dados_peca['Stringer_Cutout'].append({
                    'hasID': int(data[0]),
                    'hasParentID': int(data[1]),
                    'hasProfile': points
                })

            elif re.match(pattern_cutout, line):
                match = re.match(pattern_cutout, line)
                data = match.groups()
                points = []
                for i in range(0, 18, 3):
                    points.append((float(data[i]), float(data[i + 1]), float(data[i + 2])))
                dados_peca['Cutout'].append({
                    'hasID': int(data[0]),
                    'hasParentID': int(data[1]),
                    'hasProfile': points
                })

            elif re.match(pattern_bead, line):
                match = re.match(pattern_bead, line)
                data = match.groups()
                dados_peca['Bead'].append({
                    'hasID': int(data[0]),
                    'hasParentID': int(data[1]),
                    'hasWidth': float(data[2]),
                    'hasDepth': float(data[3])
                })

            elif re.match(pattern_lip, line):
                match = re.match(pattern_lip, line)
                data = match.groups()
                dados_peca['Lip'].append({
                    'hasID': int(data[0]),
                    'hasParentID': int(data[1]),
                    'hasWidth': float(data[2]),
                    'hasLength': float(data[3])
                })

    return dados_peca


def chart_plot(anomalies, ontology_data):
    """
    Cria um Violin plot entre as anomalias detectadas e os dados da ontologia.

    Args:
        anomalies (dict): Dicionário de anomalias detectadas e seus valores para cada classe e propriedade.
        ontology_data (dict): Dados extraídos da ontologia em um formato estruturado.
    """
    root = tk.Tk()
    root.title("Gráficos")

    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)

    for class_name, prop_names in anomalies.items():
        if class_name in ontology_data:
            for prop_name, values in prop_names.items():
                if prop_name in ontology_data[class_name]:
                    ontology_values = ontology_data[class_name][prop_name]
                    if isinstance(values, list):
                        numeric_values = []
                        for value_list in ontology_values:
                            for value in value_list:
                                numeric_values.append(float(value))
                        numeric_values.append(float(values[0]['value']))

                        frame = ttk.Frame(notebook)
                        notebook.add(frame, text=f"{class_name} - {prop_name}")
                        fig, ax = plt.subplots()
                        sns.violinplot(data=numeric_values, color='lightgrey', inner="quartile", ax=ax)
                        sns.stripplot(data=numeric_values[:-1], color='blue', jitter=True, ax=ax)
                        sns.stripplot(data=[numeric_values[-1]], color='red', jitter=True, ax=ax)

                        ax.set_title(f'Distribuição de Valores para {class_name} - {prop_name}')
                        ax.set_ylabel('Valor')

                        canvas = FigureCanvasTkAgg(fig, master=frame)
                        canvas.draw()
                        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
                        toolbar = NavigationToolbar2Tk(canvas, frame)
                        toolbar.update()
                        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def choose_file():
    """
    Abre uma janela de diálogo para permitir que o usuário escolha um arquivo.
    """

    file_path = filedialog.askopenfilename()
    directory, file_name = os.path.split(file_path)
    return file_path, directory, file_name

def save_ontology(arquivo_local, caminho_remoto):
    """
    Copia a ontologia salva localmente para um servidor remoto usando FTP.

    Args:
        arquivo_local: Nome/caminho do arquivo local da ontologia (por padrão a pasta do projeto atual).
        caminho_remoto: Caminho completo do servidor remoto em questão (hard coded).
    """

    with open('config.json') as f:
        config = json.load(f)

    hostname = config['hostname']
    port = config['port']
    username = config['username']
    password = config['password']

    ftp = FTP()
    ftp.connect(hostname, port)
    ftp.login(username, password)

    print(ftp.getwelcome())
    print(ftp.pwd())

    with open(arquivo_local, 'rb') as arquivo:
        ftp.storbinary('STOR ' + f'{caminho_remoto}', arquivo)
        print(f'{caminho_remoto}/{arquivo}')

    # Fecha AFR_Output conexão FTP
    ftp.quit()

    print("Arquivo copiado com sucesso para o servidor remoto via FTP.")

def create_ontology(onto, file_name):
    """
    Cria uma nova ontologia estática a partir dos argumentos.

    Args:
        onto: Ontologia onde a estrutura será criada.
        file_name (str): Nome do arquivo para criação.
    """

    with onto:
        '''
        CLASSES
        '''

        class Product_Data(Thing):
            namespace = onto


        class Product_Features(Product_Data):
            namespace = onto


        class Base_Features(Product_Features):
            namespace = onto


        class Web(Base_Features):
            namespace = onto


        class Contact_Features(Product_Features):
            namespace = onto


        class Attachment_Flange(Contact_Features):
            namespace = onto


        class Attachment_Hole(Contact_Features):
            namespace = onto


        class Deformed_Flange(Contact_Features):
            namespace = onto


        class Deformed_Web(Contact_Features):
            namespace = onto


        class Joggle(Contact_Features):
            namespace = onto


        class Twin_Joggle(Contact_Features):
            namespace = onto


        class Part_Features(Product_Features):
            namespace = onto


        class Part_Area(Part_Features):
            namespace = onto


        class Part_Name(Part_Features):
            namespace = onto


        class Part_Perimeter(Part_Features):
            namespace = onto


        class Part_Thickness(Part_Features):
            namespace = onto


        class Part_Weight(Part_Features):
            namespace = onto


        class Refinement_Features(Product_Features):
            namespace = onto


        class Bead(Refinement_Features):
            namespace = onto


        class Bend_Relief(Refinement_Features):
            namespace = onto


        class Corner(Refinement_Features):
            namespace = onto


        class Cutout(Refinement_Features):
            namespace = onto


        class Lightening_Cutout(Refinement_Features):
            namespace = onto


        class Lightening_Hole(Refinement_Features):
            namespace = onto


        class Lip(Refinement_Features):
            namespace = onto


        class Stiffening_Flange(Refinement_Features):
            namespace = onto


        class Stringer_Cutout(Refinement_Features):
            namespace = onto


        class Tooling_Hole(Refinement_Features):
            namespace = onto


        '''
        DATA PROPERTIES
        '''


        class hasID(DataProperty):
            namespace = onto
            domain = onto.classes()
            range = [int]


        class hasParentID(DataProperty):
            namespace = onto
            range = [int]


        class hasPosition_Point_X(DataProperty):
            namespace = onto
            domain = [Web, Lightening_Hole, Tooling_Hole, Attachment_Hole, Attachment_Flange,  Stiffening_Flange]
            range = [float]


        class hasPosition_Point_Y(DataProperty):
            namespace = onto
            domain = [Web, Lightening_Hole, Tooling_Hole, Attachment_Hole, Attachment_Flange,  Stiffening_Flange]
            range = [float]


        class hasPosition_Point_Z(DataProperty):
            namespace = onto
            domain = [Web, Lightening_Hole, Tooling_Hole, Attachment_Hole, Attachment_Flange,  Stiffening_Flange]
            range = [float]


        class hasPosition_Normal_X(DataProperty):
            namespace = onto
            domain = [Web, Lightening_Hole, Tooling_Hole, Attachment_Hole, Attachment_Flange,  Stiffening_Flange]
            range = [float]


        class hasPosition_Normal_Y(DataProperty):
            namespace = onto
            domain = [Web, Lightening_Hole, Tooling_Hole, Attachment_Hole, Attachment_Flange,  Stiffening_Flange]
            range = [float]


        class hasPosition_Normal_Z(DataProperty):
            namespace = onto
            domain = [Web, Lightening_Hole, Tooling_Hole, Attachment_Hole, Attachment_Flange,  Stiffening_Flange]
            range = [float]


        class hasRunout(DataProperty):
            namespace = onto
            domain = [Joggle, Twin_Joggle]
            range = [float]


        class hasRunout_Direction_X(DataProperty):
            namespace = onto
            domain = [Joggle, Twin_Joggle]
            range = [float]


        class hasRunout_Direction_Y(DataProperty):
            namespace = onto
            domain = [Joggle, Twin_Joggle]
            range = [float]


        class hasRunout_Direction_Z(DataProperty):
            namespace = onto
            domain = [Joggle, Twin_Joggle]
            range = [float]


        class hasWidth(DataProperty):
            namespace = onto
            domain = [Attachment_Flange, Stiffening_Flange]
            range = [float]


        class hasLength(DataProperty):
            namespace = onto
            domain = [Attachment_Flange, Stiffening_Flange, Lip]
            range = [float]


        class hasHeight(DataProperty):
            namespace = onto
            domain = [Lightening_Hole]
            range = [float]


        class hasBend_Radius(DataProperty):
            namespace = onto
            domain = [Attachment_Flange, Stiffening_Flange]
            range = [float]


        class hasBend_Radius_1(DataProperty):
            namespace = onto
            domain = [Attachment_Flange, Stiffening_Flange]
            range = [float]


        class hasBend_Radius_2(DataProperty):
            namespace = onto
            domain = [Attachment_Flange, Stiffening_Flange]
            range = [float]


        class hasRadius(DataProperty):
            namespace = onto
            domain = [Corner, Bend_Relief]
            range = [float]


        class hasDiameter(DataProperty):
            namespace = onto
            domain = [Attachment_Hole, Tooling_Hole]
            range = [float]


        class hasDeformation_Length(DataProperty):
            namespace = onto
            domain = [Deformed_Flange]
            range = [float]


        class hasOuter_Diameter(DataProperty):
            namespace = onto
            domain = [Lightening_Hole]
            range = [float]


        class hasClearance_Diameter(DataProperty):
            namespace = onto
            domain = [Lightening_Hole]
            range = [float]


        class hasAngle(DataProperty):
            namespace = onto
            domain = [Lightening_Hole]
            range = [float]


        class hasType(DataProperty):
            namespace = onto
            domain = [Stiffening_Flange, Attachment_Flange, Joggle, Twin_Joggle]
            range = [str]


        class hasProfile(DataProperty):
            namespace = onto
            domain = [Stringer_Cutout, Cutout]
            range = [str]


        class hasDepth(DataProperty):
            namespace = onto
            domain = [Joggle, Twin_Joggle, Bead]
            range = [float]


        class hasDepth_Direction_X(DataProperty):
            namespace = onto
            domain = [Joggle, Twin_Joggle, Bead]
            range = [float]


        class hasDepth_Direction_Y(DataProperty):
            namespace = onto
            domain = [Joggle, Twin_Joggle, Bead]
            range = [float]


        class hasDepth_Direction_Z(DataProperty):
            namespace = onto
            domain = [Joggle, Twin_Joggle, Bead]
            range = [float]


        class hasName(DataProperty):
            namespace = onto
            range = [str]

        class hasThickness(DataProperty):
            namespace = onto
            domain = [Part_Thickness]
            range = [float]


        '''
        OBJECT PROPERTIES
        '''
        class isParentOf(ObjectProperty):
            namespace = onto
        class isChildof(ObjectProperty):
            namespace = onto

        '''
        SEMANTIC RULES
        '''
        # Regra 2: hasID(?x, 1) -> Web(?x)
        rule2 = owl.Imp()
        rule2.set_as_rule("hasID(?x, 1) -> Web(?x)")
        # Regra 1: hasParentID(?individuoA, ?childID) ^ hasID(?individuoB, ?parentID) ^ equal(?childID, ?parentID) ^ hasName(?individuoA, ?nomeA) ^ hasName(?individuoB, ?nomeB) ^ equal(?nomeA, ?nomeB) -> isParentOf(?individuoB, ?individuoA)
        rule1 = owl.Imp()
        rule1.set_as_rule(""
            "hasParentID(?individuoA, ?childID) ^ hasID(?individuoB, ?parentID) ^ equal(?childID, ?parentID) ^ hasName(?individuoA, ?nomeA) ^ hasName(?individuoB, ?nomeB) ^ equal(?nomeA, ?nomeB) -> isParentOf(?individuoB, ?individuoA)"
        "")