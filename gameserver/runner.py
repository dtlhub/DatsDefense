from .consumer import ApiConsumer
from .storage import RoundStorage


class Runner:
    def __init__(self, api: ApiConsumer): ...
