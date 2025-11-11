# WikiQuick

Script per la conversione da file CSV a comandi QuickStatements v1


## Preparazione file CSV

Quickstatements richiede la normalizzazione di alcuni valori per la corretta importazione. Per stabilire quali normalizzazioni eseguire per camp/proprietà specifici è possibile specificare nell'header la tipologia di dato.

Per esempio:

```
|       Lit       |
------------------- --> LAST|Lit|"Dante Alighieri"
| Dante Alighieri |   

|             frwiki             |
--------------------------------- --> LAST|frwiki:Temple de Chêne-Bougeries
| Temple de Ch%C3%AAne-Bougeries |   

| P21 |
------- --> LAST|P21|Q12
| Q12 |    

| P21_STR |
----------- --> LAST|P21|"Q12"
|   Q12   |    

```

Si fornisce di seguito la lista di tipi di dato disponibili:

| Tipo | Descrizione | Dato originale | Dato normalizzato |
| ---- | ----------- | -------------- | ----------------- |
| Lxx | Label | Hello world | "Hello world" |
| Dxx | Description | Hello world | "Hello world" |
| Axx | Alias | Hello world | "Hello world" |
| xxwiki | Wiki link | https://it.wikipedia.org/wiki/Dante_Alighieri | "Dante Alighieri" |
| PXX | Elemento | Q123 | Q123 |
| PXX_STR | Stringa | Q123 | "Q123" |
| PXX_NUM | Numero | 12,53 | 12.53 |
| PXX_DATE | Datastamp | 10-06-2024 | +2024-06-10T00:00:00Z/11 |
| PXX_GEO | Coordinate geografiche | 45.466944/9.19 | @45.466944/9.19 |


## Usage

Per avviare l'applicazione:

1. copiare il repository localmente ed eseguire:

```
Linux (Debian/Ubuntu)
python3 main.py

Windows
doppio click sul file

MacOS
python3 main.py
```

2. Selezionare il file CSV da processare
3. Conversione automatica
4. Alla fine del processo di aprirà l'editor di testo predefinito con il contenuto convertito
5. Copiare il contenuto e incollarlo in QuickStatements
6. Importa comandi CSV V1
7. Avvio importazione
