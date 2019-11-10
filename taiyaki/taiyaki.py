"""Taiyaki class"""
import copy
import os
import warnings

from cost_manager import CostManager
from double_array import DoubleArray
from lattice import Lattice
import mecab_data_loader as mdl
from utils.common import savePickle, loadPickle


INF = 1e10


class Taiyaki:
    """Taiyaki class implementation"""

    def __init__(self, da_dic, word_dic_dir, trans_def):
        self.da = DoubleArray()
        self._loadDictionary(da_dic, word_dic_dir, trans_def)

    def _loadDictionary(self, da_dic, word_dic_dir, trans_def, load_pickle=True):
        # double-array
        if os.path.isfile(da_dic):
            self.da.load(da_dic)
        else:
            # TODO raise error
            warnings.warn('{} not found'.format(da_dic))

        # vocabulary files
        if os.path.exists('vocab.pkl') and load_pickle:
            self._vocab = loadPickle('vocab.pkl')
        else:
            self._vocab = mdl.loadDictionary('./data/mecab-ipadic-2.7.0-20070801/')
            savePickle(self._vocab, 'vocab.pkl')

        # transition matrix
        if os.path.exists('trans_cost.pkl') and load_pickle:
            self._trans_cost = loadPickle('trans_cost.pkl')
        else:
            self._trans_cost = mdl.loadMatrixDef('./data/mecab-ipadic-2.7.0-20070801/matrix.def')
            savePickle(self._trans_cost, 'trans_cost.pkl')

        self._cm = CostManager(self._vocab, self._trans_cost)

    def longestSearch(self, query):
        print('Input:', query)
        begin = 0
        end = len(query)
        result = []
        while begin < end:
            cp_list = self.da.commonPrefixSearch(query[begin:])
            if len(cp_list):
                longest = max(cp_list, key=len)
            else:
                longest = query[begin]
            result.append(longest)
            begin += len(longest)

        print('Result:', result)

    def createLattice(self, query):
        lattice = Lattice(query)
        
        for idx in range(len(query)):
            cps_q = query[idx:]
            # print('=====Search {}======'.format(cps_q))
            cp_list = self.da.commonPrefixSearch(cps_q)
            # print('commonPrefixSearch("{}"): {}'.format(cps_q, cp_list))
            for cp in cp_list:
                lattice.insert(idx, idx + len(cp), cp)

        return lattice

    def tokenize(self, query):
        lattice = self.createLattice(query)

        # forward
        bos = lattice.end_nodes[0][0]
        bos['min_cost'] = 0
        bos['min_prev'] = None
        for i in range(len(query) + 1):
            for rnode in lattice.begin_nodes[i]:
                rnode['min_prev'] = None
                rnode['min_cost'] = INF
                for lnode in lattice.end_nodes[i]:
                    cost = lnode['min_cost'] \
                            + self._cm.getTransitionCost(lnode, rnode) \
                            + self._cm.getEmissionCost(rnode)
                    if cost < rnode['min_cost']:
                        rnode['min_cost'] = cost
                        rnode['min_prev'] = copy.deepcopy(lnode)

        # backward
        eos = lattice.begin_nodes[-1][0]
        best_path = [eos]
        prev_node = eos['min_prev']
        while prev_node is not None:
            best_path.append(prev_node)
            prev_node = prev_node['min_prev']
        best_path = best_path[::-1] # reverse

        tokens = ([(b['_surface'], self._vocab[b['_surface']]['pos']) for b in best_path])
        return tokens
