title: Cleaning up Anaconda environment.yml files
date: 2020-03-24 07:46
category: Python
tags: anaconda, conda, env, virtual
slug: cleaning-up-anaconda-environment_yml-files
author: Martin Uribe
summary: Cleaning up Anaconda exported environment files is pretty tedious work

# Recreating virtual environments with Anaconda

I love working with Anaconda.
It makes things so much easier.
I enjoy using it so much that I even wrote a guest post article on [PyBit.es](https://pybit.es/guest-anaconda-workflow.html) about my workflow.
It goes into much more detail on the subject, but I'll cover a few basics here.

With that being the case, there is one aspect of it that I really hate and that is creating the `environment.yml` project file for distribution.

## Table of Contents

* [What is an environment.yml file](#what-is-an-environment.yml-file)
* [How do you use an environment.yml file](#how-do-you-use-an-environment.yml-file)
* [How do you create and environment.yml file](#how-do-you-create-and-environment.yml-file)
* [How to prepare an environment.yml file for mass use](#how-to-prepare-an-environment.yml-file-for-mass-use)
* [How to use the cleanup-yml.py script](#how-to-use-the-cleanup-yml.py-script)
* [How to create an environment.yml without version lock in](#how-to-create-an-environment.yml-without-version-lock-in)
* [Conclusion](#conclusion)

## <a name="what-is-an-environment.yml-file"></a>What is an environment.yml file

Think of it as the equivalent of python's `requirements.txt`.
With it, anyone can pick up your project and have a working environment up in no time and with all package dependencies resolved!

By convention, just like the `requirements.txt` file, the file is usually named *environment.yml* although it can be any name you wish.
Services like [binder](https://mybinder.org/) will automatically know that you are using an Anaconda environment when it detects it and automatically generate the environment from it.

## <a name="how-do-you-use-an-environment.yml-file"></a>How do you use an environment.yml file

Replicating a working virtual environment from the file is relatively simple.
If you or the author of the project stuck to conventions and named it *environment.yml*, then issuing the following command will get you up and running:

```zsh
conda env create
```

But what if it's named something else, like for example *secret_sauce.yml*?
in that case you will have to specify the name of the file while using the `-f` flag, like ah so:

```zsh
conda env create -f secret_sauce.yml
```

Anaconda will then create the virtual environment.
It will download and install the packages that are listed in the yml file.

## <a name="how-do-you-create-and-environment.yml-file"></a>How do you create and environment.yml file

So let's say that you want to be able to recreate your current working environment and you want an exact copy, with matching package versions and everything.
It's really easy to do, you simply issue the following command:

```zsh
conda env export > environment.yml
```

The generated file can be used to recreate your virtual environment exactly if you ever had the need.
One draw back is that, in it's current form, it only works for your specific hardware setup!

## <a name="how-to-prepare-an-environment.yml-file-for-mass-use"></a>How to prepare an environment.yml file for mass use

To make it so that others can use it, whether they are on a Windows or a Mac, you will have to prepare the file.
In it's current state it looks something like this:

```yml
name: dataviz
channels:
  - conda-forge
  - defaults
dependencies:
  - _libgcc_mutex=0.1=conda_forge
  - _openmp_mutex=4.5=0_gnu
  - appdirs=1.4.3=py_1
  - attrs=19.3.0=py_0
  - backcall=0.1.0=py_0
  - black=19.10b0=py37_0
  - bleach=3.1.3=pyh8c360ce_0
  - bokeh=2.0.0=py37hc8dfbb8_0
  - bzip2=1.0.8=h516909a_2
  - ca-certificates=2019.11.28=hecc5488_0
  - certifi=2019.11.28=py37hc8dfbb8_1
  - click=7.1.1=pyh8c360ce_0
  ...
  - yaml=0.2.2=h516909a_1
  - zeromq=4.3.2=he1b5a44_2
  - zipp=3.1.0=py_0
  - zlib=1.2.11=h516909a_1006
  - zstd=1.4.4=h3b9ef0a_2
  - pip:
    - geoplotlib==0.3.2
    - pyqt5-sip==4.19.18
    - pyqtwebengine==5.12.1
prefix: /home/mohh/anaconda3/envs/dataviz


```

> **NOTE**: I've shortened it because it was pretty long...

As I described in my [workflow](https://pybit.es/guest-anaconda-workflow.html#prepare_environment_yaml_for_distribution) article, you have to remove everything after the second **=** sign and the **prefix:** line towards the end.

This particular one had **165** lines!!
As you can imagine, that can get pretty tedious.
What would any other Python Ninja do in this situation?
That's write, hack together a quick little script to do it for you, and that is what I have done.

You can find the script on my gist account here: [cleanup-yml.py](https://gist.github.com/clamytoe/5019dd7c60688be9be7ccc3132c391ed)

*cleanup-yml.py*:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path


def clean_yaml(file: Path, skip: int = 5) -> str:
    """Cleans up an Anaconda environment file

    The contents of the file are generated by issuing the following
    command from within an activated Anaconda environment:

        conda env export > environment.yml

    Arguments:
        file {Path} -- Path file object that contains the exported env
        skip {int} -- Number of lines to skip/leave alone at the top
                      of the file

    Returns:
        str -- cleaned up data
    """
    cleaned = ""
    with file.open() as f:
        for n, line in enumerate(f.readlines()):
            if n < skip or "==" in line or "pip:" in line:
                cleaned += line
            elif line.startswith("prefix:"):
                cleaned += "\n"
            elif "=" not in line:
                cleaned += line.rstrip()
            else:
                keep, _ = line.rsplit("=", 1)
                cleaned += f"{keep}\n"
    return cleaned


def save(file: Path, data: str):
    """Saves the data to the file Path object

    Arguments:
        file {Path} -- Path file object to save the data to
        data {str} -- The data to save to the file object
    """
    file.write_text(data)


if __name__ == "__main__":
    file = Path("environment.yml")
    parsed = clean_yaml(file)
    save(file, parsed)

```

## <a name="how-to-use-the-cleanup-yml.py-script"></a>How to use the cleanup-yml.py script

Using the script is simple.
I like to put my scripts into the `~/bin/` directory that I have in my home folder.
Since that directory will automatically be in my path, I will be able to run the script from anywhere on my system.
Make sure to make the script executable: `chmod +x ~/bin/cleanup-yml.py`

To use it, you must run it from your project's home directory so that it can find the *environment.yml* file.
There is no output; I guess I should have added a message stating that the modification were completed...
A typical workflow would be as follows once you've setup your virtual environment by hand:

```zsh
conda env export > environment.yml
cleanup-yml.py
pip freeze > requirements.txt
```

## <a name="how-to-create-an-environment.yml-without-version-lock-in"></a>How to create an environment.yml without version lock in

If you don't really care about having an exact replica of your environment.
Meaning that you don't care about the package versions, and you just want the environment with the latest version of the packages installed.

This command is what you want:

```zsh
conda env export --from-history > environment.yml
```

This will generate an a yml file with just the packages that you specified and non of their dependencies.

Here's an example one:

```yml
name: dataviz
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.7
  - pandas
  - seaborn
  - jupyterlab
  - squarify
  - bokeh
  - matplotlib
  - pyglet
  - numpy
  - flake8
  - isort
  - black
  - pytest
  - pytest-cov
  - mypy
prefix: /home/mohh/anaconda3/envs/dataviz

```

For that one, you would just need to remove the **prefix** line at the end before distributing.

## <a name="conclusion"></a>Conclusion

Writing that cleanup script is really going to improve my workflow, and I hope that it will do the same for yours!

In normal Python, using the *requirements.txt* file, you would first create your virtual environment, activate it, and then install the packages with the requirements.txt file.
With Anaconda, it's all done in one step.
You also have the option of choosing different versions of Python, plus you get the guarantee that there will be no package conflicts.

> On a side note, it feels great to write a script, with type hinting to boot, and not have [black](https://github.com/psf/black), [flake8](https://gitlab.com/pycqa/flake8), [isort](https://github.com/timothycrosley/isort), or [mypy](https://github.com/python/mypy) complain about any of it!
Sure helps to shake that importer syndrome a bit...