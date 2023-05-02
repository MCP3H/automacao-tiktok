import pyautogui as pyg

print('Apertar Ctrl-C para fechar.')
try:
    while True:
        x, y = pyg.position()
        posicaoStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        print(posicaoStr, end='')
        print('\b' * len(posicaoStr), end='', flush=True)
except KeyboardInterrupt:
    print('\n')
