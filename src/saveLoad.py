
def saveFunc(varDict):
    with open('./save.txt', 'w', encoding='UTF-8') as f:
        for key, value in varDict.items():
            if key.startswith('Form') and value:
                f.write(f'{key}:{value}\n')

def loadFunc(window):
    with open('./save.txt', 'r', encoding='UTF-8') as f:
        for line in f.readlines():
            line_splitted = line.strip().split(':')
            keyValue = line_splitted[0]
            coinName = line_splitted[1]
            window[f'{keyValue}'].update(f'{coinName}')