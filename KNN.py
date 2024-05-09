from sklearn.model_selection import train_test_split

from utils import KNN, np, os, pickle

ignored_properties = ["hasID", "hasParentID", "hasType", "hasProfile", "hasName", "hasPosition_Point_X",
                      "hasPosition_Point_Y", "hasPosition_Point_Z", "hasPosition_Normal_X", "hasPosition_Normal_Y",
                      "hasPosition_Normal_Z"]

def train_knn_models(onto, test_size = 0.2):
    """
    Treina modelos Models para cada classe na ontologia.

    Args:
        ontology: Ontologia contendo os dados para treinamento dos modelos.
        k (int): Número de vizinhos a serem considerados no algoritmo Models. O padrão é a metade do número de indivíduos da classe.

    Returns:
        dict: Dicionário de modelos Models treinados para cada classe e propriedade.

    Esta função percorre cada classe na ontologia e cada instância dentro de cada classe,
    coletando os valores das propriedades de cada instância. Em seguida, treina um modelo
    Models para cada propriedade de cada classe, usando os valores das propriedades como dados de treinamento.
    Os modelos treinados são armazenados em um dicionário e retornados.
    """
    knn_models = {}
    K_dict = {}

    for classe in onto.classes():
        if not list(classe.instances()):
            continue
        knn_models[classe.name] = {}
        num_instances = len(list(classe.instances()))
        K_dict[classe.name] = int(num_instances/2)

        for individual in classe.instances():
            for prop in individual.get_properties():
                if prop.python_name in ignored_properties:
                    pass
                else:
                    prop_value = getattr(individual, prop.python_name)
                    if prop.python_name not in knn_models[classe.name]:
                        knn_models[classe.name][prop.python_name] = []
                    knn_models[classe.name][prop.python_name].append(prop_value)

    for class_name, prop_dict in knn_models.items():
        for prop_name, prop_values in prop_dict.items():
            try:
                X = np.array(prop_values, dtype=float).reshape(-1, 1)
                knn_model = KNN(n_neighbors=K_dict[class_name], method='median',metric='euclidean')
                knn_model.fit(X)

                directory = f'Models/{class_name}/{prop_name}/'
                if not os.path.exists(directory):
                    os.makedirs(directory)
                with open(f'{directory}knn_file', 'wb') as knnPickle:
                    pickle.dump(knn_model, knnPickle)

            except ValueError:
                continue

def detect_anomalies(new_piece):
    """
    Detecta anomalias em uma nova peça com base nos modelos Models treinados.

    Args:
        new_piece (dict): Dados da nova peça a serem analisados.
        knn_models (dict): Dicionário de modelos Models treinados.

    Returns:
        dict: Dicionário de anomalias detectadas para cada classe e propriedade.

    Esta função recebe dados de uma nova peça e os compara com os modelos Models treinados
    para detectar anomalias. Para cada classe e propriedade na nova peça, calcula a distância
    para o modelo Models correspondente. Se a distância for maior que a média das distâncias entre os outros indivíduos,
    considera-se uma anomalia e é registrada no dicionário de anomalias, que é retornado.
    """
    anomalies = {}
    for class_name, prop_values_list in new_piece.items():
        if class_name == "Part name":
            continue

        for prop_values in prop_values_list:
            for prop_name, prop_value in prop_values.items():
                if prop_name in ignored_properties:
                    continue
                try:
                    knn_model = pickle.load(open(f'Models/{class_name}/{prop_name}/knn_file', 'rb'))
                    print(knn_model)
                    predict = knn_model.predict(np.array([float(prop_value)]).reshape(1, -1))
                    if predict == 1:
                        if not class_name in anomalies:
                            anomalies[class_name] = {}
                        if not prop_name in anomalies[class_name]:
                            anomalies[class_name][prop_name] = []

                        anomalies[class_name][prop_name].append({
                            'value': float(prop_value)
                        })
                except AttributeError:
                    continue

    return anomalies