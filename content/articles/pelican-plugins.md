title: Playing around with adding plugins to Pelican
date: 2020-03-03 13:20
modified: 2020-03-03 13:20
category: Blog
tags: pelican, plugins, latex, css
slug: pelican-plugins
author: Martin Uribe
summary: Wanted to add some extra styling to my blog posts

# Some parts of my blog were looking pretty _blah_

## Math syntax

I've been tweaking my blog like crazy.
Just making minor changes here and there.
I wanted to make things look a little better.

For instance, for my [rescaling]({filename}scaling-values.md) article, I had the following mathematical syntax:

> **ScaledQuantity = (ActualQuantity-MinQuantity)/(MaxQuantity-MinQuantity)**

What the hell is that?
That looks horrible!
I know that markdown supports [Latex](https://www.latex-project.org/), so I looked and found this awesome resource: [Writing Mathematic Formulars in Markdown](http://csrgxtu.github.io/2015/03/20/Writing-Mathematic-Fomulars-in-Markdown/)

ScaledQuantity = \frac{ActualQuantity-MinQuantity}{MaxQuantity-MinQuantity}

Um, not quite there yet.
Something was up.
I searched to see if Pelican had any plugins for rendering math and sure enough, found that [pelican-plugins](https://github.com/getpelican/pelican-plugins) included *render_math*.
I followed the instructions and cloned the repo into my blog directory.
Probably should have dropped it somewhere outside of it, but I added it to my `.gitignore` and it's fine...

I added the following to my `pelicanconf.py` file:

```python
PLUGIN_PATHS = ['./pelican-plugins']
PLUGINS = ['render_math']
```

I tried the previous code once again and was still getting the same results.
After some more reading I found that you have to enclose the mathematical equation within double $.

$$ScaledQuantity = \frac{ActualQuantity-MinQuantity}{MaxQuantity-MinQuantity}$$

> **NICE!**

## Markdown tables

My original tables were so bland that it was almost hard to tell that they were even tables!
Unfortunately I didn't save a screenshot of it, so I can't show you what they looked like, but I can definitely show you the end result!
Thanks to [mockaroo](https://www.mockaroo.com/) I was able to generate some mock data relatively quickly.

|id|first_name|last_name|email|gender|ip_address|
|-:|:---------|:--------|:----|:----:|---------:|
|1|Odilia|O'Meara|oomeara0@yahoo.co.jp|Female|244.53.86.185|
|2|Marcelo|Tunna|mtunna1@netvibes.com|Male|128.140.17.56|
|3|Farris|Roston|froston2@ucla.edu|Male|111.104.78.209|
|4|Gene|Benzies|gbenzies3@nymag.com|Male|67.169.248.21|
|5|Ellsworth|Goodered|egoodered4@hud.gov|Male|227.48.46.133|
|6|Jan|Garnsworth|jgarnsworth5@amazon.de|Male|138.13.211.142|
|7|Robby|Rosenstengel|rrosenstengel6@chron.com|Female|105.76.137.198|
|8|Granthem|Rymer|grymer7@yolasite.com|Male|15.60.66.25|
|9|Claire|Stuther|cstuther8@salon.com|Female|5.36.242.109|
|10|Maggy|Jearum|mjearum9@npr.org|Female|179.12.188.75|

## CSS changes

I hope it doesn't bite me in the butt later on, but I'm forcing the table headers into uppercase. In case anyone is curious, this are the styles that I added to the theme:

```css
table {
  border-collapse: collapse;
  margin-left: auto;
  margin-right: auto;
  width: 90%;
}

td, th {
  border: 1px solid #ddd;
  padding: 8px;
}

tr:nth-child(even){background-color: #f2f2f2;}

tr:hover {background-color: #ddd;}

th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-transform: uppercase;
  font-weight: bold;
  background-color: #607D8B;
  color: white;
}

.math {
  font-size: medium;
}
```

> The default *math* syntax rendering was kind of small, so I changed the `font-size` to *medium*.

## On a side note

I noticed that some of my changes wouldn't take effect until after I removed the *__pycache__* and *.pytest_cache* directories. In order to automate this, I modified my *Makefile*'s `clean` code to the following:

```make
clean:
	[ ! -d $(OUTPUTDIR) ] || rm -rf $(OUTPUTDIR)
	rm -rf __pycache__
	rm -rf .pytest_cache
```

## Conclusion

This web development stuff is pretty complex.
There are lots of moving parts, so I give all of my fellow web developers a high-five for being so awesome!
I can see how this can be pretty overwhelming if you're new to this, but just keep at it and you'll get there.

This old dog can still learn some new tricks!
