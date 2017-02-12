import re
import numpy as np
from matplotlib import mlab
from matplotlib import pyplot as plt
from sklearn import grid_search, svm

def lenwords(sentence):
    return [re.sub('[^А-ЯЁа-яё]', '', word) for word in sentence.split()]

def features(f):
    sentences = re.split(r'(?:[.]\s*){3}|[.?!]', f)
    vowels = 'АЕЁИОУЫЭЮЯаеёиоуыэюя'
    data = []
    for sentence in sentences:
        if len(lenwords(sentence)) > 0:
            for word in lenwords(sentence):
                amount_vowels = [letter for letter in word if letter in vowels]
            data.append([
                len(''.join(lenwords(sentence))),         # длина предложения в буквах
                len(set(list(''.join(lenwords(sentence))))), # число различных букв в предложении
                len([letter for letter in ''.join(lenwords(sentence)) if letter in vowels]), # число гласных в предложении
                np.mean([len(word) for word in lenwords(sentence)]), # медиана числа букв в слове
                np.mean([len(amount_vowels)]) # медиана числа гласных в слове
            ])
    return data

def pca(data1, data2):
    data = np.vstack((data1, data2))
    p = mlab.PCA(data, True)
    N = len(data1)
    plt.figure()
    plt.plot(p.Y[:N,0], p.Y[:N,1], 'og', p.Y[N:,0], p.Y[N:,1], 'sb')
    plt.show()

def cross_v(fit_data):
    parameters = {'C': (.1, .5, 1.0, 1.5, 1.7, 2.0)}
    gs = grid_search.GridSearchCV(svm.LinearSVC(), parameters)
    gs.fit(fit_data[::, 1:], fit_data[::, 0])
    print('Best result is ',gs.best_score_)
    print('Best C is', gs.best_estimator_.C)
    return gs

def svm_clf(gs, fit_data):
    clf = svm.LinearSVC(C=gs.best_estimator_.C)
    clf.fit(fit_data[::2, 1:], fit_data[::2, 0])
    wrong = 0
    i = 0
    for obj in fit_data[1::2, :]:
        label = clf.predict(obj[1:].reshape(1, -1))
        if label != obj[0]:
            if wrong < 3:
                print('Пример ошибки машины: class = ', obj[0], ', label = ', label, ', экземпляр ', obj[1:])
            wrong += 1
        i += 1
    print (wrong/float(i))

if __name__ == '__main__':
    with open('anna.txt', encoding='utf-8') as f:
        anna = f.read()
    with open('sonets.txt', encoding='utf-8') as f:
        sonets = f.read()

    anna_data = np.array(features(anna))
    sonet_data = np.array(features(sonets))

    pca(anna_data, sonet_data)

    fit_anna = np.array([[0] + el for el in features(anna)])
    fit_sonets = np.array([[1] + el for el in features(sonets)])
    fit_data = np.vstack((fit_anna, fit_sonets))

    gs = cross_v(fit_data)
    svm_clf(gs, fit_data)

