from colorama import init, Fore, Back, Style

def warning(text):
    print(Fore.BLUE + Back.RED + f'{text}' + Style.RESET_ALL)

def info(text):
    print(Fore.BLUE + f'{text}' + Style.RESET_ALL)