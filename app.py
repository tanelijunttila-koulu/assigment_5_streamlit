import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
print("App Starting")

# Ladataan csv
rovaniemi_df = pd.read_csv("https://pxdata.stat.fi/PxWeb/sq/4daf212e-aba2-45b7-b59e-edbdd11e88da", encoding="latin-1")
# luodaan uudet kolumnit vuosi ja kuukausinumero jakamalla kuukausi kolumni m:n perusteella. 
rovaniemi_df[["Vuosi", "Kuukausinumero"]] = rovaniemi_df["Kuukausi"].str.split("M", expand=True)

#näytetään dataframe
st.dataframe(rovaniemi_df)

# luodaan uusi df, jonka sisällä on käyttöaste ja kuukausi
huone_aste_df = rovaniemi_df[["Huonekäyttöaste, % Rovaniemi", "Kuukausi"]]

# piirretään graafi
st.line_chart(huone_aste_df, x="Kuukausi", y="Huonekäyttöaste, % Rovaniemi")
# Graafissa näkyy piikkejä tiettyinä kuuukausina. Ennen vuotta 1998 piikit näyttivät olevan 
# kesällä, mutta sen jälkeen piikit ovat talvella, erityisesti joulun aikaan ja juuri sen jälkeen

# valitaan vuosi ja yöpymiset rovaniemellä uudeksi df:äksi.
vuosi_df = rovaniemi_df[["Vuosi", "Yöpymiset, lkm Rovaniemi"]].groupby(by=["Vuosi"]).sum()
st.dataframe(vuosi_df)

#st.line_chart(vuosi_df, x="Vuosi", y="Huonekäyttöaste, % Rovaniemi")

# piirretään graafi
st.bar_chart(vuosi_df)
# Yöpymisten määrä on kasvanut rovaniemellä vuosien saatossa, mutta koronavuosina 2020 ja 2021
# niissä oli suuri putoaminen. Yöpymisten määrä on elpynyt ja kasvanut 
# koronavuosia edeltävään aikaan verrattuna.


# Verrataan ulkomaisia ja kotimaisia yöpymisiä.

# muunnetaan kotimaiset yöpymiset string- muodosta numeeriseen.
rovaniemi_df["Kotimaiset yöpymiset, lkm Rovaniemi"] = pd.to_numeric(rovaniemi_df["Kotimaiset yöpymiset, lkm Rovaniemi"])
# poistetaan pisteet ulkomaisista yöpymisistä.
rovaniemi_df["Ulkomaiset yöpymiset Rovaniemi"] = rovaniemi_df["Ulkomaiset yöpymiset Rovaniemi"].str.replace(".", "")
# ulkomaiset numeromuotoon.
rovaniemi_df["Ulkomaiset yöpymiset Rovaniemi"] = pd.to_numeric(rovaniemi_df["Ulkomaiset yöpymiset Rovaniemi"])
# vertailu df
ulko_vs_kot_df = rovaniemi_df[["Vuosi", "Kotimaiset yöpymiset, lkm Rovaniemi", "Ulkomaiset yöpymiset Rovaniemi"]]
# groupataan data vuosien perusteella
ulko_vs_kot_year_df = ulko_vs_kot_df.groupby(by="Vuosi").sum()
st.dataframe(ulko_vs_kot_year_df)

# piirretään graafi.
st.line_chart(ulko_vs_kot_year_df)
# rovaniemellä on melkein aina ollut enemmän ulkomaisia yöpymisiä verrattuna kotimaisiin.
# Tilanne oli toisin vain vuonna 1998 ja 1990, sekä koronavuotena 2021.

# Luodaan areachart vertaillaksemme huoneen keskihintaa ja RevPar (tulot per huone.)
# https://en.wikipedia.org/wiki/RevPAR
# Valitsin nämä araecharttiin, sillä molemmat ovat samassa yksikössä ja paremmat oli viety.
area_df = rovaniemi_df[["Vuosi", "RevPar, EUR Rovaniemi", "Huoneen keskihinta Rovaniemi"]]

# tuttua
area_df["RevPar, EUR Rovaniemi"] = area_df["RevPar, EUR Rovaniemi"].str.replace(".", "")
area_df["RevPar, EUR Rovaniemi"] = pd.to_numeric(area_df["RevPar, EUR Rovaniemi"])

