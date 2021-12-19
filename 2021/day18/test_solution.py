from solution import parse_number


# To run:
# $ python3 -m pytest
def test_parse() -> None:
    assert (str(
        parse_number("[[[[7,1],[0,0]],[6,[8,2]]],[8,[3,8]]]")) ==
            "[[[[7,1],[0,0]],[6,[8,2]]],[8,[3,8]]]")
