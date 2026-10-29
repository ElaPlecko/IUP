# Naloga 4 – Sistem za obravnavo kreditnih vlog

## Opis projekta

Implementirana je spletna aplikacija s pomočjo ogrodja Streamlit in programskega jezika Python. Aplikacija simulira proces obravnave kreditnih vlog ter vodi zahtevke skozi različna stanja procesa.

Ob vsaki izvedeni aktivnosti se v dnevnik dogodkov zabeležijo podatki o dogodku, uporabniku in času izvedbe.

## Funkcionalnosti

- **Izbira uporabnika:** uporabnik izbere identiteto in vlogo – stranka, referent ali vodja. Prijava z geslom ni potrebna.
- **Oddaja kreditne vloge:** stranka vnese podatke o vlogi in priloži PDF dokument.
- **Shranjevanje dokumentov:** priloženi PDF dokument se shrani v mapo `pdf_datoteke`.
- **Samodejno preverjanje:** sistem preveri kreditno oceno. Če je ta nižja od 400, se vloga samodejno zavrne.
- **Obravnava vlog:** referent lahko prevzame vlogo, jo pregleda ter odobri ali zavrne kredit.
- **Vodenje dnevnika dogodkov:** vsaka izvedena aktivnost se zabeleži v dnevnik dogodkov.
- **Izvoz dnevnika:** dnevnik dogodkov je mogoče izvoziti v datoteko CSV, urejeno po `case_id` in `timestamp`.

## Uporabniške vloge

### Stranka
Stranka izpolni obrazec za kreditno vlogo, vnese zahtevani znesek in kreditno oceno ter priloži PDF dokument.

### Referent
Referent vidi oddane vloge, prevzame vlogo v pregled ter izvede pregled in odločitev o odobritvi ali zavrnitvi kredita.

### Vodja
Vodja lahko pregleda oddane kreditne vloge in njihova trenutna stanja.

## Dnevnik dogodkov

Dnevnik dogodkov beleži aktivnosti, ki se izvedejo med obravnavo posamezne kreditne vloge.

V trenutni implementaciji vsebuje naslednje stolpce:

- `case_id` – enolična oznaka primera.
- `activity` – ime izvedene aktivnosti.
- `user_id` – identiteta uporabnika ali sistema, ki je izvedel aktivnost.
- `timestamp` – čas izvedbe aktivnosti.
- `details` – dodatne informacije o dogodku.

Dogodki so povezani s posameznim primerom prek atributa `case_id`. Dnevnik je mogoče izvoziti v CSV, pri čemer so dogodki urejeni po `case_id` in `timestamp`.

## Uporabljene tehnologije

- Python
- Streamlit
- Pandas
- UUID za generiranje enoličnih oznak primerov

## Namestitev in zagon

### 1. Kloniranje repozitorija

```bash
git clone https://github.com/ElaPlecko/IUP.git
cd IUP
```

### 2. Ustvarjanje virtualnega okolja

```bash
python3 -m venv .venv
```

Aktivacija virtualnega okolja na macOS ali Linux:

```bash
source .venv/bin/activate
```

### 3. Namestitev knjižnic

```bash
pip install -r requirements.txt
```

### 4. Zagon aplikacije

```bash
streamlit run app.py
```

Aplikacija se odpre v spletnem brskalniku.

## Shranjevanje podatkov

PDF dokumenti se shranjujejo v mapo `pdf_datoteke`.
