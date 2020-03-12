title: Testing ABC's with abstractmethods with Pytest
date: 2020-03-12 10:31
category: Python
tags: python, pytest, abc, abstractmethods
slug: testing-abc's-with-abstractmethods-with-pytest
author: Martin Uribe
summary: What I had to do to get 100% coverage on my tests

# Testing ABC's with abstractmethods with Pytest

I was working on writing a new code challenge for [Codechalleng.es](https://codechalleng.es/) the other day.
It's based on [inheritance and composition](https://realpython.com/inheritance-composition-python/) and uses [Abstract Base Classes](https://docs.python.org/3/library/abc.html) to define the interfaces that should be implemented in classes derived from it.

I was just finishing up with the tests and everything was passing.
Then when I checked the code coverage on it, I saw that it was complaining about my *Site* class, which is the one derived from ABC has several methods decorated as *abstractmethods*.
[Coverage](https://coverage.readthedocs.io/en/coverage-5.0.3/) wanted me to test the `pass` statements on them...

Initial searches didn't turn up much, so I posed the question in PyBites slack channel.
The best suggestion was to use the *dis* module and test it that way, but since it's not really running the code, coverage still counts it as untested.

## How to test abstract methods

Finally I came across this post on [reddit]() that had the solution. Here is what the code looks like, with doctrings removed:

```python
class Site(ABC):

    web: Web

    def find_table(self, loc: int = 0) -> str:
        return self.web.soup.find_all("table")[loc]

    @abstractmethod
    def parse_rows(self, table: Soup) -> List[Any]:
        pass

    @abstractmethod
    def polls(self, table: int = 0) -> List[Any]:
        pass

    @abstractmethod
    def stats(self, loc: int = 0):
        pass
```

Here is how you go about testing them:

```python
def test_site(test_file):
    Site.__abstractmethods__ = set()

    @dataclass
    class Dummy(Site):
        web: Web

    url = "https://projects.fivethirtyeight.com/polls/"
    test_web = Web(url, test_file)
    d = Dummy(test_web)
    table = d.find_table()
    rows = d.parse_rows(table)
    polls = d.polls()
    stats = d.stats()
    assert d.web.file.name == "test.html"
    assert isinstance(Site, ABCMeta)
    assert rows is None
    assert polls is None
    assert stats is None
```

As you can see, the way to accomplish this is to override `__abstractmethods__`.
Basically tricking it into thinking that it doesn't have any.
The last three *asserts* then verify that `None` is being returned.

```
============================= test session starts ==============================
platform linux -- Python 3.7.3, pytest-4.4.0, py-1.8.0, pluggy-0.9.0 -- /home/mohh/anaconda3/envs/pybites/bin/python
cachedir: .pytest_cache
rootdir: /home/mohh/Projects/team-charlie/020
plugins: cov-2.8.1, asyncio-0.10.0
collected 8 items                                                              

test_composition.py::test_file_class PASSED                              [ 12%]
test_composition.py::test_web PASSED                                     [ 25%]
test_composition.py::test_web_bad_url PASSED                             [ 37%]
test_composition.py::test_poll PASSED                                    [ 50%]
test_composition.py::test_leaderboard PASSED                             [ 62%]
test_composition.py::test_rcp_stats PASSED                               [ 75%]
test_composition.py::test_nyt PASSED                                     [ 87%]
test_composition.py::test_site PASSED                                    [100%]

----------- coverage: platform linux, python 3.7.3-final-0 -----------
Name             Stmts   Miss  Cover   Missing
----------------------------------------------
composition.py     107      0   100%


=========================== 8 passed in 7.22 seconds ===========================
```

Success!

## Conclusion

If you're ever faced with having to write test for abstract methods, simply override the `__abstractmethods__` of the ABC class!
Definitely something to keep in your toolbox.

Until next time, happy coding!
