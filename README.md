# 💼 Job Hunter AI

Aplicação em Python desenvolvida para automatizar a busca e análise de vagas de tecnologia.

## 🚀 Funcionalidades

- Busca de vagas por palavra-chave
- Busca ao pressionar Enter
- Suporte a sinônimos (ex.: estágio → estagiário)
- Web scraping com fallback de vagas realistas
- Filtros por local e empresa
- Links clicáveis
- Métricas automáticas
- Gráficos interativos
- Exportação para Excel

## 🛠️ Tecnologias Utilizadas

- Python
- Streamlit
- Pandas
- BeautifulSoup
- Requests
- OpenPyXL

## 📊 Indicadores

- Total de vagas
- Total de empresas
- Vagas remotas

## 📁 Estrutura do Projeto

job-hunter-ai/
- app.py
- scraper.py
- requirements.txt
- README.md

## ▶️ Como Executar

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py