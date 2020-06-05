title: Pytest fixtures with tear down
date: 2020-02-19 17:40
modified: 2020-03-12 21:55
category: Python
tags: pytest, fixtures, tear-down
slug: pytest-fixtures
author: Martin Uribe
summary: Figured out how to tear down a pytest fixture

# Setting up pytest fixtures with teardown code

Today after listening to [Brian Okken's](https://twitter.com/brianokken) [Test & Code](https://testandcode.com/) podcast with [Anthony Shaw](https://twitter.com/anthonypjshaw), I was reminded that I wanted to install Anthony's [Python Security Plugin](https://github.com/tonybaloney/pycharm-security) for [JetBrain's PyCharm](https://www.jetbrains.com/pycharm/) IDE.
That was a breeze to install and it just worked out of the box.
I fired it up and it automatically checked my code and called it good.

I then started to write some tests and while checking a password, it alerted me to an issue.
It made a suggestion to fix it, so I accepted and it updated my code and even added the proper import statement!

*FROM*:

```python
    assert dummy.password == "admin"
```

*TO*:

```python
from secrets import compare_digest

import pytest

from passlock.entry import Entry


@pytest.fixture(scope="module")
def dummy():
    return Entry("router", "http://192.168.2.1", "admin", "admin")


def test_entry(dummy):
    assert dummy.name == "router"
    assert dummy.url == "http://192.168.2.1"
    assert dummy.username == "admin"
    assert compare_digest(dummy.password, "admin")
```

Although, this is just a dummy password for testing, it doesn't hurt to build up some good habits!

## On to the fixture tear down

This is when I got to the part where I had to test the creation of my private and public keys.
Since I was creating them for testing and didn't want them around afterwards, I decided that I needed to make them go away after the tests were done.

I was already using fixtures so that I didn't have to recreate the instances of my classes for each test; generating the keys take a bit of time!
I went crazy an opted to make them future proof with **4096-bits**...

The challenge was figuring out how to tear them down.
I did some initial searches and was coming up blank.
I then looked up the pytest guru, [Brian's](https://pythontesting.net/framework/pytest/pytest-fixtures-easy-example/) blog about the topic, but his examples were too simplistic for what I was trying to do.
All they demonstrated was how to print a message, it didn't actually show how to return anything, and then have it torn down afterwards.

*Brian's example*:

```python
from __future__ import print_function
import pytest

@pytest.fixture(scope='module')
def resource_a_setup(request):
    print('\nresources_a_setup()')
    def resource_a_teardown():
        print('\nresources_a_teardown()')
    request.addfinalizer(resource_a_teardown)

def test_1_that_needs_resource_a(resource_a_setup):
    print('test_1_that_needs_resource_a()')

def test_2_that_does_not():
    print('\ntest_2_that_does_not()')

def test_3_that_does(resource_a_setup):
    print('\ntest_3_that_does()')
```

I ended up reading the actual [pytest documentation](https://docs.pytest.org/en/latest/fixture.html); who would have thunk?!
I'll do you guys a solid and cut out the noise and show you what I did:

```python
import pytest


@pytest.fixture(scope="module")
def custom_locker():
    v = Vault(".toe", "tlock")
    yield v
    v.plock.unlink()
    v.pub.unlink()
    v.base.rmdir()


def test_vault_custom(custom_locker):
    assert custom_locker.loc == ".toe"
    assert custom_locker.key_name == "tlock"
```

Setting the `scope` of the fixture to *module* makes it so that it doesn't actually do the tearing down until after all of the tests are completed.
*Perfect!*

The variables in the `Vault` instance are Path objects, so it was simple enough to just `unlink()` the files and then `rmdir()` the directory after it's been emptied.
Of course, I tried removing the directory first, but it wasn't having any of that until it was empty...
