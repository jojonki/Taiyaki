import pickle


def savePickle(d, path):
    # print('save pickle to', path)
    with open(path, mode='wb') as f:
        pickle.dump(d, f)


def loadPickle(path):
    # print('load', path)
    with open(path, mode='rb') as f:
        return pickle.load(f)
