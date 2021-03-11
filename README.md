# Taxi demand prediction

## How to run
1. *conda install --file requirements.txt* or *pip install -r requirements.txt*
2. *python predict.py -i "inputFile" -o "outputFile"*

Input and output files are .json.
Input file should contain array of JSON objects with structure: 
*{ 'lat': latitudeID, 'lng': longitudeID, 'timestamp': 'yyyy-MM-dd HH:mm:ss'}*
Input file example: input.json.

As latitude and longitude in provided dataset are not the real coordinates, but coordinate IDs, only known pickup locations must be used in input file.
Known pickup locations: data/known_locations.txt
