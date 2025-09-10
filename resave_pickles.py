import pickle

pickle_files = ["model/movie_list.pkl", "model/similarity.pkl", "model/movie_dict.pkl"]

for file_path in pickle_files:
    # Load the pickle
    with open(file_path, "rb") as f:
        data = pickle.load(f)
    # Re-save with highest protocol
    with open(file_path, "wb") as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
    print(f"{file_path} re-saved successfully ✅")
