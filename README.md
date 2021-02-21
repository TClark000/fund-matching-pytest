# Fund Matching Model - testing with pytest framework
> A fund matching model based around a simple class with methods as defined by the instructions, and test suite to test for accuracy and correctness using [pytest](https://docs.pytest.org/en/stable/).

## Table of contents
* [Setup](#setup)
* [To Run](#to-run)
* [Things to Do](#things-to-do)
* [Status](#status)
* [Inspiration](#inspiration)
* [Contact](#contact)

## Setup
install python 3.8.x
pip install -r [requirements.txt](requirements.txt)

## To Run

File structure:
```
.
├── README.md
├── matcher
│   ├── __init__.py
│   ├── allocation.py
│   ├── donation.py
│   ├── exceptions.py
│   ├── fund_matcher.py
│   └── match_fund.py
├── requirements.txt
└── tests
    ├── test_donation.py
    ├── test_fund_matcher.py
    └── test_match_fund.py
```

Run pytest:
```pytest -v``` or ```python3 -m pytest -v```

Run pytest with --cov:

```python -m pytest -v --cov-report term-missing --cov=.```

## Things to Do
* Add more tests
* Separate out Allocation State into its own class
* Add persistence to Allocation State
* Make it thread safe

## Status
Project is: _finished_

## Contact
Created by [@teresaclark](https://github.com/tclark000/)