from .idle import IdleStrategy
from .stupid_attack import StupidAttackStrategy

_STRATEGIES_LIST = [
    IdleStrategy,
    StupidAttackStrategy
]

ALL_STRATEGIES = {strategy.name(): strategy for strategy in _STRATEGIES_LIST}
