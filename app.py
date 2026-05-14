import streamlit as st
import pandas as pd
from io import BytesIO
from scraper import buscar_vagas

st.set_page_config(
    page_title="Job Hunter AI",
    page_icon="💼",
    layout="wide"
)

st.title("💼 Job Hunter AI")
st.subheader("Automação inteligente para busca de vagas de TI")


def converter_para_excel(df):
    arquivo = BytesIO()

    with pd.ExcelWriter(arquivo, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Vagas")

    arquivo.seek(0)
    return arquivo


with st.form("form_busca"):
    palavra_chave = st.text_input(
        "Digite a vaga que deseja buscar:",
        placeholder="Ex: Estágio TI, Suporte de TI, Analista de Dados"
    )

    buscar = st.form_submit_button("🔍 Buscar Vagas")


if buscar:
    dados = buscar_vagas(palavra_chave)

    if dados.empty:
        st.warning("Nenhuma vaga encontrada.")
    else:
        # Sidebar com filtros
        st.sidebar.header("🔎 Filtros")

        locais = ["Todos"] + sorted(dados["Local"].dropna().unique().tolist())
        empresas = ["Todas"] + sorted(dados["Empresa"].dropna().unique().tolist())

        filtro_local = st.sidebar.selectbox("Local", locais)
        filtro_empresa = st.sidebar.selectbox("Empresa", empresas)

        if filtro_local != "Todos":
            dados = dados[dados["Local"] == filtro_local]

        if filtro_empresa != "Todas":
            dados = dados[dados["Empresa"] == filtro_empresa]

        if dados.empty:
            st.warning("Nenhuma vaga encontrada com os filtros selecionados.")
        else:
            st.success(f"{len(dados)} vaga(s) encontrada(s).")

            # Métricas
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("📄 Total de Vagas", len(dados))

            with col2:
                st.metric("🏢 Empresas", dados["Empresa"].nunique())

            with col3:
                vagas_remotas = (
                    dados["Local"].astype(str).str.lower() == "remoto"
                ).sum()
                st.metric("🌍 Vagas Remotas", vagas_remotas)

            # Tabela
            st.dataframe(
                dados,
                use_container_width=True,
                column_config={
                    "Link": st.column_config.LinkColumn("Link da Vaga")
                }
            )

            # Gráficos
            st.subheader("📊 Análise dos Dados")

            col_graf1, col_graf2 = st.columns(2)

            with col_graf1:
                st.write("### Vagas por Empresa")
                empresas_chart = dados["Empresa"].value_counts()
                st.bar_chart(empresas_chart)

            with col_graf2:
                st.write("### Vagas por Local")
                locais_chart = dados["Local"].value_counts()
                st.bar_chart(locais_chart)

            # Download Excel
            arquivo_excel = converter_para_excel(dados)

            st.download_button(
                label="📥 Baixar Excel",
                data=arquivo_excel,
                file_name="vagas_ti.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )