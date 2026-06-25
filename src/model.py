class Model:
    def __init__(self):
        self.vectorizer = None
        self.clf = None

    def predict(self, text: str):
        return "positive"


def load_model():
    return Model()