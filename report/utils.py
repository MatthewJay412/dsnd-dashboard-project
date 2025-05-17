import pickle
from pathlib import Path

# First things first — let's figure out where we are in the project
# We're climbing up two levels to land at the root folder
project_root = Path(__file__).resolve().parent.parent

# From the root, we head into the 'assets' folder to grab our model file
model_path = project_root / "assets" / "model.pkl"


def load_model():
    # Open up the model file and bring that baby back into memory
    with model_path.open("rb") as file:
        model = pickle.load(file)

    # Hand back the loaded model to whoever called us
    return model
