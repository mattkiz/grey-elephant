from sklearn.neural_network import MLPClassifier
import pickle



categories = pickle.load(open("eBay_categories.pkl","rb"))
model = pickle.load(open("model.pkl", "rb"))
documents = pickle.load(open("document.pkl", "rb"))
training = pickle.load(open("training.pkl", "rb"))
#nn = pickle.load(open("neuralnetwork.pkl","rb"))

clf = MLPClassifier(solver='lbfgs', hidden_layer_sizes=(100,))
X = []
Y = []
index = 0
for key in training.keys():
    print(index/len(training.keys())* 100)
    for sentence in training[key]:
        for word in sentence:
            try:
                vec = model.wv[word]
                X.append(vec)
                Y.append(index)
                print("learn")
            except:
                pass
    index += 1

clf.fit(X,Y)
pickle.dump(clf, open("neuralnetwork.pkl","wb"))

