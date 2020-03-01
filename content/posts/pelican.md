title: Finally getting the hang of working with Pelican!
date: 2020-02-28 09:50
modified: 2020-03-01 00:42
category: Blog
tags: pelican, Makefile, make
slug: pelican
author: Martin Uribe
summary: Nothing beats learning something new than just jumping in and playing around with it!

# Finally getting the hang of working with Pelican

If you've seen my [source repo](https://github.com/clamytoe/clamytoe.github.io) for this site, you know that I followed [Erik O'Shaughnessy's](https://opensource.com/users/jnyjny) *Run your blog on GitHub Pages with Python* [tutorial](https://opensource.com/article/19/5/run-your-blog-github-pages-python).
It's a great tutorial, I specifically love his **one weird trick**, but it leaves so many unanswered questions.
Go read it now if you haven't and we'll pick up where he leaves off.

Luckily he does provide the link to the official [documentation](https://docs.getpelican.com/).
It was through that link that I found Pelican's tutorials [repo](https://github.com/getpelican/pelican/wiki/Tutorials).
Specifically [Matt Makai's](https://www.fullstackpython.com/about-author.html) introductory [tutorial](https://www.fullstackpython.com/blog/generating-static-websites-pelican-jinja2-markdown.html).
I'll admit, that I only skimmed over it, it's kind of long.
I was looking for anything that would jump out at me.
What caught my eye was how simple it all was to automate things with `make`!

I took a quick look at mine and saw what commands were defined.

```zsh
make
Makefile for a pelican Web site

Usage:
   make html                           (re)generate the web site
   make clean                          remove the generated files
   make regenerate                     regenerate files upon modification
   make publish                        generate using production settings
   make serve [PORT=8000]              serve site at http://localhost:8000
   make serve-global [SERVER=0.0.0.0]  serve (as root) to :80
   make devserver [PORT=8000]          serve and regenerate together
   make ssh_upload                     upload the web site via SSH
   make rsync_upload                   upload the web site via rsync+ssh  
   make github                         upload the web site via gh-pages

Set the DEBUG variable to 1 to enable debugging, e.g. make DEBUG=1 html
Set the RELATIVE variable to 1 to enable relative urls
```

Looking at the `Makefile` source is where I noticed that for local development, it just uses the `pelicanconf.py` script, but for publishing it uses `publishconf.py`.
Looking at `publishconf.py` I saw that it actually imports `pelicanconf.py` and then overrides some of the variables.

> **AHA!** This is were I had a eurika moment!

I had noticed a problem with my site.
Whenever I clicked on the header link, instead of taking me back to the home page it would just reload whatever page I was on.
I was able to get around that by just specifying the `SITE_URL` variable in `pelicanconf.py`.
Unfortunately, that broke testing the blog locally because all the links would point to the live site on GitHub!

What I'm trying to say here is that in I was able to resolve both of these issues by making the following changes.

*pelicanconf.py*:

```python
SITEURL = ""
```

*publishconf.py*:

```python
SITEURL = "https://clamytoe.github.io"
```

Another issue that I was having was that I couldn't figure out how to get my `favicon.ico` to be treated as a static file and automatically dumped into the `output` directory.
My solution had been to write a little bash script to copy it over for me, but that was kind of tedious.
But now that I was going to use the `Makefile` I decided to automate it in there!

I added the following lines to it:

```make
FAVICON=$(INPUTDIR)/static/favicon.ico
```

Then after the `html`, `regenerate`, and `publish` commands, I added:

```make
cp $(FAVICON) $(OUTPUTDIR)
```

> NOTE: I had initially added that to all of the commands, but the ones that run the server, don't actually get to that step.

When I *Ctrl+C* out of it, it just exists...

## New workflow

With that all set, things are now much easier and make more sense.
What I would recommend, is to run the `make clean` command and commit it to your `content` branch.
Now you will have a *clean* slate to start with.

You can now add any new content and do the following commands:

```zsh
git add .
git commit -m "Your description..."
git push origin content
```

> NOTE: Of course, only push your files when you're ready to, but you get the idea.

Now you're ready to generate the actual site, here's how that's now done.

### Generate the site

If you just want to generate the site this is the command that you want:

```zsh
make html
```

Then you can either run the Pelican server or the Python one.

#### Pelican server

```zsh
pelican --listen
```

#### Python server

```zsh
cd output
python -m http.server
```

Both of those will make the site accessible at `http://localhost:8000`

### Generate site and preview

Now, if you know that you will be wanting to preview your site, a much better way is to use this command:

```zsh
make devserver
```

Not only will this generate the site, but will also start the Pelican server automagically for you!
This option comes in handy when you are tweaking your site's theme.
I wanted to change the colors on mine and doing it like this automatically detected the changes and served them up.

### Publish the site

This command generates the site using the `publishconf.py` script, so if you specified your site's url in there, it will add it to the generated html pages.
It's nice for making sure all is working correctly and enabling your Google Analytics; if you're into that sort of thing.

```zsh
make publish
```

### Publish and push to github

Now, we're cooking with Crisco!
This command will generate the final site using `publishconf.py`, merge the output into your `master` branch, and push it up the hubs; all in one step!

```zsh
make github
```

### Cleaning up

Now that you've pushed to the hubs, removed the generated files:

```zsh
make clean
```

If you run `git status`, you should see that there are no changes and that you are ready to add more content.
Nice!

## Conclusion

This was a great learning experience for me.
Not only did I update the color scheme of my site, I also fixed some annoying issues that I was having.
Now I don't have to look up any `ghp-import ...` command and things just got a heck of a lot more pleasant.

**In summary**:

```zsh
touch content/posts/new-blog-post.md
vi $_
# write the blog content
git status
git add .
git commit -m "New blog post."
git push origin content
make github
make clean
```

### On a side note

I was also having a weird problem with my search feature.
I had to remove the machine code from my [cryptography](https://clamytoe.github.io/category/cryptography.html) blog post because it was completely screwing up the JavaScript.
Once I got that working, I then noticed that whenever I tried to do a search from any of the category pages, that it was looking for `/category/search.html`.
That page doesn't exists, so I was baffled as to why that was going on.
I took a look at the [pelican-mg](https://github.com/lucachr/pelican-mg) theme's [Jinja](https://palletsprojects.com/p/jinja/) templates and found the issue in `base.html`.
I simply had to add `{{ SITEURL }}` in the `action` part of the form:

```html
<form class="uk-search" action="{{ SITEURL }}/search.html" data-uk-search>
```

Now it works beautifully!

Of course, with me being an upstanding netcitizen, I submitted a [pull request](https://github.com/lucachr/pelican-mg/pull/11) to fix the issue :).
