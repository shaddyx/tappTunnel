import logging


class _Ip_storage:
    ip_counter = 0

def resolve():
    _Ip_storage.ip_counter += 1
    ip = "192.168.10.{}".format(_Ip_storage.ip_counter)
    logging.info("Resolved ip: {}".format(ip))
    return ip