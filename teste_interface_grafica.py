# Criar uma interface gráfica em python usando tkinter com as seguintes definições:

# 1. O primeiro parâmetro da interface vai ser essa pergunta "Preencha o item que vai ser detectado nos vídeos:", e abaixo da pergunta é um combo com 3 items (1-teste/2-teste2/3-teste3);

# 2. O segundo parâmetro da interface vai ser essa pergunta "Quanto tempo de frame vai ser analisado dos vídeos (em segundos):", e abaixo vai ser um range slider de 0 a 60, quando mover o range slider deve mostrar o número abaixo;

# 3. O terceiro parâmetro da interface vai ser essa pergunta "Qual o percentual de frames que o item tem que aparecer no vídeo, e abaixo vai ser um range slider de 0 a 100, quando mover o range slider deve mostrar o número abaixo;

# 4. O quarto parâmetro da interface vai ser dois radios button, um com o texto "Tempo de execução" e o outro preenchido com o texto "Quantidade de vídeos";

# 5. O quinto parâmetro da interface está relacionado com o quarto parâmetro, se o usuário preencher o radio button "Tempo de execução", aparece um parâmetro com a pergunta "Quanto tempo a ferramenta vai ficar executando (em minutos):" e abaixo um range slider de 0 a 500, quando mover o range slider deve mostrar o número abaixo, e se o usuário preencher o radio button "Quantos vídeos vc deseja captar:" e abaixo um range slider de 0 a 100, quando mover o range slider deve mostrar o número abaixo

# 7.  Vai ter um botão de enviar, que após pressionar, vai printar todas as informações dos parâmetros 

# 8. A interface vai ficar do lado superior direito da tela do windows

import PySimpleGUI as sg

# Definindo o tema da interface
sg.theme('DarkAmber')

# Definindo a estrutura dos elementos da interface
layout = [
    [sg.Text('Preencha o item que vai ser detectado nos vídeos:')],
    [sg.Combo(['1-teste', '2-teste2', '3-teste3'], size=(40,20))],
    
    [sg.Text('Quanto tempo de frame vai ser analisado dos vídeos (em segundos):')],
    [sg.Slider(range=(0, 60), orientation='h', size=(40,20), default_value=0, key='sliderTempo')],

    [sg.Text('Qual o percentual de frames que o item tem que aparecer no vídeo?')],
    [sg.Slider(range=(0, 100), orientation='h', size=(40,20), default_value=0, key='sliderPercentual')],

    [sg.Text('Selecione uma opção abaixo')],
    [sg.Radio('Tempo de execução', 'rdExecucao', enable_events=True, default=True, key='rbTempoExec'), sg.Radio('Quantidade de vídeos', 'rdExecucao', enable_events=True, key='rbQtdVideos')],
    [sg.Text('Quanto tempo a ferramenta vai ficar executando (em minutos):', visible=True, key='lblExec')],
    [sg.Slider(range=(0, 500), orientation='h', size=(40,20), default_value=0, key='exec', visible=True)],
    #[sg.Text('Quantos vídeos você deseja captar:', visible=False, key='lblQtdVideos'), sg.Slider(range=(0, 100), orientation='h', size=(40,20), default_value=0, key='qtdVideos', visible=False)],

    [sg.Button('Executar', key='btnExecutar')]
]

# Criando a janela com os elementos definidos na estrutura layout
window = sg.Window('Minha janela', layout, location=(1000, 0))    # Definindo a localização da janela na tela

# Loop de eventos para a interface gráfica
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    if event == 'rbTempoExec':
        window['lblExec'].update('Quanto tempo a ferramenta vai ficar executando (em minutos):')
        window['exec'].update(0, range=(0, 500))

    if event == 'rbQtdVideos':
        window['lblExec'].update('Quantos vídeos você deseja captar:')
        window['exec'].update(0, range=(0, 100))

    if event == 'btnExecutar':
        if values['rbTempoExec']:
            tempo_execucao = values['tempoExec']
            print(f'Tempo de execução: {tempo_execucao} minutos')
        elif values['rbQtdVideos']:
            qtd_videos = values['qtdVideos']
            print(f'Quantidade de vídeos: {qtd_videos}')
