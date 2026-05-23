from src.data_loader import load_feats


def get_feat_dictionary():
    """
    Return the feat data as a plain dictionary keyed by the feat name.

    feats.json currently loads as a list containing one dictionary:
    [
        {
            "power attack": {...},
            "crushing blow": {...}
        }
    ]

    This function hides that old data shape from the rest of the code.
    """
    feats = load_feats()
    return feats[0]


def get_feat_names():
    """Return a list of all feat names."""
    feat_dictionary = get_feat_dictionary()
    return list(feat_dictionary.keys())


def has_feat(feat_name):
    """    Return true if the feat exists."""
    feat_dictionary = get_feat_dictionary()
    return feat_name in feat_dictionary


def get_feat(feat_name):
    """
    Return a single feat by name.

    Raises a KeyError if the feat does not exist.
    """
    feat_dictionary = get_feat_dictionary()
    return feat_dictionary[feat_name]


def get_feat_action(feat_name):
    """Return the action field for a feat."""
    feat = get_feat(feat_name)
    return feat["action"]


def get_feat_dictionary_and_names():
    """
    Return feat data and feat names in the same shape as the old featDict() helper.

    This exists as a temporary bridge while old bot cold is being refactored.
    """
    feat_dictionary = get_feat_dictionary()
    feat_names = list(feat_dictionary.keys())
    return [feat_dictionary], feat_names