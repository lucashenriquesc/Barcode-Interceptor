import os
import keyboard
import mouse
import csv

class Barcode():
    def __init__(self):
        self.filepath = os.getcwd() + "/barcodes.txt" #Caminho para o arquivo contendo os códigos de barras.
        self.barcode_reset_keys_filepath = os.getcwd() + "/keys.txt" #Caminho para o arquivo contendo as teclas que ao serem pressionadas, limpam a variável self.barcode.
        self.invalid_barcodes = {} #Dicionário onde são armazenados os códigos de barras do arquivo.
        self.barcode = '' #String onde é armazenado o código de barras bipado pelo usuário.
        self.special_keys = ['!', '@', '$', '%', '¨', '&', '*', '(', ')', 'up', 'down', 'left', 'right', 'page down', 'page up', 
                             'print screen', 'scroll lock', 'end', 'home', 'insert'] #Lista de teclas que precisam ser pressionadas dentro do keyboardhook.
        self.barcode_keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '#'] #Caracteres que ao serem pressionados, são considerados como parte de um código de barras.
        self.enter = ['enter'] 
        self.barcode_reset_keys = [] #Lista que armazena teclas que ao serem pressionadas, limpam a variável self.barcode.
    def load_codes(self):
        """Carrega o arquivo contendo os códigos de barras."""
        with open(self.filepath, 'r+') as f:
            reader = csv.reader(f)
            next(reader) #Pula a primeira linha do arquivo.
            print("Produtos cadastrados: ")
            for row in reader:
                self.invalid_barcodes[row[0].strip()] = row[1].strip()
                print("Peça: " + row[2].strip().upper() + "| Código de Barras: " + row[0].strip() + "| Código interno: " + row[1].strip())
    def load_reset_keys(self):
        """Carrega o arquivo contendo as teclas que limpam a variável self.barcode."""
        with open(self.barcode_reset_keys_filepath, 'r') as f:
            for row in csv.reader(f):
                for key in row: 
                    pass
                    self.barcode_reset_keys.append(key.strip())
    def on_mouse_event(self, event):
        """Limpa a variável self.barcode ao pressionar o botão esquerdo do mouse."""
        if mouse.is_pressed(button='left'):
            self.barcode = ''
    def keyboard_event(self, event):
        """Verifica as entradas do usuário ao pressionar teclas no teclado ou ao bipar com o scanner de código de barras."""
        if event.event_type == 'down':
            if event.name == 'enter' and self.barcode in self.invalid_barcodes.keys(): #Caso input seja ENTER e código de barras está no arquivo com um código interno para substituí-lo.
                self.clear_field() 
                self.barcode_replace(event) 
                self.barcode = ''
            elif event.name == 'enter' and self.barcode not in self.invalid_barcodes.keys(): #Caso input seja ENTER e código de barras não está no arquivo. Nada é modificado e a tecla ENTER é pressionada normalmente e o self.barcode é limpo.
                keyboard.press(event.scan_code)
                self.barcode = ''
            elif event.name in self.barcode_keys: #Verifica se a tecla pressionada é um número ou caracter considerado como parte de um código de barras.
                self.barcode += event.name
                keyboard.press(event.name)
            elif event.name in self.special_keys: #Verifica se a tecla pressionada é uma das teclas que precisam ser pressionadas dentro do keyboardhook
                keyboard.press(event.name)     
        if event.event_type == 'up': 
            keyboard.release(event.name)  
    def clear_field(self):
        """Limpa o campo de código de barras."""
        keyboard.press('ctrl'); keyboard.press('a'); keyboard.press('backspace')
        keyboard.release('ctrl'); keyboard.release('a'); keyboard.release('backspace')
    def barcode_replace(self, event):
        """Substitui o código de barras fornecido pelo usuário pelo código interno contido no arquivo."""
        self.barcode = str(self.invalid_barcodes[self.barcode])
        for number in list(self.barcode):
            keyboard.press_and_release(number)
        keyboard.press(event.scan_code)
        keyboard.release(event.scan_code)
    def clear_barcode(self, event):
        """Limpa a variável self.barcode quando as teclas no self.barcode_reset_keys são pressionadas, com exceção do SHIFT."""
        if event.event_type == 'down' and event.name in self.barcode_reset_keys:
            if event.name == 'shift':
                pass
            else:
                self.barcode = ''
        elif event.event_type == 'up' and event.name in self.barcode_reset_keys:
            pass
    def exec_keyhook(self):
        """Inicia o hook para monitorar os eventos de mouse e teclado."""
        mouse.hook(self.on_mouse_event)
        for key in self.barcode_keys:
            keyboard.hook_key(key, self.keyboard_event, suppress=True)
        for sp in self.special_keys:
            keyboard.hook_key(sp, self.keyboard_event, suppress=True)
        for nb in self.enter:
            keyboard.hook_key(nb, self.keyboard_event, suppress=True)
        for key in self.barcode_reset_keys:
            keyboard.hook_key(key, self.clear_barcode, suppress=False)
        keyboard.wait(None)

intercepter = Barcode()
intercepter.load_reset_keys()
intercepter.load_codes()
intercepter.exec_keyhook() 









































