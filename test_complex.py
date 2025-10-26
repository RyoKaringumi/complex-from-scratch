
def test_complex_creation() -> None:
    from complex import Complex

    c = Complex(3.0, 4.0)
    assert c.real == 3.0
    assert c.imag == 4.0
