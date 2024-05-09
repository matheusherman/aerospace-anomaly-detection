## README

**Título do TCC:** Sistema Interoperável para Identificação de
Anomalias em Processos de Manufatura na Indústria
Aeroespacial Usando Aprendizado de Máquina

**Autor:** Matheus Herman

**Resumo:**

Este repositório contém o código-fonte, dados e outros materiais relacionados para execução do software.

**Estrutura do Repositório:**

* `README.md`: Este arquivo
* `stp_files`: Pasta contendo os arquivos STP para conversão
* `AFR_output`: Pasta contendo os arquivos TXT convertidos
* `AFR_Script`: Script em C++ para conversão .STP -> .TXT
* `KNN.py`: Código de treinamento do modelo e detecção de anomalias
* `conversor.py`: Código para chamar as funções de conversão de dados stp -> txt
* `extract_and_insert.py`: Funções de coleta e inserção dos dados na ontologia
* `utils.py`: Funções comuns para funcionamento do software
* `dev_TCC.owl`: Ontologia OWL contendo características geométricas das peças
* `main.py`: Código fonte para execução do software, contendo a interface
  
**Como utilizar:**

Para utilizar este repositório, você deve:

* Clonar o repositório para o seu computador:

```
git clone https://github.com/matheusherman/TCC.git
```

* Instalar as dependências:
  
```
pip install -r requirements.txt
```

* Executar o main.py:
  
```
python3 main.py
```
