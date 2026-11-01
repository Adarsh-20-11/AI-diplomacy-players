
def test_import_needle():
    try:
        import needle
        assert needle.__version__
    except ImportError as e:
        print("Could not import needle.\nStack Trace: "+e)
