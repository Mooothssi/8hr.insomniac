from datetime import date, datetime
from colorama import init, Fore

COLOR_CODE = {
    "INFO": Fore.CYAN,
    "INTRO": Fore.LIGHTMAGENTA_EX
}

END_COLOR_CODE = "\033[0m"


class Logger():
    def Log(self, text, msg_type="INFO"):
        init(convert=True)
        suffix = msg_type
        print(f"{COLOR_CODE[msg_type]}[{datetime.now()} | {suffix}]\033[00m {text}")

    def Intro(self, text, msg_type="INTRO"):
        init(convert=True)
        suffix = msg_type
        print(f"{COLOR_CODE[msg_type]}{text}\033[00m")
