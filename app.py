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

st.dataframe(rovaniemi_df)

# This is test
