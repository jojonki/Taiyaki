"""Utility class to calculate emission cost and transition cost
"""
from taiyaki.mecab_data_loader import H2I


class CostManager:
    def __init__(self, vocab, trans_cost):
        self._vocab = vocab
        self._trans_cost = trans_cost

    def getEmissionCost(self, node):
        if node['surface'] in self._vocab:
            return node['cost']
        else:
            # TODO handle correctly
            return 10000

    def getTransitionCost(self, lnode, rnode):
        try:
            key = '{}:{}'.format(lnode['lctx_id'], rnode['rctx_id'])
            return self._trans_cost[key]
        except KeyError:
            # TODO handle correctly
            return 10000
