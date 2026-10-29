import streamlit as st
import pandas as pd
import uuid
from datetime import datetime
from pathlib import Path

st.set_page_config(
    page_title="Obravnava kreditnih vlog",
    layout="wide"
)

st.title("Sistem za obravnavo kreditnih vlog")
Path("pdf_datoteke").mkdir(exist_ok=True)

if "dogodki" not in st.session_state:
    st.session_state.dogodki = []
if "zahtevki" not in st.session_state:
    st.session_state.zahtevki = []


def zapisi_dogodek(case_id, aktivnost, uporabnik, podrobnosti=""):
    dogodek = {
        "case_id": case_id,
        "activity": aktivnost,
        "user_id": uporabnik,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "details": podrobnosti
    }
    st.session_state.dogodki.append(dogodek)


st.header("Izbira uporabnika")
uporabniki = {
    "Ana Novak": "stranka",
    "Marko Kovač": "referent",
    "Petra Horvat": "vodja"
}
izbrani_uporabnik = st.selectbox(
    "Izberi uporabnika:",
    list(uporabniki.keys())
)
vloga = uporabniki[izbrani_uporabnik]

st.write(f"Prijavljeni uporabnik: **{izbrani_uporabnik}**")
st.write(f"Vloga: **{vloga}**")
st.divider()


if vloga == "stranka":
    st.header("Oddaja kreditne vloge")
    with st.form("obrazec_vloge"):
        ime = st.text_input("Ime in priimek")
        znesek = st.number_input(
            "Zahtevani znesek kredita (€)",
            min_value=1000,
            max_value=100000,
            value=10000,
            step=1000
        )
        kreditna_ocena = st.number_input(
            "Kreditna ocena",
            min_value=0,
            max_value=1000,
            value=700
        )
        pdf = st.file_uploader(
            "Priloži potrdilo o plači (PDF)",
            type=["pdf"]
        )
        oddaj = st.form_submit_button("Oddaj vlogo")

    if oddaj:
        if not ime.strip():
            st.error("Vnesi ime in priimek.")
        elif pdf is None:
            st.error("Priloži PDF dokument.")
        elif not pdf.getvalue().startswith(b"%PDF-"):
            st.error("Priložena datoteka ni prepoznana kot PDF.")
        else:
            case_id = str(uuid.uuid4())[:8].upper()

            pot = Path("pdf_datoteke") / f"{case_id}.pdf"
            pot.write_bytes(pdf.getvalue())

            zahtevek = {
                "case_id": case_id,
                "ime": ime.strip(),
                "znesek": znesek,
                "kreditna_ocena": kreditna_ocena,
                "pdf": str(pot),
                "stanje": "Oddana",
                "referent": None
            }
            st.session_state.zahtevki.append(zahtevek)

            zapisi_dogodek(
                case_id,
                "Oddaja vloge",
                izbrani_uporabnik,
                f"PDF: {pot}"
            )

            zapisi_dogodek(
                case_id,
                "Samodejno preverjanje",
                "SYSTEM",
                f"Kreditna ocena: {kreditna_ocena}"
            )

            if kreditna_ocena < 400:
                zahtevek["stanje"] = "Zavrnjena"
                zapisi_dogodek(
                    case_id,
                    "Samodejna zavrnitev",
                    "SYSTEM",
                    "Kreditna ocena je nižja od 400."
                )
                zapisi_dogodek(
                    case_id,
                    "Obvestilo stranki",
                    "SYSTEM",
                    "Vloga je bila samodejno zavrnjena."
                )
                st.warning(
                    f"Vloga {case_id} je bila samodejno zavrnjena."
                )
            else:
                zahtevek["stanje"] = "Čaka na prevzem"
                st.success(
                    f"Vloga je bila uspešno oddana! Številka vloge: {case_id}"
                )
            st.rerun()

