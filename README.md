# NSGA-II Energy Optimization - Ottimizzazione di Sistemi Ibridi

Questa cartella contiene il progetto per il corso di **Intelligenza Computazionale**, incentrato sull'applicazione di algoritmi genetici multiobiettivo (**NSGA-II** tramite la libreria `DEAP`) per il dimensionamento ottimale di un sistema energetico solare-batteria.

## Contenuto della cartella

- `generate_data.py`: script per la generazione e il preprocessing dei profili energetici iniziali.
- `src/`: cartella contenente i moduli logici del progetto (`objectives.py`, `optimize.py`, `simulator.py`).
- `data/`: file di dati di input (profili di carico e generazione solare).
- `analysis.ipynb`: Jupyter Notebook principale per l'esecuzione e la visualizzazione dei risultati.
- `requirements.txt`: dipendenze Python necessarie.
- `.gitignore`: file/cartelle da escludere dal versionamento Git.

## Come eseguire il codice

1. Installa le dipendenze:
```bash
pip install -r requirements.txt
```
2. Esegui Jupyter Notebook e apri il file principale:

```bash
jupyter notebook analysis.ipynb
```

## Dettagli del Progetto

Il notebook sviluppato esegue:
- **Ottimizzazione multiobiettivo** del sistema solare-batteria tramite l'algoritmo **NSGA-II** (`DEAP`).
- **Validazione quantitativa** attraverso il calcolo dell'**Hypervolume (HV)** per misurare la convergenza e la diversità del fronte.
- **Analisi di compromesso** mediante l'individuazione geometrica del punto di "gomito" (**Knee Point**), utile per isolare la configurazione impiantistica ideale.