area_df["Huoneen keskihinta Rovaniemi"] = area_df["Huoneen keskihinta Rovaniemi"].str.replace(".", "")
area_df["Huoneen keskihinta Rovaniemi"] = pd.to_numeric(area_df["Huoneen keskihinta Rovaniemi"])

area_df = area_df.groupby(by="Vuosi").sum()
st.area_chart(area_df, y=["RevPar, EUR Rovaniemi", "Huoneen keskihinta Rovaniemi"])
# Huoneen keskihinnan noustessa tulot per huone kasvavat myös. 
# Mielenkiintoista on, että koronavuosina huoneen keskihinta ei laskenut paljoakaan, mutta revpar laski huomattavasti.

# Uusi csv - Majoitusliikkeiden kapasiteetti kunnittain (per vuosi)
# Rajoitin hakemisen vain rovaniemeen, sillä haluan vertailla rovaniemen kapasiteettia ja käyttöä
# chartissa.
capacity_df = pd.read_csv("https://pxdata.stat.fi/PxWeb/sq/38a22205-8005-4706-91e3-7286388c06dd", encoding='latin-1')
capacity_df = capacity_df[["Vuosi", "Kaikki majoitusliikkeet Rovaniemi"]]
st.dataframe(capacity_df)
# pinta_alat_df.merge(majoitus_df, left_on="namefin", how="inner", right_on="Kunta")
comparison_df = vuosi_df.merge(capacity_df, left_on="Vuosi", right_on="Vuosi")
st.dataframe(comparison_df)
# Haluan kaksi y-akselia, sillä verrattavat lukemat ovat suuruusluokaltaan suuresti erit.
# st.line_chart ei ilmeisesti tue montaa y-akselia. (https://discuss.streamlit.io/t/2nd-y-axis-in-a-line-chart/45613)
# tämän korjaamiseksi voi käyttää joko Vega-altair paketin charttia tai matplotlibiä. Valitsin matplotlibin, koska se on tutumpi. 
# apua tähän https://discuss.streamlit.io/t/dual-axis-chart/26789
# varmistettu https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.twinx.html
fig, ax_1 = plt.subplots(1, figsize=(20,5))
# luodaan toinen y-akseli
ax_2 = ax_1.twinx()

color = 'tab:blue'

labels = comparison_df["Vuosi"]
values = comparison_df["Yöpymiset, lkm Rovaniemi"]
ax_1.bar(labels, values, color=color)
ax_1.set_xlabel('Vuosi')

color = 'tab:red'

labels_2 = comparison_df["Vuosi"]
values_2 = comparison_df["Kaikki majoitusliikkeet Rovaniemi"]
ax_2.plot(labels_2, values_2, color=color)


ax_1.set_ylabel('Yöpymiset (kpl)')
ax_2.set_ylabel('Kapasiteetti (kpl)', color=color)

plt.title("Yöpymisien määrä verrattuna yöpymiskapasiteettiin Rovaniemellä per vuosi.", y=1.10)
plt.suptitle("Rovaniemen yöpymiskapasiteetti on kasvanut vuosien aikana, samoin kysyntä. Pandemian aikana kapasiteetti ei kasvanut, mutta ei myöskään pienentynyt.", fontsize="medium", y=0.95)
# piirretään chartti
st.pyplot(fig)

# graafista näkee, että Rovaniemen yöpymiskapasiteetti on kasvanut vuosien kuluessa, 
# ja siihen on liittynyt kasvua yöpymisissä myös. Erityisesti vuonna 2015 yöpymiset ja kapasiteetti lähtivät raketinmoiseen kasvuun.
# Koronavuosina kapasiteetti pysyi samana kysynnän pienentyessä, mutta lähti kasvamaan koronan jälkeen.

# latausnappi: https://docs.streamlit.io/develop/api-reference/widgets/st.download_button

# cachetetaan csv tiedosto, jotta sitä ei generoitaisi uudestaa jokaisella rerunilla.
@st.cache_data
def convert_for_download(df):
    # muunnetaan dataframe csv tiedostoksi latin-1 enkoodauksella.
    return df.to_csv().encode("latin-1")
csv = convert_for_download(comparison_df)

# latausnappi
st.download_button(label="Lataa vertausdata", data=csv, file_name="comparison_data.csv")