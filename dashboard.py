import streamlit as st
import pandas as pd
import plotly.express as px

# Configurar o layout da página
st.set_page_config(
    page_title="Dashboard - Análise de Aluguel", 
    page_icon="logo.jpg",
    layout="wide"
)

# Função para carregar dados com cache
def load_data():
    df = pd.read_csv("houses_to_rent_v2.csv")
    df['animal'] = df['animal'].replace({'acept': 'Sim', 'not acept': 'Não'})
    df['city'] = df['city'].astype(str)
    return df

# Função para aplicar filtros
def apply_filters(df):
    cities = st.sidebar.multiselect(
        "Selecione as Cidades", 
        options=sorted(df["city"].unique()), 
        default=sorted(df["city"].unique())
    )
    area_min, area_max = st.sidebar.slider(
        "Selecione o intervalo de área (m²)", 
        int(df["area"].min()), int(df["area"].max()), 
        (int(df["area"].min()), int(df["area"].max()))
    )
    rent_min, rent_max = st.sidebar.slider(
        "Selecione o intervalo de aluguel (R$)", 
        int(df["rent amount (R$)"].min()), int(df["rent amount (R$)"].max()), 
        (int(df["rent amount (R$)"].min()), int(df["rent amount (R$)"].max()))
    )
    animal_filter = st.sidebar.multiselect(
        "Permitir animais de estimação?", 
        options=["Sim", "Não"], 
        default=["Sim", "Não"]
    )
    room_filter = st.sidebar.multiselect(
        "Selecione a quantidade de quartos", 
        options=sorted(df["rooms"].unique()), 
        default=sorted(df["rooms"].unique())
    )

    return df[
        (df['city'].isin(cities)) & 
        (df['area'] >= area_min) &
        (df['rent amount (R$)'] >= rent_min) &
        (df['rent amount (R$)'] <= rent_max) &
        (df['animal'].isin(animal_filter)) &
        (df['rooms'].isin(room_filter))
    ]

