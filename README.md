# HOW TO ACCESS DAHSBOARD

## Setup Environment - Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
mkdir proyek_analisis_data
cd ..\submission_analisis_data\
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run steamlit app
```
streamlit run "..\submission_analisis_data\dashboard\dashboard.py"
```
