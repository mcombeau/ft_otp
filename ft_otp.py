import argparse
import pathlib
from typing import Optional

HEADER = '''
███████╗████████╗      ██████╗ ████████╗██████╗ 
██╔════╝╚══██╔══╝     ██╔═══██╗╚══██╔══╝██╔══██╗
█████╗     ██║        ██║   ██║   ██║   ██████╔╝
██╔══╝     ██║        ██║   ██║   ██║   ██╔═══╝ 
██║        ██║███████╗╚██████╔╝   ██║   ██║     
╚═╝        ╚═╝╚══════╝ ╚═════╝    ╚═╝   ╚═╝     
                                                
'''

Args = argparse.Namespace
Parser = argparse.ArgumentParser
Path = pathlib.PosixPath

# ---------------------------
# Prettify
# ---------------------------
class color:
    HEADER = '\033[36m'
    INFO = '\033[96m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    RESET = '\033[0m'

def print_header() -> None:
    for line in HEADER.splitlines():
        print(color.HEADER + '{:^70}'.format(line) + color.RESET)

def print_args(args: Args) -> None:
    print('{:-^80}'.format(''))
    if args.key:
        print(f'[+] Key to generate TOTP with: {color.INFO}{args.key}{color.RESET}')
    if args.hex_key:
        print(f'[+] Hexadecimal key to encrypt: {color.INFO}{args.hex_key}{color.RESET}')
    print(f'[+] Verbose mode: {color.INFO}{args.verbose}{color.RESET}')
    print('{:-^80}'.format(''))

# ---------------------------
# Argument parsing
# ---------------------------
def parse_args() -> Args:
    parser: Parser = Parser(description = 'A Time-based One Time Password generator')
    parser.add_argument('-k', '--key', type = str, help = 'generate a Time-based One Time Password with the given encrypted key.')
    parser.add_argument('-g', '--generate-key', dest = 'hex', type = str, help = 'generate a key for TOTPs from a string of 64 hexadecimal characters.')
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = 'Enable verbose mode')
    args: Args = parser.parse_args()
    if args.key is None and args.hex is None:
        parser.print_help()
        exit(0)
    return args

# ---------------------------
# Main
# ---------------------------
def main() -> None:
    print_header()
    args: Args = parse_args()
    print_args(args)

if __name__ == '__main__':
    main()
