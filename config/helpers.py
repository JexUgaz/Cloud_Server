###########  Acciones  ###############
import os
import platform
import inquirer
import time
import sys

class MensajeResultados:
	success="success"
	failed="failed"

def clearScreen():
    sys_op= platform.system()
    if sys_op=="Linux":
        os.system('clear')
    elif sys_op=="Windows":
        os.system('cls')
    else:
        print("No es Linux ni Windows")


##########  FORMATO UI    #############
def setBarra(enter=False, text="",total_dashes=70):
    n_letters = len(text)

    if n_letters == 0:
        print("-" * total_dashes)
    else:
        n_edgeSpaces = 3
        n_spaces = n_edgeSpaces * 2 + n_letters
        n_dashes = (total_dashes - n_spaces) // 2

        if total_dashes % 2 != 0 or n_letters % 2 == 0:
            # Cantidad de barras es impar o cantidad de letras es par
            extend = "-" if (total_dashes % 2 != 0 and n_letters % 2 == 0) else ""
            print("-" * n_dashes + " " * n_edgeSpaces + text + " " * n_edgeSpaces + extend + "-" * n_dashes)
        else:
            print("-" * n_dashes + " " * n_edgeSpaces + text + " " * n_edgeSpaces + "-" + "-" * n_dashes)

    if enter:
        print()

def setListOptionsShell(message:str,choices:list[str]):
    opciones = [
            inquirer.List("opcion",
                        message=message,
                        choices=[(c,c) for c in choices])
        ]
    respuestas = inquirer.prompt(opciones)
    return respuestas["opcion"]

def printWaiting(text):
    print(f"{text}\n")
    input("Presione ENTER para continuar...")

def setTitle(title=""):
    setBarra()
    setBarra(text=title)
    setBarra(enter=True)

def loading_animation():
    global done
    done=False
    chars = ['\\', '-', '/']
    i = 0
    while not done:
        sys.stdout.write(f'\Espere... {chars[i]}')
        sys.stdout.flush()
        time.sleep(0.1)
        i = (i + 1) % len(chars)
    
    sys.stdout.write(f'\Espere...  Terminado!')
    sys.stdout.flush()

def cancel_loading_done():
    global done
    done=True
