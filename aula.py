# pip install dash
# pip install pandas
# pip install openpyxl

# **************** DASHBOARD COM DASH E PLOTLY ********************

from dash import Dash, html, dcc, Output, Input
# Importação do dashboard, estrutura do html e estruturação dcc (dash core components -> componentes do dashboard)

import plotly.express as px
import pandas as pd

app = Dash(__name__)
# Ao construir um Dashboard, temos duas grandes estruturas: Layout e Callbacks
# Layout -> Tudo aquilo que você vai visualizar
# CallBacks -> Todas as funcionalidades que você vai  dar para o dash

df = pd.read_excel("Vendas.xlsx")
#  Esta linha lê o arquivo Excel chamado "Vendas.xlsx" e armazena os dados em um DataFrame do pandas chamado df.

fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
# Esta linha cria um gráfico de barras usando o Plotly Express, onde o eixo x representa os produtos, o eixo y representa as quantidades vendidas 
# e as barras são coloridas de acordo com a "ID Loja". As barras são agrupadas por "ID Loja".

opcoes = list(df['ID Loja'].unique())
# Esta linha cria uma lista contendo os valores únicos da coluna "ID Loja" do DataFrame df.

opcoes.append("Todas as Lojas")
# Esta linha adiciona a string "Todas as Lojas" ao final da lista opcoes.
# A lista opcoes agora contém todos os valores únicos de "ID Loja" mais a opção adicional "Todas as Lojas".

app.layout = html.Div(children=[
# Define o layout do aplicativo Dash. O layout é um html.Div que contém todos os elementos da interface do usuário.
    html.H1(children='Faturamento das Lojas'),
# Cria um título de nível 1 com o texto "Faturamento das Lojas".
    html.H2(children='Gráfico com o faturamento de todos os produtos separados por loja'),
# Cria um subtítulo de nível 2 com o texto "Gráfico com o faturamento de todos os produtos separados por loja".
    html.Div(children='''
            Obs: Esse gráfico mostra a quantidade de produtos ventidos, não o faturamento 
            '''),
    html.Div(id="texto"),
# Este Div pode ser usado para exibir texto dinamicamente no aplicativo.
    dcc.Dropdown(opcoes, value='Todas as Lojas', id='lista_lojas'),
# Cria um dropdown (menu suspenso) com as opções de lojas. A opção padrão selecionada é "Todas as Lojas" e o id do dropdown é 'lista_lojas'.

    dcc.Graph(
        id='grafico_quantidade_vendas',
        figure=fig
# Cria um gráfico usando o dcc.Graph. O id do gráfico é 'grafico_quantidade_vendas' e a figura a ser exibida é definida por fig.
    )
])

@app.callback(
# Define um callback no Dash. Um callback é uma função que é chamada automaticamente sempre que os inputs especificados mudam.
    Output('grafico_quantidade_vendas', 'figure'),
# Especifica que a saída da função callback será o parâmetro figure do componente com o id 'grafico_quantidade_vendas'.
    Input('lista_lojas', 'value')
# Especifica que a entrada para a função callback será o valor selecionado do dropdown com o id 'lista_lojas'.
)
def update_output(value):
# Define a função update_output que será chamada quando o valor do dropdown mudar.
    if value == "Todas as Lojas":
        fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
# Verifica se o valor selecionado é "Todas as Lojas".
#  Se for "Todas as Lojas", cria um gráfico de barras usando todos os dados do DataFrame df.
    else: 
        tabela_filtrada = df.loc[df['ID Loja']==value, :]
        fig = px.bar(tabela_filtrada, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
# Caso o valor selecionado não seja "Todas as Lojas", filtra o DataFrame df para incluir apenas as linhas onde 'ID Loja' é igual ao valor selecionado.
# Cria um gráfico de barras usando o DataFrame filtrado tabela_filtrada.
    return fig
# Retorna o gráfico criado para ser exibido no componente dcc.Graph com o id 'grafico_quantidade_vendas'.

if __name__ == '__main__':
    app.run(debug=True)
# Verifica se o módulo está sendo executado como o script principal. Se for, executa o código dentro do bloco if.