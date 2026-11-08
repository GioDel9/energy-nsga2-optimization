# Energy System Optimization - BESS Sizing & Computational Intelligence

Questo repository contiene il codice sorgente e la documentazione per il progetto del corso di **Intelligenza Computazionale**, incentrato sul dimensionamento ottimale di un sistema di accumulo energetico a batteria (BESS) integrato con generazione fotovoltaica.

## 🚀 Panoramica del Progetto

Il progetto affronta il problema del dimensionamento ottimo di un sistema ibrido residenziale. L'obiettivo è minimizzare il **Costo Totale Annuo (TAC)**, inteso come il bilancio tra i costi di capitale iniziali (**CapEx**) e i costi operativi legati alla dipendenza dalla rete elettrica (**OpEx**).

Per risolvere il problema sono stati implementati e confrontati tre differenti approcci di ottimizzazione euristica:

1. **NSGA-II** (`nsga2.py`) per generare il Fronte di Pareto e identificare il *Knee Point* di compromesso (~12.40 kWh).
2. **Differential Evolution** (`de.py`) per la minimizzazione diretta del costo economico globale.
3. **Particle Swarm Optimization** (`pso.py`) per validare la stabilità e la convergenza dello sciame sullo stesso ottimo globale.

## 📂 Struttura della Cartella

```text
├── data/
│   ├── load_profile_sample.csv       # Profilo di carico residenziale
│   └── solar_generation_profile.csv  # Profilo di generazione fotovoltaica
├── src/
│   ├── __init__.py
│   ├── objectives.py                 # Funzioni obiettivo (CapEx, OpEx, TAC)
│   ├── simulator.py                  # Modello di bilancio energetico orario (8.760 ore)
│   ├── nsga2.py                      # Algoritmo NSGA-II
│   ├── de.py                         # Algoritmo Differential Evolution
│   ├── pso.py                        # Algoritmo Particle Swarm Optimization
│   ├── tuning_nsga2.py               # Script di tuning per NSGA-II
│   ├── tuning_DE.py                  # Script di tuning per Differential Evolution
│   └── tuning_PSO.py                 # Script di tuning per PSO
├── generate_data.py                  # Script di generazione e preprocessing dei dati
├── analysis.ipynb                    # Jupyter Notebook principale (Analisi e Visualizzazioni)
├── requirements.txt                  # Dipendenze Python necessarie
└── .gitignore                        # File e cartelle da escludere dal versionamento Git
```

## ⚙️ Come Eseguire il Codice

### 1. Installa le dipendenze
Assicurati di avere Python installato, quindi esegui nel terminale:
```bash
pip install -r requirements.txt
```

### 2. Genera i dati di input (se necessario)
```bash
python generate_data.py
```

### 3. Avvia l'ambiente di analisi
Apri Jupyter Notebook per eseguire l'analisi completa e visualizzare i grafici e le curve di convergenza:
```bash
jupyter notebook analysis.ipynb
```

## 🔬 Dettagli Metodologici e Risultati

* **Modellazione Energetica:** Simulazione oraria su base annuale ($8.760$ ore) per catturare la stagionalità della generazione solare e la variabilità della richiesta di carico.
* **Fronte di Pareto (NSGA-II):** Mappatura completa del trade-off tra capacità di accumulo e prelievo da rete, con individuazione geometrica del *Knee Point* a **12.40 kWh** (~€ 2,606 di costo annuo).
* **Validazione Incrociata:** Le euristiche mono-obiettivo (DE e PSO) convergono stabilmente sul medesimo ottimo economico, dimostrando l'assoluta robustezza e determinismo del modello matematico sviluppato.