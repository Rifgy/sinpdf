import socket

def get_local_hostname():
    try:
        # get host domain name
        hostname = socket.gethostname()
        return hostname
    except Exception as e:
        if __name__ == "__main__":
            return f"Error when receiving the name of the host: {e}"
        else:
            return f'error'

if __name__ == "__main__":
    local_hostname = get_local_hostname()
    print(f"Local host name: {local_hostname}")