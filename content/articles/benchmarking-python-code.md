title: Benchmarking Python Code
date: 2020-05-04 08:56
category: Python
tags: time, timeit, decorator, functools, wraps
slug: benchmarking-python-code
author: Martin Uribe
summary: How much faster is one implementation compared to another?

# Need to compare which code is faster, read on to find out how

A friend of mine, [Mridu Bhatnagar](https://dev.to/mridubhatnagar), has been posting some really cool articles explaining how she's gone about solving some [LeetCode](https://leetcode.com/) challenges.
They are all interesting, but due to time constraints, I have only attempted to see if I can do a couple of them.

## Move Zeroes

One of the first that I attempted to do was [Move Zeroes](https://dev.to/mridubhatnagar/day-3-move-zeroes-1lbb).
I thought that I was being clever, and sure enough, my initial time test seemed to indicate the same.
That is, until [Suraj Sharma](https://www.linkedin.com/in/sps22/) pointed out to me that once the numbers got bigger, that my implementation would be slower.

I decided to see if it was true, and sure enough, once I increased the starting size number, mine was way slower!!
At any rate, Suraj really liked how I benchmarked the codes, so I decided to share it here.

I wanted to write a script that would indicate, whose code it was currently running with the results to the right of it.
In order to keep it [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself), I decided to use decorators.

Here is what the results look like:

```console
...
Working with 8 zeroes out of 100 numbers
   mridu: 0.0000221729
clamytoe: 0.0000185966
 striker: 0.0000629425
 ...
Working with 10003 zeroes out of 100,000 numbers
   mridu: 8.4343523979
clamytoe: 8.0974295139
 striker: 0.0438303947
```

Full code can be found in this [gist](https://gist.github.com/clamytoe/1fcd47d6f1b5db4d2657623947cd5646).

### Decorator: ID Checker

Part of the requirements for the challenge, was that the same object needed to be modified and not just create a new one.
I'm not really sure if this is the way to do it, but I decided that checking to see if the `id` of the before and after objects were the same was the way to go.

```python
def id_checker(func):
    @wraps(func)
    def wrapper(nums):
        before = id(nums)
        func(nums)
        after = id(nums)

        if DEBUG:
            print(f"{'before':>8}: {before}")
            print(f"{'after':>8}: {after}\n")

        if before != after:
            print("The nums list is not the same!")

    return wrapper
```

Since our functions all only passed the `nums` variable, I decided to just hard code it in instead of using `*args`.
In hindsight, I should have used `*args`.
Sometimes while developing code, I like to throw in a `DEBUG` global variable to turn on/off print statements, so those can be ignored.

### Decorator: Timer

I decided that the easiest way to keep track of whose code was being benchmarked, would be to name each of our functions, with our nicknames.
Then it would be simple enough to extract the function name from within the code.

To time the functions, I created this `timer` decorator.
It's a pretty straight forward timer.
The only unique part is how I extracted the function name.

```python
def timer(func):
    @wraps(func)
    def wrapper(nums):
        start = time()
        func(nums)
        stop = time()
        print(f"{func.__name__:>8}: {stop - start:.10f}")

    return wrapper
```

If you are not familiar with formatting strings within _f-strings_, the `:>8` simply means to right align it and use 8 spaces.
The `:.10f` just means that it's a float value and that I want it to use 10 digits of accuracy.

### Decorating the Functions

Each of the separate functions were decorated in the same manner.
To try and keep this discussion short, I'll only illustrate mine.

```python
@id_checker
@timer
def clamytoe(nums: List[int]):
    count = 0
    while True:
        try:
            nums.remove(0)
            count += 1
        except ValueError:
            break

    for _ in range(count):
        nums.insert(len(nums), 0)
```

The decorators are applied from bottom up.
Meaning that the `@timer` decorator is the first to be ran, followed by the `@id_checker`.
If you are not familiar with decorators, [Dan Bader](https://dbader.org/blog/python-decorators) wrote a nice article on them.

## A Better Way to Benchmark Code

Python comes with the [`timeit`](https://docs.python.org/3/library/timeit.html) module in the standard library.
I don't like that you have to pass the code that you want to benchmark to it as a string, but it works pretty well.

I was working through another one of the challenges that Mridu had completed, [Reverse words in a string III](https://dev.to/mridubhatnagar/day-16-reverse-words-in-a-string-iii-jn3).
When it came time to compare my implementation with hers, I decided to use the `timeit` module.

Here is the script in it's entirety:

```python
from timeit import timeit

setup_code = """
s = "Let's take LeetCode contest"
"""

mridu = """
def reverseWords(s: str) -> str:
    s = s.split()
    s1 = ''
    for x in range(0, len(s)):
        if x == len(s) - 1:
            s1 += s[x][::-1]
        else:
            s1 += s[x][::-1] + ' '
    return s1


reverseWords(s)
"""

clamytoe = """
def reverse_words(s):
    return " ".join([word[::-1] for word in s.split()])


reverse_words(s)
"""


codes = {
    "clamytoe": clamytoe,
    "mridu": mridu
}

for code in codes:
    print(code, timeit(stmt=codes[code], setup=setup_code))
```

The results from running it, look like this:

```console
clamytoe 1.9202047239996318
mridu 3.630925637000473
```

As you can see, in the `timeit` function, I'm passing `stmt` and `setup` variables.
The `stmt` is the actual code to benchmark, while `setup` is used to setup any code that will be required for it to run properly.

You can also pass a `number` variable that allows you to modify how many times the code is ran, with the default being 1,000,000.

I didn't see a way of using decorators here, so I simply used a dictionary to do the identifying for me.

## Summary

I hope that you will now know how to benchmark any of your code.
The first method, using `time` is more suited towards larger code, while `timeit` is good for shorter snippets of code.
The _timeit_ module can do a few more things.
I suggest reading up on it if you're curious.

Until next time, keep on coding!
