"""Taiyaki class"""
import copy
import os
import sys
import warnings

from taiyaki.cost_manager import CostManager
from taiyaki.double_array import DoubleArray
from taiyaki.lattice import Lattice
from utils.common import savePickle, loadPickle
import taiyaki.mecab_data_loader as mdl


INF = 1e10


class Taiyaki:
    """Taiyaki class implementation"""

    def __init__(self, da_dic, word_dic_dir, trans_def, char_def):
        self.da = DoubleArray()
        print('Loading dictionaries...')
        self._loadDictionary(da_dic, word_dic_dir, trans_def, char_def)
        print('Loaded!')

    def _loadDictionary(self, da_dic_file, vocab_dic_file, trans_cost_file, char_cat_def_file):
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

        # char.def
        if os.path.isfile(char_cat_def_file):
            self._char_cat_def = loadPickle(char_cat_def_file)
        else:
            # TODO raise error
            warnings.warn('{} not found'.format(char_cat_def_file))
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
            if len(cp_list) == 0: # unk word
                unk_word, unk_cat_name = mdl.getUnkWordFromSentence(cps_q, self._char_cat_def)
                for props in self._vocab[unk_cat_name]:
                    # add dummy fields since unk.def does not have ruby and pron fields
                    props += ['*'] * (len(mdl.DIC_FORM) - len(props))
                    props_dic = {key: val for key, val, in zip(mdl.DIC_FORM[1:], props)} # ignore the first element, 'surface'
                    lattice.insert(idx, idx + len(unk_word), unk_word, props_dic, unk=True)
            else:
                for cp in cp_list:
                    for props in self._vocab[cp]:
                        props_dic = {key: val for key, val, in zip(mdl.DIC_FORM[1:], props)} # ignore the first element, 'surface'
                        lattice.insert(idx, idx + len(cp), cp, props_dic, unk=False)

        return lattice

    def tokenize(self, query):
        lattice = self.createLattice(query)
        # lattice.pprint()

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

        # tokens = ([(b['surface'], b['pos'], 'unk={}'.format(b['unk'])) for b in best_path])

        return best_path
