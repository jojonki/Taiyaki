class CostManager:
    def __init__(self, vocab, trans_cost):
        self._vocab = vocab
        self._trans_cost = trans_cost

    def getEmissionCost(self, node):
        if node['_surface'] in self._vocab:
            return self._vocab[node['_surface']]['emission_cost']
        else:
            # TODO handle correctly
            return 10000

    def getTransitionCost(self, lnode, rnode):
        try:
            key = '{}:{}'.format(self._vocab[lnode['_surface']]['lctx_id'], self._vocab[rnode['_surface']]['rctx_id'])
            return self._trans_cost[key]
        except KeyError:
            # TODO handle correctly
            return 10000
