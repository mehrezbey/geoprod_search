import sys
from datetime import datetime

from search_module.utils.colors import Colors

def print_log(message, status):
    """
    Args:
        message (string): description of the message to print
        status (char): s for success, w for warning, e for error and i for info
    """
    status = status.lower()
    date = datetime.now().strftime("%H:%M:%S")
    color = Colors.END
    if(status == 's'):
        color = Colors.GREEN
        print(f"{color} [{date}] - SUCCESS : {message}")
        sys.stdout.flush()
        
    elif(status == 'e'):
        color = Colors.RED
        print(f"{color} [{date}] - ERROR : {message}")
        sys.stdout.flush()

    elif(status == 'w'):
        color = Colors.YELLOW
        print(f"{color} [{date}] - WARNING :  {message}")
        sys.stdout.flush()
        
    elif(status == 'i'):
        color = Colors.BLUE
        print(f"{color} [{date}] - INFO :  {message}")
        sys.stdout.flush()
        
    print(f"{Colors.END}")
    sys.stdout.flush()