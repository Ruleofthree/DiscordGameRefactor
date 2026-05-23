from original.onMSGUtils import featDict


def test_legacy_featdict_returns_old_shape():
    feat_dictionary, feat_names = featDict()

    assert isinstance(feat_dictionary, list)
    assert isinstance(feat_dictionary[0], dict)
    assert isinstance(feat_names, list)
    assert "power attack" in feat_dictionary[0]
    assert "power attack" in feat_names