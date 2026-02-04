from app.services.bucket_classifier import infer_bucket


def test_infer_bucket_from_category():
    assert infer_bucket(category="rent", note=None) == "necessary"
    assert infer_bucket(category="dining_out", note=None) == "controllable"
    assert infer_bucket(category="entertainment", note=None) == "unnecessary"


def test_infer_bucket_from_note_keywords():
    assert infer_bucket(category=None, note="Netflix monthly") == "unnecessary"
    assert infer_bucket(category=None, note="Electricity bill") == "necessary"
    assert infer_bucket(category=None, note="Coffee with friends") == "controllable"


def test_infer_bucket_unknown_returns_none():
    assert infer_bucket(category="some_new_category", note="random") is None
