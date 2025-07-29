**Thesis Title:** Interoperable System for Anomaly Detection in Manufacturing Processes in the Aerospace Industry Using Machine Learning

**Author:** Matheus Herman

**Summary:**

This repository contains the source code, data, and other materials required to run the software.

**Repository Structure:**

* `README.md`: This file
* `stp_files`: Folder containing the STP files for conversion
* `AFR_output`: Folder containing the converted TXT files
* `AFR_Script`: C++ script for .STP → .TXT conversion
* `KNN.py`: Code for model training and anomaly detection
* `conversor.py`: Script to call the data conversion functions (STP → TXT)
* `extract_and_insert.py`: Functions for extracting and inserting data into the ontology
* `utils.py`: Common utility functions for the software
* `dev_TCC.owl`: OWL ontology containing geometric features of the parts
* `main.py`: Main script for running the software, including the user interface

**How to Use:**

To use this repository, follow these steps:

* Clone the repository to your computer:

```
git clone https://github.com/matheusherman/TCC.git
```

* Install the dependencies:

```
pip install -r requirements.txt
```

* Run the main script:

```
python3 main.py
```
