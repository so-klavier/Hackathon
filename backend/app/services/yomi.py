import pyopenjtalk
import jaconv

def get_furigana_openjtalk(text: str) -> str:
    features = pyopenjtalk.run_frontend(text)

    result = ""

    for feature in features:

        if feature is not None:
            reading = feature["read"]
            result = result + reading

    result = jaconv.kata2hira(result)
    return result