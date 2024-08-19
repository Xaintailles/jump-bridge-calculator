import networkx as nx
import json
import os
import pandas as pd


fountain_file_path = r"./data/fountain.json"
jump_bridges_file_path = r"./data/jumpBridges.json"

if os.path.exists(fountain_file_path):
    # Open the fountain.json file
    with open(fountain_file_path, "r") as fountain_file:
        # Load the fountain.json data
        fountain_data = json.load(fountain_file)

def main():

    # Check if both files exist
    if os.path.exists(fountain_file_path) and os.path.exists(jump_bridges_file_path):
        # Open the fountain.json file
        with open(fountain_file_path, "r") as fountain_file:
            # Load the fountain.json data
            fountain_data = json.load(fountain_file)

        # Open the jumpBridges.json file
        with open(jump_bridges_file_path, "r") as jump_bridges_file:
            # Load the jumpBridges.json data
            jump_bridges_data = json.load(jump_bridges_file)

    # Convert the fountain.json data to a DataFrame
    df_original = pd.DataFrame(fountain_data)

    # Explode the DataFrame
    df = df_original.explode('stargates')

    # Reset the index
    df = df.reset_index(drop=True)

    # Only keep 'name' and 'stargates' columns
    df = df.loc[:, ['name', 'stargates']]

    # Convert the jumpBridges.json data to a DataFrame
    jump_bridges_df = pd.DataFrame(jump_bridges_data, columns=['name', 'stargates'])

    # Append the jump bridges DataFrame to the existing DataFrame
    df = pd.concat([df,jump_bridges_df])


    # Create a graph from the DataFrame
    G = nx.from_pandas_edgelist(df, 'name', 'stargates')

    paths = dict(nx.all_pairs_shortest_path(G))

    all_fountain_systems = list(df_original["name"])

    origin = []
    destination = []
    systems_in_between = []
    distance = []

    for s1 in all_fountain_systems:
        for s2 in all_fountain_systems:
            origin.append(s1)
            destination.append(s2)
            systems_in_between.append(paths[s1][s2])
            distance.append(len(paths[s1][s2]))

    test =  pd.DataFrame(
    {'origin': origin,
     'destination': destination,
     'systems_in_between': systems_in_between,
     'distance': distance
    })

    print(test)

main()