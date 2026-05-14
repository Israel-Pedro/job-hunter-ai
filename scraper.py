import requests
from bs4 import BeautifulSoup
import pandas as pd


def buscar_vagas(palavra_chave):
    url = "https://remoteok.com/remote-dev-jobs"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    vagas = []

    # Tenta buscar vagas reais
    try:
        resposta = requests.get(url, headers=headers, timeout=10)

        if resposta.status_code == 200:
            soup = BeautifulSoup(resposta.text, "html.parser")

            for linha in soup.select("tr.job")[:20]:
                cargo_tag = linha.select_one("h2")
                empresa_tag = linha.select_one("h3")

                if not cargo_tag or not empresa_tag:
                    continue

                cargo = cargo_tag.get_text(strip=True)
                empresa = empresa_tag.get_text(strip=True)

                if palavra_chave and palavra_chave.lower() not in cargo.lower():
                    continue

                link_relativo = linha.get("data-href", "")
                link = (
                    f"https://remoteok.com{link_relativo}"
                    if link_relativo
                    else "https://remoteok.com"
                )

                vagas.append({
                    "Cargo": cargo,
                    "Empresa": empresa,
                    "Local": "Remoto",
                    "Link": link
                })
    except Exception:
        pass

    # Se não encontrou vagas reais, usa vagas de demonstração
    if not vagas:
        vagas_demo = [
            {"Cargo": "Estagiário de TI", "Empresa": "Dataprev", "Local": "Rio de Janeiro - RJ", "Link": "https://www.dataprev.gov.br"},
            {"Cargo": "Suporte de TI", "Empresa": "Doutor PC", "Local": "Rio de Janeiro - RJ", "Link": "https://www.doutorpc.com.br"},
            {"Cargo": "Analista de Dados Júnior", "Empresa": "NIP do Brasil", "Local": "Rio de Janeiro - RJ", "Link": "https://www.nipdobrasil.com.br"},
            {"Cargo": "Desenvolvedor Python Júnior", "Empresa": "Stone", "Local": "Rio de Janeiro - RJ", "Link": "https://www.stone.com.br"},
            {"Cargo": "Analista de Suporte", "Empresa": "Stefanini", "Local": "Rio de Janeiro - RJ", "Link": "https://stefanini.com"},
            {"Cargo": "Estagiário em Desenvolvimento", "Empresa": "TOTVS", "Local": "Rio de Janeiro - RJ", "Link": "https://www.totvs.com"},
            {"Cargo": "Analista de BI Júnior", "Empresa": "Globo", "Local": "Rio de Janeiro - RJ", "Link": "https://www.globo.com"},
            {"Cargo": "Cientista de Dados Júnior", "Empresa": "Petrobras", "Local": "Rio de Janeiro - RJ", "Link": "https://petrobras.com.br"},
            {"Cargo": "Desenvolvedor Java Júnior", "Empresa": "Accenture", "Local": "Rio de Janeiro - RJ", "Link": "https://www.accenture.com/br-pt"},
            {"Cargo": "Analista de Infraestrutura", "Empresa": "Capgemini", "Local": "Rio de Janeiro - RJ", "Link": "https://www.capgemini.com/br-pt"},
            {"Cargo": "Estagiário de Dados", "Empresa": "Banco do Brasil", "Local": "Rio de Janeiro - RJ", "Link": "https://www.bb.com.br"},
            {"Cargo": "Suporte Técnico", "Empresa": "Serpro", "Local": "Rio de Janeiro - RJ", "Link": "https://www.serpro.gov.br"},
            {"Cargo": "Desenvolvedor Front-End Júnior", "Empresa": "XP Inc.", "Local": "Rio de Janeiro - RJ", "Link": "https://www.xpinc.com"},
            {"Cargo": "Analista de Sistemas Júnior", "Empresa": "IBM", "Local": "Rio de Janeiro - RJ", "Link": "https://www.ibm.com/br-pt"},
            {"Cargo": "Engenheiro de Dados Júnior", "Empresa": "iFood", "Local": "Remoto", "Link": "https://www.ifood.com.br"},
            {"Cargo": "Desenvolvedor Full Stack Júnior", "Empresa": "Mercado Livre", "Local": "Remoto", "Link": "https://www.mercadolivre.com.br"},
            {"Cargo": "Estagiário em Cybersecurity", "Empresa": "Cisco", "Local": "Rio de Janeiro - RJ", "Link": "https://www.cisco.com"},
            {"Cargo": "Analista de Cloud Júnior", "Empresa": "Oracle", "Local": "Remoto", "Link": "https://www.oracle.com/br"},
            {"Cargo": "Analista de Banco de Dados", "Empresa": "Bradesco", "Local": "Rio de Janeiro - RJ", "Link": "https://banco.bradesco"},
            {"Cargo": "Estagiário em Inteligência Artificial", "Empresa": "Microsoft", "Local": "Remoto", "Link": "https://www.microsoft.com"}
        ]

        if palavra_chave:
            termo = palavra_chave.lower().strip()

            sinonimos = {
                "estágio": "estagiário",
                "estagio": "estagiário",
                "dev": "desenvolvedor",
                "infra": "infraestrutura",
                "ia": "inteligência artificial"
            }

            termo = sinonimos.get(termo, termo)

            vagas_demo = [
                vaga for vaga in vagas_demo
                if termo in vaga["Cargo"].lower()
            ]

        vagas = vagas_demo

    return pd.DataFrame(vagas)