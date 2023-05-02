from tkinter import PhotoImage
import threading
import PySimpleGUI as sg
from ctypes import windll
import sys
import torch
import funcoespyautogui as pya
import funcoesanalise as ma
import funcoesdb as db
import time
import win32gui
from app import app
 
if __name__ == '__main__':

    # Classe para configurar os parametros
    class Parametros(object):
        pass

    # Definindo o tema da interface
    sg.theme('DarkGrey3')

    # Tive que criar dessa forma a interface para evitar que o usuário mova a janela do programa, 
    # e manter o programa na barra do windows
    #https://github.com/PySimpleGUI/PySimpleGUI/issues/150 - Missing program icon on taskbar when using no_titlebar = True

    GWL_EXSTYLE = -20
    WS_EX_APPWINDOW = 0x00040000
    WS_EX_TOOLWINDOW = 0x00000080

    class Janela(sg.Window):
        def __init__(self, *args, no_titlebar=False, **kwargs):
            self._no_titlebar = no_titlebar
            super().__init__(*args, **kwargs)

        def Finalize(self, *args, **kwargs):
            super().Finalize(*args, **kwargs)
            if self._no_titlebar:
                root = self.TKroot
                root.overrideredirect(True)
                hwnd = windll.user32.GetParent(root.winfo_id())

                if hasattr(windll.user32, "GetWindowLongPtrW"):
                    get_window_style = windll.user32.GetWindowLongPtrW
                    set_window_style = windll.user32.SetWindowLongPtrW
                else:
                    get_window_style = windll.user32.GetWindowLongW
                    set_window_style = windll.user32.SetWindowLongW

                style = get_window_style(hwnd, GWL_EXSTYLE)
                style = style & ~WS_EX_TOOLWINDOW
                style = style | WS_EX_APPWINDOW
                set_window_style(hwnd, GWL_EXSTYLE, style)
                img = PhotoImage(file='icone.png')
                root.tk.call('wm', 'iconphoto', root._w, img)
                root.withdraw()
                root.deiconify()
        
        def windowSeal(self):
            root = self.TKroot
            root.overrideredirect(True)
            hwnd = windll.user32.GetParent(root.winfo_id())
            win32gui.SetForegroundWindow(hwnd)

    # Criei um dicionário que já tem todos os objetos possíveis de detectar do YOLO
    objetos_pt = {
        'avião': 'airplane',
        'banana': 'banana',
        'banco': 'bench',
        'barco': 'boat',
        'bicicleta': 'bicycle',
        'bola esportiva': 'sports ball',
        'bolo': 'cake',
        'bolsa': 'handbag',
        'brócolis': 'broccoli',
        'cachorro': 'dog',
        'cachorro-quente': 'hot dog',
        'cadeira': 'chair',
        'cama': 'bed',
        'caminhão': 'truck',
        'carro': 'car',
        'cavalo': 'horse',
        'celular': 'cell phone',
        'cenoura': 'carrot',
        'colher': 'spoon',
        'controle remoto': 'remote',
        'elefante': 'elephant',
        'escova de dentes': 'toothbrush',
        'esquis': 'skis',
        'facas': 'knife',
        'forno': 'oven',
        'frisbee': 'frisbee',
        'garfo': 'fork',
        'garrafa': 'bottle',
        'gato': 'cat',
        'geladeira': 'refrigerator',
        'girafa': 'giraffe',
        'gravata': 'tie',
        'guarda-chuva': 'umbrella',
        'hidrante': 'fire hydrant',
        'laranja': 'orange',
        'livro': 'book',
        'luva de beisebol': 'baseball glove',
        'mala': 'suitcase',
        'maçã': 'apple',
        'mesa de jantar': 'dining table',
        'microondas': 'microwave',
        'mochila': 'backpack',
        'motocicleta': 'motorcycle',
        'mouse': 'mouse',
        'notebook': 'laptop',
        'ônibus': 'bus',
        'ovelha': 'sheep',
        'parquímetro': 'parking meter',
        'pessoa': 'person',
        'pia': 'sink',
        'pipa': 'kite',
        'pizza': 'pizza',
        'placa de pare': 'stop sign',
        'planta em vaso': 'potted plant',
        'prancha de snowboard': 'snowboard',
        'prancha de surf': 'surfboard',
        'pássaro': 'bird',
        'raquete de tênis': 'tennis racket',
        'relógio': 'clock',
        'rosquinha': 'donut',
        'sanduíche': 'sandwich',
        'secador de cabelo': 'hair drier',
        'semáforo': 'traffic light',
        'skate': 'skateboard',
        'sofá': 'couch',
        'taco de beisebol': 'baseball bat',
        'taça de vinho': 'wine glass',
        'teclado': 'keyboard',
        'televisão': 'tv',
        'tesoura': 'scissors',
        'tigela': 'bowl',
        'torradeira': 'toaster',
        'trem': 'train',
        'ursinho de pelúcia': 'teddy bear',
        'urso': 'bear',
        'vaca': 'cow',
        'vaso': 'vase',
        'vaso sanitário': 'toilet',
        'xícara': 'cup',
        'zebra': 'zebra',
    }

    # Defino a estrutura dos elementos da interface
    interface = [
        [sg.Text('Preencha o objeto que vai ser detectado nos vídeos:')],
        [sg.Combo(list(objetos_pt.keys()), size=(40,20), key='cmbObjeto')],

        [sg.Text('Qual o percentual de critério de aceitação dos frames:')],
        [sg.Slider(range=(0, 100), orientation='h', size=(40,20), default_value=50, key='sliderCriterio', enable_events=True, disable_number_display=True)],
        [sg.Text('50', key='sliderCriterioText', size=(3, 1))],
        
        [sg.Text('Quanto tempo de frame vai ser analisado dos vídeos (em segundos):')],
        [sg.Slider(range=(0, 60), orientation='h', size=(40,20), default_value=0, key='sliderTempo', enable_events=True, disable_number_display=True)],
        [sg.Text('0', key='sliderTempoText', size=(3, 1))],

        [sg.Text('Qual o percentual de frames que o objeto tem que aparecer no vídeo:')],
        [sg.Slider(range=(0, 100), orientation='h', size=(40,20), default_value=0, key='sliderPercentual', enable_events=True, disable_number_display=True)],
        [sg.Text('0', key='sliderPercentualText', size=(3, 1))],

        [sg.Text('Quantos vídeos você deseja analisar:', visible=True, key='lblExec')],
        [sg.Slider(range=(0, 100), orientation='h', size=(40,20), default_value=0, key='exec', visible=True, enable_events=True, disable_number_display=True)],
        [sg.Text('0', key='execText', size=(3, 1))],

        [sg.Button('Executar', key='btnExecutar'), sg.Button('Sair', key='btnSair')]
    ]

    parametros_validados_interface_carregado = False
    parametros_validados_interface = [
        [sg.Text('-----------------------------------------------------------------------------------')],
        [sg.Text("", key='paramText')],
    ]

    algoritmo_interface_carregado = False
    algoritmo_interface = [
        [sg.Text('-----------------------------------------------------------------------------------')],
        [sg.Text("Carregando o algoritmo de detecção de objeto YOLOV5")],
    ]

    algoritmo_carregado_interface_carregado = False
    algoritmo_carregado_interface = [
        [sg.Text("Algoritmo carregado")],
        [sg.Text('-----------------------------------------------------------------------------------')],
    ]

    execucao_interface_carregado = False
    execucao_interface = [
        [sg.Text("Quantidade de vídeos analisados: ")],
        [sg.Text(0, key="videoAnalisado")],
        [sg.Text("Quantidade de vídeos que correspondem aos parâmetros: ")],
        [sg.Text(0, key="videoAnalisadoParam")]
    ]

    # Criao a janela com os elementos definidos na estrutura interface
    janela = Janela('Hunter', interface, location=(1350, 200), grab_anywhere=False, grab_anywhere_using_control=False, icon="icone.ico", no_titlebar=True, finalize=True)

    programa_executando = False
    flag_cancelamento = threading.Event()
    thread = "thread da aplicação "

    def create_thread_app(janela, values):
        global programa_executando
        programa_executando = True
        global thread
        thread = threading.Thread(target=comecaAplicacao, args=(janela, values))
        thread.start()

    def comecaAplicacao(janela, values):

        # VALIDA PARAM

        if (values['cmbObjeto'] == ''):
            janela['paramText'].update('Objeto para a detecção não foi selecionado')
            janela['btnExecutar'].update(disabled=False, button_color=("#dfddc7", "#a34a28"))
            return False
        
        if (values['sliderCriterio'] == 0):
            janela['paramText'].update('O critério de aceitação está zerado')
            janela['btnExecutar'].update(disabled=False, button_color=("#dfddc7", "#a34a28"))
            return False
        
        if (values['sliderTempo'] == 0):
            janela['paramText'].update('O tempo de frame da análise dos vídeos está zerado')
            janela['btnExecutar'].update(disabled=False, button_color=("#dfddc7", "#a34a28"))
            return False
        
        if (values['sliderPercentual'] == 0):
            janela['paramText'].update('O percentual de frames que o objeto tem que aparecer está zerado')
            janela['btnExecutar'].update(disabled=False, button_color=("#dfddc7", "#a34a28"))
            return False
        
        if (values['exec'] == 0):
            janela['paramText'].update('A quantidade de vídeos para analisar está zerado')
            janela['btnExecutar'].update(disabled=False, button_color=("#dfddc7", "#a34a28"))
            return False
        
        janela['paramText'].update('Os parâmetros estão corretos')

        # MODELO
        if not flag_cancelamento.is_set():
            global algoritmo_interface_carregado
            if (algoritmo_interface_carregado == False):
                algoritmo_interface_carregado = True
                janela.extend_layout(janela, algoritmo_interface)
                janela.refresh()

        if not flag_cancelamento.is_set():
            tipo_modelo = 'yolov5x' # yolov5n, yolov5s, yolov5m, yolov5l, yolov5x  -- Coloquei em ordem qual modelo esta mais treinado
            use_cuda = torch.cuda.is_available()
            device = torch.device("cuda" if use_cuda else "cpu")
            model = torch.hub.load('ultralytics/yolov5', tipo_modelo, device)

        if not flag_cancelamento.is_set():
            global algoritmo_carregado_interface_carregado
            if (algoritmo_carregado_interface_carregado == False):
                algoritmo_carregado_interface_carregado = True
                janela.extend_layout(janela, algoritmo_carregado_interface)
                janela.refresh()
        
        # PARAMS
        if not flag_cancelamento.is_set():
            
            settings = Parametros()
            settings.modelo = tipo_modelo
            settings.param = values['cmbObjeto']
            settings.time_video_sec = int(values['sliderTempo'])
            settings.crit_aceit = int(values['sliderCriterio'])
            settings.perc_video = int(values['sliderPercentual'])
            settings.qt_video = int(values['exec'])

            conexao = db.abrirConexao()
            config = db.criarParametro(conexao, settings)
            
            # MIDIA

            print("*************************************************")
            print("ABRINDO MIDIA")
            pya.abrirTiktokTag(settings.param)
            time.sleep(10)
            pya.abrirMidia()
            time.sleep(1)
            print("*************************************************")
            print("MIDIA CARREGADA")
        
        if not flag_cancelamento.is_set():
            janela.windowSeal()
            global execucao_interface_carregado
            if (execucao_interface_carregado == False):
                execucao_interface_carregado = True
                janela.extend_layout(janela, execucao_interface)
                janela.refresh()

        # ANALISE
        videos = 0
        videos_ana = 0
        begin_tool = time.perf_counter()
        end_tool = time.perf_counter()
        while(not flag_cancelamento.is_set() and settings.qt_video > videos_ana):
            
            video = ma.Video(model, settings)

            # Find video
            while(True):
                video_url = pya.copiarLinkVideo()
                video_url = video_url.split("?q=")[0]
                has_video = db.verificarVideo(conexao, video_url, config)
                if len(has_video) > 0:
                    pya.passarVideo()
                else:
                    break
            
            janela.windowSeal()
            time.sleep(1)

            analise = video.run()
            if (analise.is_valid):
                # pya.likeVideo()
                videos += 1
                janela['videoAnalisadoParam'].update(str(videos))

            db.salvarVideo(conexao, config, video_url, analise.qt_frame, analise.qt_frame_param, analise.is_valid)

            videos_ana += 1
            janela['videoAnalisado'].update(str(videos_ana))

            pya.passarVideo()
            time.sleep(1)

            end_tool = time.perf_counter()
            
        print("*************************************************")
        print(f'Videos analisados: {videos_ana}')
        print(f'Videos analisados passou no param: {videos}')
        print(f'Tempo de execucao: {end_tool - begin_tool}')

        if not flag_cancelamento.is_set():
            pya.fecharMidia()
            db.fecharConexao(conexao)
            janela['btnExecutar'].update(disabled=False, button_color=("#dfddc7", "#a34a28"))
        
        global programa_executando
        programa_executando = False

        # if not flag_cancelamento.is_set():
        #     if (programa_executando == False):
        #         janela.finalize()

    # Loop de eventos para a interface gráfica
    while True:
        event, values = janela.read()

        if event == sg.WINDOW_CLOSED:
            break
        
        # Ajusta texto dos sliders
        if event == 'sliderTempo':
            janela['sliderTempoText'].update(str(int(values['sliderTempo'])))
        elif event == 'sliderCriterio':
            janela['sliderCriterioText'].update(str(int(values['sliderCriterio'])))
        elif event == 'sliderPercentual':
            janela['sliderPercentualText'].update(str(int(values['sliderPercentual'])))
        elif event == 'exec':
            janela['execText'].update(str(int(values['exec'])))

        if event == 'btnSair':
            janela.finalize()
            new_interface = [
                [sg.Text('Preencha o objeto que vai ser detectado nos vídeos:')],
                [sg.Combo(list(objetos_pt.keys()), size=(40,20), key='cmbObjeto')],

                [sg.Text('Qual o percentual de critério de aceitação dos frames:')],
                [sg.Slider(range=(0, 100), orientation='h', size=(40,20), default_value=0, key='sliderCriterio', enable_events=True, disable_number_display=True)],
                [sg.Text('0', key='sliderCriterioText', size=(3, 1))],
                
                [sg.Text('Quanto tempo de frame vai ser analisado dos vídeos (em segundos):')],
                [sg.Slider(range=(0, 60), orientation='h', size=(40,20), default_value=0, key='sliderTempo', enable_events=True, disable_number_display=True)],
                [sg.Text('0', key='sliderTempoText', size=(3, 1))],

                [sg.Text('Qual o percentual de frames que o objeto tem que aparecer no vídeo:')],
                [sg.Slider(range=(0, 100), orientation='h', size=(40,20), default_value=0, key='sliderPercentual', enable_events=True, disable_number_display=True)],
                [sg.Text('0', key='sliderPercentualText', size=(3, 1))],

                [sg.Text('Quantos vídeos você deseja analisar:', visible=True, key='lblExec')],
                [sg.Slider(range=(0, 100), orientation='h', size=(40,20), default_value=0, key='exec', visible=True, enable_events=True, disable_number_display=True)],
                [sg.Text('0', key='execText', size=(3, 1))],

                [sg.Button('Executar', key='btnExecutar'), sg.Button('Sair', key='btnSair')]
            ]
            janela.layout(new_interface) 
            janela.refresh()

            resp = sg.popup("Deseja encerrar a execução da aplicação?", background_color="DarkBlue", custom_text=("Sim", "Não"), no_titlebar=True, location=(1350, 200))
            if resp == "Sim":
                flag_cancelamento.set()
                if (programa_executando == False): break
                else:
                    thread.join()
                    break

        if event == 'btnExecutar':
            janela['btnExecutar'].update(disabled=True, button_color=('white', 'gray'))

            if (parametros_validados_interface_carregado == False):
                parametros_validados_interface_carregado = True
                janela.extend_layout(janela, parametros_validados_interface)
                janela.refresh()
                
            create_thread_app(janela, values)

    janela.close()

    pya.abrirLocalhost()
    app.run()