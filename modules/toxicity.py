from detoxify import Detoxify

model = Detoxify('original')

def analyze_text(text):
    result = model.predict(text)
    return result