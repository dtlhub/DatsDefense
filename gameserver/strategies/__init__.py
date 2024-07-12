from .idle import IdleStrategy

_STRATEGIES_LIST = [
    IdleStrategy,
]

ALL_STRATEGIES = {strategy.name(): strategy for strategy in _STRATEGIES_LIST}
