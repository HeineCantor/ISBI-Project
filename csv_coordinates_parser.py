import pandas as pd
from tqdm import tqdm

def latLongConvert(x : str):
    sgn = +1
    if x[-1] == 'S' or x[-1] == 'W':
        sgn = -1

    return float(x[:-1]) * sgn


cityDataframe = pd.read_csv("./Datasets/GlobalLandTemperaturesByMajorCity.csv")
cityDataframe["Latitude"] = [latLongConvert(x) for x in tqdm(cityDataframe["Latitude"].tolist())]
cityDataframe["Longitude"] = [latLongConvert(x) for x in tqdm(cityDataframe["Longitude"].tolist())]

cityDataframe.to_csv("converted.csv")