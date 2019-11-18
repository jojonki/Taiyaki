"""Utility class to calculate emission cost and transition cost
"""
from taiyaki.mecab_data_loader import H2I


class CostManager:
    def __init__(self, vocab, trans_cost):
        self._vocab = vocab
        self._trans_cost = trans_cost

    def getEmissionCost(self, node):
        assert 'cost' in node
        return node['cost']

    def getTransitionCost(self, lnode, rnode):
        if rnode['surface'] == '__EOS__':
            return 0

        try:
            key = '{}:{}'.format(lnode['lctx_id'], rnode['rctx_id'])
            return self._trans_cost[key]
        except KeyError:
            # TODO handle correctly
            print('Unknown transition:', lnode['surface'], rnode['surface'])
            return 10000
