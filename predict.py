import argparse
import pickle
import joblib
import json
import sys
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input file path', required=True)
    parser.add_argument('-o', '--output', help='Output file path', default='output.json')
    args = parser.parse_args()
    return (args.input, args.output)

def main():
    inp, outp = parse_args()
    try:
        model, map_locations, map_area, map_time = load_models()
    except Exception as e:
        stop_script('Unable to load models: ', e)
    try:
        f = load_file(inp)
    except Exception as e:
        stop_script('Error druring opening input file: ', e)
    try:
        X = preprocess(f, map_locations, map_area, map_time)
    except Exception as e:
        stop_script('Wrong data provided: ', e)
    try:
        prediction = predict(X, model)
    except Exception as e:
        stop_script('Error during prediction: ', e)
    try:
        output = generate_output(f, prediction)
        save_output(output, outp)
        print(f'Predictions saved to {outp}')
    except Exception as e:
        stop_script('Error druring saving output file: ', e)

def load_models():
    with open('models/model.pkl', 'rb') as file:
        model = joblib.load(file)
    with open('models/locations.pkl', 'rb') as file:
        map_locations = pickle.load(file)
    with open('models/area.pkl', 'rb') as file:
        map_area = pickle.load(file)
    with open('models/time.pkl', 'rb') as file:
        map_time = pickle.load(file)
    return (model, map_locations, map_area, map_time)

def load_file(path):
    with open(path, 'r') as json_file:
        return json.load(json_file)

def preprocess(data, map_locations, map_area, map_time):
    pickup = []
    timestamp = []
    for d in data:
        pickup.append((d['lat'], d['lng']))
        timestamp.append(d['timestamp'])
    df = pd.DataFrame({'pickup_location': pickup, 'timestamp': timestamp})
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['pickup_location'] = df['pickup_location'].map(map_locations)
    df['pickup_community_area'] = df['pickup_location'].map(map_area)
    df['time_bin'] = df['timestamp'].dt.floor('30min').dt.time.map(map_time)
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    if (df['pickup_location'].isnull().any()):
        raise ValueError('Wrong coordinates')
    df.drop(columns=['timestamp'], inplace=True)
    return df

def predict(X, model):
    prediction = model.predict(X)
    rounded = [round(p) for p in prediction]
    return rounded

def generate_output(data, prediction):
    for d, p in zip(data, prediction):
        d['demand'] = p
    return data

def save_output(output, path):
    with open(path, 'w+') as outfile:
        json.dump(output, outfile)

def stop_script(message, exception):
    print(message, exception)
    sys.exit()

main()

# TODO declare custom exceptions
# I did not export reusable code in separeate module because it is like 6 lines of it in this script.