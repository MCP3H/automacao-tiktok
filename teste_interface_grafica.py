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

if __name__ == '__main__':

    # Definindo o tema da interface
    sg.theme('DarkGrey3')

    #https://github.com/PySimpleGUI/PySimpleGUI/issues/150 - Missing program icon on taskbar when using no_titlebar = True

    GWL_EXSTYLE = -20
    WS_EX_APPWINDOW = 0x00040000
    WS_EX_TOOLWINDOW = 0x00000080

    class MyWindow(sg.Window):
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

    classes_pt = {
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

    # Definindo a estrutura dos elementos da interface
    layout = [
        [sg.Text('Preencha o objeto que vai ser detectado nos vídeos:')],
        [sg.Combo(list(classes_pt.keys()), size=(40,20), key='cmbObjeto')],

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

    valid_param_layout_loaded = False
    valid_param_layout = [
        [sg.Text('-----------------------------------------------------------------------------------')],
        [sg.Text("", key='paramText')],
    ]

    model_layout_loaded = False
    model_layout = [
        [sg.Text('-----------------------------------------------------------------------------------')],
        [sg.Text("Carregando algoritmo de detecção de objeto YOLOV5")],
    ]

    model_loaded_layout_loaded = False
    model_loaded_layout = [
        [sg.Text("Algoritmo carregado")],
        [sg.Text('-----------------------------------------------------------------------------------')],
    ]

    info_layout_loaded = False
    info_layout = [
        [sg.Text("Quantidade de vídeos analisados: ")],
        [sg.Text(0, key="videoAnalisado")],
        [sg.Text("Quantidade de vídeos que correspondem aos parâmetros: ")],
        [sg.Text(0, key="videoAnalisadoParam")]
    ]

    # Criando a janela com os elementos definidos na estrutura layout
    window = MyWindow('Hunter', layout, location=(1350, 200), grab_anywhere=False, grab_anywhere_using_control=False, icon="icone.ico", no_titlebar=True, finalize=True)

    running = 1
    go = False
    interface_running = True
    app_running = False
    flag_cancelamento = threading.Event()
    thread = "thread da aplicação "

    def create_thread_app(window, values):
        global app_running
        app_running = True
        global thread
        thread = threading.Thread(target=comecaAplicacao, args=(window, values))
        thread.start()

    def comecaAplicacao(window, values):

        # VALIDA PARAM

        if (values['cmbObjeto'] == ''):
            window['paramText'].update('Objeto para a detecção não foi selecionado')
            window['btnExecutar'].update(disabled=False, button_color=("#dfddc7", "#a34a28"))
            return False
        
        if (values['sliderCriterio'] == 0):
            window['paramText'].update('O critério de aceitação está zerado')
            window['btnExecutar'].update(disabled=False, button_color=("#dfddc7", "#a34a28"))
            return False
        
        if (values['sliderTempo'] == 0):
            window['paramText'].update('O tempo de frame da análise dos vídeos está zerado')
            window['btnExecutar'].update(disabled=False, button_color=("#dfddc7", "#a34a28"))
            return False
        
        if (values['sliderPercentual'] == 0):
            window['paramText'].update('O percentual de frames que o objeto tem que aparecer está zerado')
            window['btnExecutar'].update(disabled=False, button_color=("#dfddc7", "#a34a28"))
            return False
        
        if (values['exec'] == 0):
            window['paramText'].update('A quantidade de vídeos para analisar está zerado')
            window['btnExecutar'].update(disabled=False, button_color=("#dfddc7", "#a34a28"))
            return False
        
        window['paramText'].update('Os parâmetros estão corretos')

        # MODELO
        if not flag_cancelamento.is_set():
            global model_layout_loaded
            if (model_layout_loaded == False):
                model_layout_loaded = True
                window.extend_layout(window, model_layout)
                window.refresh()

        if not flag_cancelamento.is_set():
            use_cuda = torch.cuda.is_available()
            device = torch.device("cuda" if use_cuda else "cpu")
            model = torch.hub.load('ultralytics/yolov5', 'yolov5s', device)

        if not flag_cancelamento.is_set():
            global model_loaded_layout_loaded
            if (model_loaded_layout_loaded == False):
                model_loaded_layout_loaded = True
                window.extend_layout(window, model_loaded_layout)
                window.refresh()
        
        # PARAMS
        if not flag_cancelamento.is_set():
            class Settings(object):
                pass
            settings = Settings()
            settings.param = classes_pt.get(values['cmbObjeto'])
            settings.time_video_sec = int(values['sliderTempo'])
            settings.crit_aceit = int(values['sliderCriterio'])
            settings.perc_video = int(values['sliderPercentual'])
            settings.qt_video = int(values['exec'])

            conexao = db.abrirConexao()
            config = db.createConfig(conexao, settings)
            
            # MIDIA

            print("*************************************************")
            print("ABRINDO MIDIA")
            pya.openTiktok(settings.param)
            time.sleep(10)
            pya.openVideo()
            time.sleep(1)
            print("*************************************************")
            print("MIDIA CARREGADA")
        
        if not flag_cancelamento.is_set():
            window.windowSeal()
            global info_layout_loaded
            if (info_layout_loaded == False):
                info_layout_loaded = True
                window.extend_layout(window, info_layout)
                window.refresh()

        # ANALISE
        videos = 0
        videos_ana = 0
        begin_tool = time.perf_counter()
        end_tool = time.perf_counter()
        while(not flag_cancelamento.is_set() and settings.qt_video > videos_ana):
            
            video = ma.Video(model, settings)

            # Find video
            while(True):
                video_url = pya.copyLinkVideo()
                video_url = video_url.split("?q=")[0]
                has_video = db.verificarVideo(conexao, video_url, config)
                if len(has_video) > 0:
                    pya.passVideo()
                else:
                    break
            
            window.windowSeal()
            time.sleep(1)

            analise = video.run()
            if (analise.is_valid):
                # pya.likeVideo()
                videos += 1
                window['videoAnalisadoParam'].update(str(videos))

            db.salvarVideo(conexao, config, video_url, analise.qt_frame, analise.qt_frame_param, analise.is_valid)

            videos_ana += 1
            window['videoAnalisado'].update(str(videos_ana))

            pya.passVideo()
            time.sleep(1)

            end_tool = time.perf_counter()
            
        print("*************************************************")
        print(f'Videos analisados: {videos_ana}')
        print(f'Videos analisados passou no param: {videos}')
        print(f'Tempo de execucao: {end_tool - begin_tool}')

        if not flag_cancelamento.is_set():
            pya.closeVideo()
            db.fecharConexao(conexao)
            window['btnExecutar'].update(disabled=False, button_color=("#dfddc7", "#a34a28"))
        
        global app_running
        app_running = False

        if not flag_cancelamento.is_set():
            if (app_running == False):
                window.finalize()

        if flag_cancelamento.is_set():
            global interface_running
            interface_running = False

    # Loop de eventos para a interface gráfica
    while interface_running:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break
        
        # Ajusta texto dos sliders
        if event == 'sliderTempo':
            window['sliderTempoText'].update(str(int(values['sliderTempo'])))
        elif event == 'sliderCriterio':
            window['sliderCriterioText'].update(str(int(values['sliderCriterio'])))
        elif event == 'sliderPercentual':
            window['sliderPercentualText'].update(str(int(values['sliderPercentual'])))
        elif event == 'exec':
            window['execText'].update(str(int(values['exec'])))

        if event == 'btnSair':
            if (running):
                
                # window.finalize()
                # new_layout = [
                #     [sg.Text('Preencha o objeto que vai ser detectado nos vídeos:')],
                #     [sg.Combo(list(classes_pt.keys()), size=(40,20), key='cmbObjeto')],

                #     [sg.Text('Qual o percentual de critério de aceitação dos frames:')],
                #     [sg.Slider(range=(0, 100), orientation='h', size=(40,20), default_value=0, key='sliderCriterio', enable_events=True, disable_number_display=True)],
                #     [sg.Text('0', key='sliderCriterioText', size=(3, 1))],
                    
                #     [sg.Text('Quanto tempo de frame vai ser analisado dos vídeos (em segundos):')],
                #     [sg.Slider(range=(0, 60), orientation='h', size=(40,20), default_value=0, key='sliderTempo', enable_events=True, disable_number_display=True)],
                #     [sg.Text('0', key='sliderTempoText', size=(3, 1))],

                #     [sg.Text('Qual o percentual de frames que o objeto tem que aparecer no vídeo:')],
                #     [sg.Slider(range=(0, 100), orientation='h', size=(40,20), default_value=0, key='sliderPercentual', enable_events=True, disable_number_display=True)],
                #     [sg.Text('0', key='sliderPercentualText', size=(3, 1))],

                #     [sg.Text('Quantos vídeos você deseja analisar:', visible=True, key='lblExec')],
                #     [sg.Slider(range=(0, 100), orientation='h', size=(40,20), default_value=0, key='exec', visible=True, enable_events=True, disable_number_display=True)],
                #     [sg.Text('0', key='execText', size=(3, 1))],

                #     [sg.Button('Executar', key='btnExecutar'), sg.Button('Sair', key='btnSair')]
                # ]
                # window.layout(new_layout) 
                # window.refresh()

                resp = sg.popup("Deseja encerrar a execução da aplicação?", background_color="DarkBlue", custom_text=("Sim", "Não"), no_titlebar=True, location=(1350, 200))
                if resp == "Sim":
                    flag_cancelamento.set()
                    if (app_running == False): break
                    else:
                        thread.join()
                        break 

        if event == 'btnExecutar':
            window['btnExecutar'].update(disabled=True, button_color=('white', 'gray'))

            if (valid_param_layout_loaded == False):
                valid_param_layout_loaded = True
                window.extend_layout(window, valid_param_layout)
                window.refresh()
                
            create_thread_app(window, values)

    window.close()