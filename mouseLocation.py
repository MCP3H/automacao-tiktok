import pyautogui as pyg

print('Apertar Ctrl-C para fechar.')
try:
    while True:
        x, y = pyg.position()
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        print(positionStr, end='')
        print('\b' * len(positionStr), end='', flush=True)
except KeyboardInterrupt:
    print('\n')
