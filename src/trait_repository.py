from src.data_loader import load_traits


def get_trait_dictionary():
    """
    Return the full dictionary from traits.json.

    traits.json currently stores its trait data as a list containing
    one dictionary, so this preserves the legacy data shape while giving
    the rest of the project a clean access point.
    """
    trait_data = load_traits()
    return trait_data[0]


def get_trait_names():
    """
    Return a list of all available trait names.
    """
    return list(get_trait_dictionary().keys())


def get_trait_dictionary_and_names():
    """
    Return the legacy traitDict-style shape:
    full loaded traits data, plus a list of trait names.

    This intentionally mirrors the old traitDict() return format.
    """
    trait_data = load_traits()
    trait_names = list(trait_data[0].keys())
    return trait_data, trait_names


def get_trait(trait_name):
    """
    Return one trait entry by name.
    """
    return get_trait_dictionary()[trait_name]