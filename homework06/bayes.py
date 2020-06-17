import math


class NaiveBayesClassifier:

    def __init__(self, alpha=1):
        self.a = alpha
        self.word_dict = dict()
        self.class_inds = dict()
        self.y = None
        self.doc_prob = None
        self.n_classes = None

    def fit(self, x, y):
        self.y = list(set(y))
        words = []
        for doc in x:
            words.extend(doc.split(' '))
        d = len(set(words))
        for c in y:
            if c not in self.class_inds.keys():
                self.class_inds[c] = len(self.class_inds) - 1
        self.n_classes = len(self.class_inds)
        for i, doc in enumerate(x):
            for word in doc.split():
                if word not in self.word_dict.keys():
                    self.word_dict[word] = [0 for _ in range(self.n_classes)]
                self.word_dict[word][self.class_inds[y[i]]] += 1
        for word in self.word_dict.keys():
            n_word = sum(self.word_dict[word])
            for i, n_word_in_class in enumerate(self.word_dict[word]):
                self.word_dict[word][i] = math.log((n_word_in_class + self.a) / (n_word + self.a * d), math.e)

    def predict(self, x):
        self.doc_prob = list()
        for doc in x:
            probs = list()
            for c in self.class_inds.keys():
                probs.append(math.log(1 / self.n_classes, math.e) + sum([
                    self.word_dict[word][self.class_inds[c]]
                    if word in self.word_dict.keys()
                    else 0
                    for word in doc.split()
                ]))
            self.doc_prob.append(probs.index(max(probs)))
        return [self.y[c] for c in self.doc_prob]

    def score(self, x_test, y_test):
        prediction = self.predict(x_test)
        c = sum([1 for i, p in enumerate(prediction) if p == y_test[i]])
        return c / len(prediction)


if __name__ == '__main__':
    import csv
    import string

    with open("data/SMSSpamCollection") as f:
        data = list(csv.reader(f, delimiter="\t"))

    def clean(s):
        translator = str.maketrans("", "", string.punctuation)
        return s.translate(translator)


    spam_x, spam_y = [], []
    for target, msg in data:
        spam_x.append(msg)
        spam_y.append(target)
    spam_x = [clean(x).lower() for x in spam_x]
    x_train, y_train, spam_x_test, spam_y_test = spam_x[:3900], spam_y[:3900], spam_x[3900:], spam_y[3900:]
    model = NaiveBayesClassifier()
    model.fit(x_train, y_train)
    print(model.score(spam_x_test, spam_y_test))
