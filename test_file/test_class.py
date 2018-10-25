class TestClass:
    def test_one(self):
        x = "this"
        assert 'h' in x

    def test_two(self):
        x = "check this out! hello!"
        assert hasattr(x, 'check')

