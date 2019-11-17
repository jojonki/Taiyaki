class Lattice(object):
    def __init__(self, sent=None):
        self.clear()
        if sent:
            self.setSentence(sent)

    def _newNode(self, begin, end, _surface_str=None, props=None, unk=None):
        ret_node = {
            'surface': begin,
            'length': end - begin,
            '_surface': _surface_str, # TODO redundant
            'min_cost': None,
            'min_prev': None, # previous node
            'unk': unk
        }
        for k, v in props.items():
            ret_node[k] = v

        return ret_node

    def setSentence(self, sent):
        self._sent = sent
        # +1 for BOS or EOS ndoe
        self.begin_nodes = [[] for _ in range(len(sent) + 1)]
        self.end_nodes = [[] for _ in range(len(sent) + 1)]

        # TODO remove hard coding
        bos_node = self._newNode(0, 0, '__BOS__', {'lctx_id': 0, 'rctx_id': 0, 'cost': 0, 'pos': None, 'pron': None})
        self.end_nodes[0].append(bos_node)
        eos_node = self._newNode(len(sent), 0, '__EOS__', {'lctx_id': 1316, 'rctx_id': 1316, 'cost': 0, 'pos': None, 'pron': None})
        self.begin_nodes[len(sent)].append(eos_node)

    def insert(self, begin, end, _surface_str=None, props=None, unk=None):
        node = self._newNode(begin, end, _surface_str, props, unk)
        self.begin_nodes[begin].append(node)
        self.end_nodes[end].append(node)
        return node

    def clear(self):
        self._sent = None
        self.begin_nodes = []
        self.end_nodes = []

    def pprint(self):
        for i in range(len(self._sent) + 1):
            print(['{} ({})'.format(n['_surface'], n['pron']) for n in self.end_nodes[i]], end='')
            print(' ({}) '.format(i), end='')
            print(['{} ({})'.format(n['_surface'], n['pron']) for n in self.begin_nodes[i]])

    def plot(self):
        from graphviz import Digraph
        g = Digraph(format='png')
        g.attr('node', shape='circle')
        added_nodes = []
        for i in range(len(self._sent) + 1):
            for ct, n in enumerate(self.end_nodes[i]):
                if n['_surface'] not in added_nodes:
                    g.node(n['_surface'], n['_surface'])
                    added_nodes.append(n['_surface'])
            for ct, n in enumerate(self.begin_nodes[i]):
                if n['_surface'] not in added_nodes:
                    g.node(n['_surface'], n['_surface'])
                    added_nodes.append(n['_surface'])

            for en in self.end_nodes[i]:
                for bn in self.begin_nodes[i]:
                    g.edge(en['_surface'], bn['_surface'])

        print('Save this lattice image as png')
        g.render('lattice')
