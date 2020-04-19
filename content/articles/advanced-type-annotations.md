title: Advanced type annotations
date: 2020-04-19 12:20
category: Python
tags: annotations, hinting, properties, class methods, inheritance
slug: advanced-type-annotations
author: Martin Uribe
summary: Some concrete examples on how to type hint more advanced class objects

# How to add type annotations to Python dataclasses

During the COVID19 outbreak, a lof of companies are either giving away free books, tutorials, or access their training material.
One such company is Pluralsight.
For the whole month of April 2020, they have given everyone free access to their complete library!
The content is just awesome, some of the best I've seen.
I have been working through their [Python - Beyond the Basics](https://app.pluralsight.com/library/courses/python-beyond-basics) when I came across their section on *Properties and Class Methods*.

## Sample program

Their sample program was pretty cool:

{% include_code ../code/og-shipping.py lang:python :hidelink: %}

As you can see, there is a lot going on in that code.

> I don't know how you guys learn, but I just can't sit and watch a video; I have to be actually coding along to make it stick.

That bit of code seemed simple enough, so I decided to kick it up a notch by using *dataclasses* and *type annotations*!

## Hell week

Hence my journey into hell week commenced!

To make it an even better learning experience, I decided to only read the documentation on [type annotations](https://docs.python.org/3/library/typing.html). I lost track of how many hours I spent trying to get it, not only to work, but to get *mypy* to NOT complain about any part of it.

After a few days of pulling out my hair I relaxed that restriction, but to my surprise, there really wasn't that much documentation on how to do what I wanted to do!
Mostly every example out there dealt with type hinting normal classes, not dataclasses!

In the end I discovered that *mypy* doesn't support type annotations of [settable property variables](https://github.com/python/mypy/issues/220)!
Oh well, I could not get a clean *mypy* run in the end, but I definitely learned a lot about type hinting the rest of the code.

## What I ended up with

Instead of going step by step over every bit of the code, I'm just going to present it in its entirety and let you soak it in.
I'll talk about the parts that gave me the most problems and point out the parts were I learned things.

{% include_code ../code/shipping.py lang:python :hidelink: %}

## Learning points

Let's start at the top.

### The class definitions

{% include_code ../code/shipping.py lang:python lines:7-17 :hidelink: %}

This class definition is filled with lots of good nuggets.

* Class variables must be annotated with *ClassVar*
* *contents* is not enforced because of the use of the classmethod *create_empty*, so it was annotated with *Optional*
* *args* and *kwargs* were declared because PyCharm was complaining about them not being there, even though the code will run fine without them
* *args* are *tuples*, not a *list*!
* *kwargs* are just *dicts* not a list of them

### \_\_post_init__

In this method we generate the custom **bic** code that's made up from the *owner_code*, the *serial* number, and a *category* code.

{% include_code ../code/shipping.py lang:python lines:18-22 :hidelink: %}

### Volume property

The *@classmethods* remained the same, so we're not going to discuss those.
Things start to get interesting when it comes to the *volume_ft3* property though.

{% include_code ../code/shipping.py lang:python lines:41-47 :hidelink: %}

As you can see, the logic for the volume calculation was extracted from the property and moved into its own method.

> This will come in handy later on when this method gets overwritten in another class that inherits from this one.

### Inheriting the main class

Now comes the fun parts!
When you normally inherit a class, you usually call *super()* to initialize some of the variables.
Not so with *dataclasses*!
This is one point where I was pulling my hair out to figure out how to declare these and it turned out to be simpler than I thought.
Just don't!

{% include_code ../code/shipping.py lang:python lines:49-55 :hidelink: %}

The part that gave me the biggest headache was declaring the **required** *celcius* variable because *celsius* is also a property value!

We also don't want the user to be able to manually set the *celsius* value, because it has to be within a set range, so the "private" variable *_celsius* was created.

{% include_code ../code/shipping.py lang:python lines:52-52 :hidelink: %}

Pay attention to the usage of *field*.
This tells the class constructor not only to not expect a value to be passed during initialization, but also to not display this variable through *repr*!

### Property init values

Here is how you handle *init* values that are also properties of the class.
A more detailed explanation can be found in this wonderful write-up: [Reconciling Dataclasses and Properties in Python](https://florimond.dev/blog/articles/2018/10/reconciling-dataclasses-and-properties-in-python/)

{% include_code ../code/shipping.py lang:python lines:70-83 :hidelink: %}

As with the *property* value in the main class, the logic was also extracted from the *property* and moved into its own method.
I also had to add a *try/except* clause to it because for some reason, if the *celcius* value was not passed during initialization, it would try and initialize it with a *None* value but would give some obscure error message...

### Overwriting methods

Next we'll skip to overwriting the *_calc_volume* method.

{% include_code ../code/shipping.py lang:python lines:96-98 :hidelink: %}

Notice how we call the parent class with *super()* but that we also use the class name while retrieving the class variable *FRIDGE_VOLUME_FT3*!

## Conclusion

There's a lot going on here, and it might take you a while to grok it all, but keep at it and I can assure you that the next time that you need to annotate some *dataclasses*, this information will come in really handy!
