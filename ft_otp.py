import argparse
import os
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

class InvalidHexKeyError(Exception):
    def __init__(self, message = 'invalid hex key: key must be 64 hexadecimal characters') -> None:
        self.message: str = message
        super().__init__(self.message)

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
    if args.hex:
        print(f'[+] Hexadecimal key to encrypt: {color.INFO}{args.hex}{color.RESET}')
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

def get_file_contents(file_name: str, verbose: bool = False) -> str:
    file_path: Path = Path(file_name)
    if verbose:
        print(f'Opening {file_name} as a file...')
    with open(file_path,'r') as f:
        content: str = f.read().strip()
        if verbose:
            print(f'File {file_name} found.')
            print(f'File {file_name} contains: \"{content}\"')
        return content

# ---------------------------
# Key generation
# ---------------------------
def validate_hex_key(hex: str, verbose: bool = False) -> None:
    if len(hex) != 64:
        raise InvalidHexKeyError
    if verbose:
        print(f'{color.SUCCESS}Valid hex key: {hex}{color.RESET}')

def get_hex_key(args: Args) -> str:
    try:
        validate_hex_key(args.hex, args.verbose)
        return args.hex
    except InvalidHexKeyError as e:
        if args.verbose:
            print(f'{args.hex}: {e}')
        hex_key: str = get_file_contents(args.hex, args.verbose)
        validate_hex_key(hex_key, args.verbose)
        return hex_key
        
def generate_key_from_hex(args: Args) -> None:
    hex: str = get_hex_key(args)

# ---------------------------
# Main
# ---------------------------
def main() -> None:
    print_header()
    args: Args = parse_args()
    print_args(args)
    try:
        if args.hex:
            generate_key_from_hex(args)
    except Exception as e:
        print(f'{color.ERROR}ft_otp: error: {e}{color.RESET}')

if __name__ == '__main__':
    main()