elif vloga == "referent":
    st.header("📋 Obravnava kreditnih vlog")

    if not st.session_state.zahtevki:
        st.info("Trenutno ni oddanih vlog.")
    else:
        for zahtevek in st.session_state.zahtevki:
            st.subheader(f"Vloga {zahtevek['case_id']}")
            st.write(f"Stranka: {zahtevek['ime']}")
            st.write(f"Znesek: {zahtevek['znesek']} €")
            st.write(f"Stanje: {zahtevek['stanje']}")

            if zahtevek["stanje"] == "Čaka na prevzem":
                if st.button(
                    "Prevzemi v pregled",
                    key=f"prevzemi_{zahtevek['case_id']}"
                ):
                    zahtevek["stanje"] = "V pregledu"
                    zahtevek["referent"] = izbrani_uporabnik

                    zapisi_dogodek(
                        zahtevek["case_id"],
                        "Prevzem v pregled",
                        izbrani_uporabnik
                    )
                    st.rerun()

            elif (
                zahtevek["stanje"] == "V pregledu"
                and zahtevek["referent"] == izbrani_uporabnik
            ):
                if st.button(
                    "Preglej vlogo",
                    key=f"preglej_{zahtevek['case_id']}"
                ):
                    zapisi_dogodek(
                        zahtevek["case_id"],
                        "Pregled vloge",
                        izbrani_uporabnik
                    )

                    zahtevek["stanje"] = "Pregledana"
                    st.rerun()

            elif (
                zahtevek["stanje"] == "Pregledana"
                and zahtevek["referent"] == izbrani_uporabnik
            ):

                if zahtevek["znesek"] <= 20000:
                    if st.button(
                        "Odobri kredit",
                        key=f"odobri_{zahtevek['case_id']}"
                    ):
                        zahtevek["stanje"] = "Odobrena"

                        zapisi_dogodek(
                            zahtevek["case_id"],
                            "Odobritev kredita",
                            izbrani_uporabnik
                        )

                        zapisi_dogodek(
                            zahtevek["case_id"],
                            "Obvestilo stranki",
                            "SYSTEM",
                            "Kredit je odobren."
                        )

                        zahtevek["stanje"] = "Zaključena"
                        zapisi_dogodek(
                            zahtevek["case_id"],
                            "Zaključek primera",
                            "SYSTEM"
                        )

                        st.success("Kredit je odobren.")
                        st.rerun()

                    if st.button(
                        "Zavrni kredit",
                        key=f"zavrni_{zahtevek['case_id']}"
                    ):
                        zahtevek["stanje"] = "Zavrnjena"

                        zapisi_dogodek(
                            zahtevek["case_id"],
                            "Zavrnitev kredita",
                            izbrani_uporabnik
                        )

                        zapisi_dogodek(
                            zahtevek["case_id"],
                            "Obvestilo stranki",
                            "SYSTEM",
                            "Kredit je zavrnjen."
                        )

                        zapisi_dogodek(
                            zahtevek["case_id"],
                            "Zaključek primera",
                            "SYSTEM"
                        )

                        st.rerun()
                else:
                    st.info(
                        "Vloga presega pooblastila referenta. "
                        "Potrebna je eskalacija k vodji."
                    )

            st.divider()


elif vloga == "vodja":
    st.header("Pregled primerov")
    for zahtevek in st.session_state.zahtevki:
        st.write(
            f"**{zahtevek['case_id']}** | "
            f"{zahtevek['ime']} | "
            f"{zahtevek['znesek']} € | "
            f"{zahtevek['stanje']}"
        )

st.divider()
st.header("Dnevnik dogodkov")

if st.session_state.dogodki:
    df = pd.DataFrame(st.session_state.dogodki)
    st.dataframe(df, use_container_width=True)
    csv = (
        df.sort_values(["case_id", "timestamp"])
        .to_csv(index=False)
        .encode("utf-8-sig")
    )
    st.download_button(
        label="Izvozi dnevnik v CSV",
        data=csv,
        file_name="dnevnik_dogodkov.csv",
        mime="text/csv"
    )
else:
    st.info("Dnevnik dogodkov je trenutno prazen.")