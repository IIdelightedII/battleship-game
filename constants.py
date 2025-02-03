from colorama import init, Fore, Back, Style
init()
SHIP = "■"
DESTROYED_SHIP = Fore.LIGHTRED_EX + 'X' + Style.RESET_ALL
EMPTY = Fore.LIGHTBLACK_EX  + "o" + Style.RESET_ALL # английская o
BUFFER_ZONE = Fore.LIGHTBLACK_EX  + "о" + Style.RESET_ALL # русская о
EXTRA_BUFFER_ZONE = Fore.LIGHTBLACK_EX + Style.BRIGHT + "·" + Style.RESET_ALL
FULLY_DESTROYED_SHIP = Fore.LIGHTWHITE_EX + Style.BRIGHT + "=" + Style.RESET_ALL
MISS = Fore.LIGHTBLUE_EX + "+" + Style.RESET_ALL