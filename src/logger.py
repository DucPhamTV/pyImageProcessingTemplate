import logging

COMMON_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

formatter = logging.Formatter(COMMON_FORMAT)


def create_file_handler(filename, level):
    handler = logging.FileHandler(filename)
    handler.setLevel(level)
    handler.setFormatter(formatter)

    return handler


def create_stream_handler(level=logging.DEBUG):
    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(formatter)

    return handler
