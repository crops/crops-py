from docker import Client

def docker_connect(base_url):
    cli = Client(base_url)
    return cli
