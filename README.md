# Barcode-Interceptor
Script para interceptar códigos de barras registrados por um leitor de códigos de barras e substituí-los por códigos fornecidos pelo usuário.

Como usar:

Instale as bibliotecas [keyboard](https://pypi.org/project/keyboard/) e [mouse](https://pypi.org/project/mouse/)

```
pip install keyboard
pip install mouse
```

Abra o arquivo barcodes.txt e adicione os códigos de barras que deseja substituir, e o código pelo qual será substituído.

Adicionar somente um código de barras e um código para substituí-lo POR LINHA, separados por virgula, no seguinte formato:

CódigoDeBarras, NovoCódigo

No arquivo keys.txt, pode-se adicionar teclas para "resetar" a variável que armazena o código de barras, para evitar que entradas do usuário sejam interpretadas como códigos de barras em momentos indesejados.
