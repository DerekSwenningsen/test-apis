'''
    To make it easy to print messages to console in color
'''

from colorama import Fore, Style


def info(msg) -> str:
    """
     Print a message to the console in a blue color. This is useful for
        debugging the program that is running on a remote host.

     Args:
        msg: The message to print. Should be a string or any object that can
            be converted to a string before being passed to : func : ` print `.

     Returns:
        None.
    """
    print(Fore.BLUE + msg + Style.RESET_ALL)


def success(msg) -> str:
    """
     Prints a success message to the standard output in a green color.

     Args:
        msg: The message to be printed.

     Returns:
        None.
    """
    print(Fore.GREEN + msg + Style.RESET_ALL)


def error(msg) -> str:
    """
     Print an error message to the console in red.

     Args:
        msg: The message to print. Must be a string.

     Returns:
        None.
    """
    print(Fore.RED + msg + Style.RESET_ALL)


def warn(msg) -> str:
    """
     Print a warning message to the console in yellow.

     Args:
        msg: The message to print. If it's a string it will be treated as a
         string and appended to the warning.

     Returns:
        None.
    """
    print(Fore.YELLOW + msg + Style.RESET_ALL)
