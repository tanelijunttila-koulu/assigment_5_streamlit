import streamlit as st
import pandas as pd

print("App Starting")

rovaniemi_df = pd.read_csv("https://pxdata.stat.fi/PxWeb/sq/4daf212e-aba2-45b7-b59e-edbdd11e88da", encoding="latin-1")
rovaniemi_df[["Vuosi", "Kuukausinumero"]] = rovaniemi_df["Kuukausi"].str.split("M", expand=True)
st.dataframe(rovaniemi_df)

huone_aste_df = rovaniemi_df[["Huonekäyttöaste, % Rovaniemi", "Kuukausi"]]

#st.dataframe(huone_aste_df)
st.line_chart(huone_aste_df, x="Kuukausi", y="Huonekäyttöaste, % Rovaniemi")

vuosi_df = rovaniemi_df[["Vuosi", "Yöpymiset, lkm Rovaniemi"]].groupby(by=["Vuosi"]).sum()
st.dataframe(vuosi_df)
#st.line_chart(vuosi_df, x="Vuosi", y="Huonekäyttöaste, % Rovaniemi")
st.bar_chart(vuosi_df)

# This is test

# ulk vs kot
rovaniemi_df["Kotimaiset yöpymiset, lkm Rovaniemi"] = pd.to_numeric(rovaniemi_df["Kotimaiset yöpymiset, lkm Rovaniemi"])
rovaniemi_df["Ulkomaiset yöpymiset Rovaniemi"] = rovaniemi_df["Ulkomaiset yöpymiset Rovaniemi"].str.replace(".", "")
rovaniemi_df["Ulkomaiset yöpymiset Rovaniemi"] = pd.to_numeric(rovaniemi_df["Ulkomaiset yöpymiset Rovaniemi"])
ulko_vs_kot_df = rovaniemi_df[["Vuosi", "Kotimaiset yöpymiset, lkm Rovaniemi", "Ulkomaiset yöpymiset Rovaniemi"]]
ulko_vs_kot_year_df = ulko_vs_kot_df.groupby(by="Vuosi").sum()
st.dataframe(ulko_vs_kot_year_df)
st.line_chart(ulko_vs_kot_year_df)
st.text("Hello World")

area_df = rovaniemi_df[["Vuosi", "RevPar, EUR Rovaniemi", "Huoneen keskihinta Rovaniemi"]]

area_df["RevPar, EUR Rovaniemi"] = area_df["RevPar, EUR Rovaniemi"].str.replace(".", "")
area_df["RevPar, EUR Rovaniemi"] = pd.to_numeric(area_df["RevPar, EUR Rovaniemi"])

area_df["Huoneen keskihinta Rovaniemi"] = area_df["Huoneen keskihinta Rovaniemi"].str.replace(".", "")
area_df["Huoneen keskihinta Rovaniemi"] = pd.to_numeric(area_df["Huoneen keskihinta Rovaniemi"])

area_df = area_df.groupby(by="Vuosi").sum()
st.area_chart(area_df, y=["RevPar, EUR Rovaniemi", "Huoneen keskihinta Rovaniemi"])

# st.area_chart