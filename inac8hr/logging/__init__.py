from datetime import date, datetime
from colorama import init, Fore

COLOR_CODE = {
    "INFO": Fore.BLUE
}

END_COLOR_CODE = "\033[0m"


class Logger():
    def Log(self, text, msg_type="INFO"):
        init(convert=True)
        suffix = msg_type
        print(f"{Fore.CYAN}[{datetime.now()} | {suffix}]\033[00m {text}")
