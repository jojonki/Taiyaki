"""Taiyaki class"""
import copy
import os
import sys
import warnings

from taiyaki.cost_manager import CostManager
from taiyaki.double_array import DoubleArray
from taiyaki.lattice import Lattice
from utils.common import savePickle, loadPickle


INF = 1e10


class Taiyaki:
    """Taiyaki class implementation"""

    def __init__(self, da_dic, word_dic_dir, trans_def):
        self.da = DoubleArray()
        print('Loading dictionaries...')
        self._loadDictionary(da_dic, word_dic_dir, trans_def)
        print('Loaded!')

    def _loadDictionary(self, da_dic_file, vocab_dic_file, trans_cost_file):
        # double-array
        if os.path.isfile(da_dic_file):
            self.da.load(da_dic_file)
        else:
            # TODO raise error
            warnings.warn('{} not found'.format(da_dic_file))
            sys.exit()

        # vocabulary files
        if os.path.isfile(vocab_dic_file):
            self._vocab = loadPickle(vocab_dic_file)
        else:
            # TODO raise error
            warnings.warn('{} not found'.format(vocab_dic_file))
            sys.exit()

        # transition matrix
        if os.path.isfile(trans_cost_file):
            self._trans_cost = loadPickle(trans_cost_file)
        else:
            # TODO raise error
            warnings.warn('{} not found'.format(trans_cost_file))
            sys.exit()

        self._cm = CostManager(self._vocab, self._trans_cost)

    def longestSearch(self, query):
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

        return result

    def commonPrefixSearch(self, query):
        return self.da.commonPrefixSearch(query)

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
