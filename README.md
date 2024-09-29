
# DASHBOARD DE VISUALIZAÇÃO DE DADOS

Este projeto faz parte da disciplina de **Visualização de Dados**, onde foi solicitado desenvolver um dashboard interativo utilizando **Streamlit** para análise de dados de aluguel de imóveis.

Obs: O arquivo `requirements.txt` foi adicionado neste repositório para facilitar a instalação das dependências.

## 🚀 Começando

Essas instruções permitirão que você obtenha uma cópia do projeto em operação na sua máquina local para fins de desenvolvimento e teste.

### 📋 Pré-requisitos

Para rodar o projeto, você precisará ter instalado:
- [Python](https://www.python.org/)
- [Pip](https://pip.pypa.io/en/stable/installation/)

### 🔧 Instalação

1. Clone o repositório em sua máquina local:
   ```bash
   git clone https://github.com/hedleydarsh/dasboard_streamlit.git
   ```
2. Navegue até o diretório do projeto:
   ```bash
   cd <diretorio-do-projeto/dasboard_streamlit>
   ```
3. Instale as dependências listadas no arquivo `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Executando o Dashboard

Para executar o dashboard, utilize o seguinte comando:
```bash
streamlit run dashboard.py
```

O dashboard será aberto no navegador, permitindo a exploração interativa dos dados de aluguel de imóveis.

## 📦 Documentação

A documentação técnica do projeto está incluída nos comentários do código, explicando as funcionalidades de filtragem de dados e visualização com gráficos interativos.

## 📝 Funcionalidades

- Filtros para selecionar cidades, faixa de área e valor de aluguel, permitindo personalizar a análise.
- Gráficos interativos que exibem:
  - **Quantidade de casas por cidade** (gráfico de barras)
  - **Preço médio de aluguel por quantidade de quartos e cidade** (gráfico de barras agrupadas)
  - **Média de área por cidade** (gráfico de barras)
  - **Média de aluguel por cidade** (gráfico de linha)
  - **Distribuição dos valores embutidos no aluguel por cidade** (gráfico de violino)

## 📊 Ferramentas e Bibliotecas Utilizadas

- **Python**: Linguagem principal do projeto.
- **Streamlit**: Para criar a interface web interativa.
- **Pandas**: Para manipulação e análise de dados.
- **Plotly**: Para a criação de gráficos interativos.

## 🎓 Universidade Federal do Maranhão - UFMA
### **Disciplina**: Visualização de Dados

Projeto desenvolvido como parte da **Especialização em Análise de Dados e Inteligência Artificial** da UFMA.

**Aluno**: Hedley Lima Cunha  
**Email**: hedley.ti@gmail.com
