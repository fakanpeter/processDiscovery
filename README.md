# processDiscovery

A `processDiscovery` repository célja a különböző forrásokból számrazó naplfófájlok tisztítása, folyamatfelfedezése, valamint az így kapott generált ábrák összehasonlítása.

## Tartalom

- `.idea/`: Projektbeállítások könyvtára.
- `CSVs/`: A nyers naplófájlokból generált tisztított adatokat tartalmazo csv fájlok.
- `input/`: Nyers naplófájlok könyvtára.
- `models/`: Generált folyamatmodellek tárolására szolgáló könyvtár.
- `camunda_log_filter.py`: Szkript a Camunda-ból származó naplófájlok tisztítására.
- `idom_log_filter.py`: Szkript az Idomsofttól kapott naplófájl tisztítására.
- `process_discovery.py`: Szkript a folyamatmodellek generálásához a szűrt naplóadatok alapján.
- `similarity_check.py`: Szkript a generált folyamatmodellek közötti hasonlóság ellenőrzésére.

## Használat

1. **Naplófájlok előkészítése**: A feldolgozandó nyers naplófájlokat az `input/` könyvtárba kell helyezni.

2. **Naplófájlok szűrése**:
   - Camunda naplók esetén `camunda_log_filter.py` szkriptet szükséges futtatni:
     ```bash
     python camunda_log_filter.py
     ```
   - Idomsoftos napló esetén az `idom_log_filter.py` szkriptet szükséges futtatni. Sokkal lassabban fut le mint a Camunda logjait tisztító program.:
     ```bash
     python idom_log_filter.py
     ```

3. **Folyamatmodellek generálása**: A tisztított naplóadatokon a folyamatbányászathoz  `process_discovery.py` szkriptet szükséges futtatni. Ezen felül a model_path változóban megadott fájllal össze is veti a program a generált ábrát, ha a compare változó igaz értéken van:
   ```bash
   python process_discovery.py

3. **Folyamatmodellek összehasonlítása**: Folyamatbányászat során generált folyamatábrák a `similarity_check.py` szkript futtatásával összehasonlíthatók a NetworkX könyvtár segítségével (gráf alapú összevetés). Mivel a gráfok túl bnagyok ahhoz, hogy belátható időn belül lefusson az algoritmus, így az edit_distance függvény timeout paraméterét változtatva másodpercekben megadható, hogy mennyi ideig fusson az algoritmus. Az idő leteltével az addigi legjobb (legkisebb) eredményt adja vissza.:
   ```bash
   python similarity_check.py ```