# Função para adicionar CSS customizado
def add_custom_css():
    st.sidebar.markdown(
        """
        <style>
        [data-testid="stWidgetLabel"] p:first-child {
            font-weight: bold !important;
            font-size: 16px !important;
            color: white !important;
        }
        [data-testid="stImage"] {
            margin-top: -100px !important;
        }
        [data-testid="stTickBarMax"], [data-testid="stTickBarMin"] {
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Função para gerar o gráfico de quantidade de casas por cidade
def plot_city_count(df_filtered):
    city_count = df_filtered['city'].value_counts().reset_index()
    city_count.columns = ['city', 'house_count']
    city_count = city_count.sort_values(by='house_count', ascending=False)
    
    fig_cities = px.bar(
        city_count, x='city', y='house_count', text='house_count', color='house_count',
        title="Quantidade de Casas por Cidade", 
        color_continuous_scale=[(0.0, '#87CEEB'), (1.0, '#6A5ACD')], 
        labels={'city': 'Cidade', 'house_count': 'Quantidade de Casas'}
    )
    fig_cities.update_traces(textposition='outside', marker_line_width=0)
    fig_cities.update_layout(
        margin=dict(l=0, r=0, t=50, b=0), 
        coloraxis_showscale=False, yaxis=dict(showticklabels=False), 
        title_font=dict(size=18, color='#333333'), 
        showlegend=False, 
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(245, 245, 245, 1)'
    )
    return fig_cities

# Função para gerar o gráfico de aluguel por quantidade de quartos e cidade
def plot_price_by_rooms_city(df_filtered):
    price_by_rooms_city = df_filtered.groupby(['rooms', 'city'])['rent amount (R$)'].mean().reset_index()
    
    fig_price_rooms_city = px.bar(
        price_by_rooms_city, 
        x='rooms', y='rent amount (R$)', color='city', barmode='group', 
        labels={'rooms': 'Quantidade de Quartos', 'rent amount (R$)': 'Aluguel Médio (R$)'}, 
        title="Preço Médio de Aluguel por Quantidade de Quartos e Cidade", 
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_price_rooms_city.update_layout(
        margin=dict(l=100, r=0, t=50, b=0), 
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(245, 245, 245, 1)', 
        xaxis_title="Quantidade de Quartos", yaxis_title="Aluguel Médio (R$)", 
        legend_title="Cidade", 
        font=dict(size=14), 
        title_font=dict(size=18, color='#333333'), 
        showlegend=True
    )
    return fig_price_rooms_city

# Função para gerar o gráfico de média de área por cidade
def plot_area_by_city(df_filtered):
    city_mean = df_filtered.groupby('city').agg({'area': 'mean'}).reset_index()
    city_mean['formatted_area'] = city_mean['area'].apply(lambda x: f'{x:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."))

    fig_area = px.bar(
        city_mean, x='area', y='city', text='formatted_area', color='area',
        color_continuous_scale=[(0.0, '#87CEEB'), (1.0, '#6A5ACD')], 
        title="Média de Área por Cidade", labels={'city': 'Cidade', 'area': 'Área Média (m²)'}
    )
    fig_area.update_traces(textposition='outside', marker_line_width=0)
    fig_area.update_layout(
        margin=dict(l=0, r=0, t=50, b=0), 
        coloraxis_showscale=False, yaxis=dict(showticklabels=True), 
        title_font=dict(size=18, color='#333333'), 
        showlegend=False, 
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(245, 245, 245, 1)'
    )
    return fig_area

# Função para gerar o gráfico de média de aluguel por cidade
def plot_rent_by_city(df_filtered):
    city_mean = df_filtered.groupby('city').agg({'rent amount (R$)': 'mean'}).reset_index()
    city_mean['formatted_rent'] = city_mean['rent amount (R$)'].apply(lambda x: f'R$ {x:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."))

    fig_rent = px.line(
        city_mean, x='city', y='rent amount (R$)', text='formatted_rent', markers=True, 
        title="Média de Aluguel por Cidade", 
        labels={'city': 'Cidade', 'rent amount (R$)': 'Aluguel Médio (R$)'}
    )
    fig_rent.update_traces(
        textposition='top center', line=dict(width=3), marker=dict(size=10, color='red')
    )
    fig_rent.update_layout(
        margin=dict(l=0, r=0, t=50, b=0), 
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(245, 245, 245, 1)', 
        xaxis_title=None, yaxis_title="Aluguel Médio (R$)", 
        title_font=dict(size=18, color='#333333'), 
        showlegend=False
    )
    return fig_rent

# Função para gerar o gráfico de pizza de proporção de animais
def plot_animal_pie(df_filtered):
    animal_proportion = df_filtered['animal'].value_counts().reset_index()
    animal_proportion.columns = ['Permissão de Animais', 'Contagem']

    fig_animal_pie = px.pie(
        animal_proportion, names='Permissão de Animais', values='Contagem', 
        title='Proporção de Casas que Aceitam Animais', 
        color_discrete_sequence=px.colors.qualitative.Pastel,
        labels={'Permissão de Animais': 'Aceita Animais?', 'Contagem': 'Contagem'},
        width=200, height=400
    )
    fig_animal_pie.update_layout(
        title_font=dict(size=18, color='#333333'), 
        paper_bgcolor='rgba(245, 245, 245, 1)', 
        margin=dict(l=0, r=0, t=50, b=0)
    )
    return fig_animal_pie

# Função para gerar o gráfico de violino para a distribuição de valores
def plot_rent_distribution(df_filtered):
    #retirar os outliers
    df_filtered = df_without_outliers = remove_outliers(df_filtered, 'total (R$)')

    
   # Gráfico de Distribuição dos Valores Embutidos no Aluguel por Cidade
    # Criar o gráfico de violin plot para mostrar a distribuição dos valores embutidos
    fig_rent_distribution = px.violin(
        df_filtered, 
        x='city', 
        y='total (R$)', 
        color='city',  # Usar as cidades para diferenciar as cores
        box=True,  # Adicionar uma caixa de estatísticas para cada cidade
        points="all",  # Mostrar todos os pontos individuais
        title="Distribuição dos Valores Embutidos no Aluguel por Cidade",
        color_discrete_sequence=px.colors.qualitative.Pastel  # Usar cores pastéis para consistência
    )

    # Ajustes no layout do gráfico
    fig_rent_distribution.update_layout(
        title_font=dict(size=18, color='#333333'),  # Destacar o título com charcoal
        paper_bgcolor='rgba(245, 245, 245, 1)',  # Fundo cinza claro (#F5F5F5)
        plot_bgcolor='rgba(0,0,0,0)',  # Remover fundo cinza
        height=400,  # Definir altura do gráfico
        margin=dict(l=0, r=0, t=50, b=0),  # Ajustar as margens
        xaxis_title="Cidade",  # Título do eixo X
        yaxis_title="Valor Embutido (R$)",  # Título do eixo Y
        showlegend=False  # Remover a legenda para simplificação
    )
    
    return fig_rent_distribution


def remove_outliers(df, column):
    # Calcular o 1º quartil (Q1) e o 3º quartil (Q3)
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    
    # Calcular o IQR
    IQR = Q3 - Q1
    
    # Definir os limites
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Filtrar o DataFrame, mantendo apenas os valores dentro dos limites
    df_filtered = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    
    return df_filtered


# Função principal para renderizar o dashboard
def main():
    # Carregar a base de dados
    df = load_data()

    # Aplicar CSS customizado
    add_custom_css()
    
    # Adicionar uma logo no topo da barra lateral
    st.sidebar.image("logo.png", use_column_width=True)

    # Aplicar filtros aos dados
    df_filtered = apply_filters(df)

    # Verificar se há dados filtrados
    if not df_filtered.empty:
        col1, col2 = st.columns(2)
        
        # Plotar os gráficos
        with col1:
            st.plotly_chart(plot_city_count(df_filtered), use_container_width=True)
        
        with col2:
            st.plotly_chart(plot_price_by_rooms_city(df_filtered), use_container_width=True)

        col2, col3, col4 = st.columns(3)
        
        with col2:
            st.plotly_chart(plot_area_by_city(df_filtered), use_container_width=True)

        with col3:
            st.plotly_chart(plot_rent_by_city(df_filtered), use_container_width=True)
        
        with col4:
            st.plotly_chart(plot_animal_pie(df_filtered), use_container_width=True)
            
        st.plotly_chart(plot_rent_distribution(df_filtered), use_container_width=True)
    else:
        st.write("Nenhum dado disponível com os filtros aplicados.")

# Executar a função principal
if __name__ == "__main__":
    main()
