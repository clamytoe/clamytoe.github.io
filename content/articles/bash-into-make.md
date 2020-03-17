title: Bash script into a Makefile
date: 2020-03-17 05:08
modified: 2020-03-17 07:56
category: Misc
tags: bash, make, makefile
slug: bash-into-make
author: Martin Uribe
summary: How to convert a bash script into a Makefile

# Using make can literally make your life easier

So the other day on the Pybites slack channel, [Erik O'Shaughnessy's](https://opensource.com/users/jnyjny) and I were chatting about something and I happened to mention that I had written a bash script to generate documents from Asciidoc files but wanted to create a Makefile to do the same instead.
Without hesitation, he asked for my bash script and got to work!
I don't think that I could have found a better tutorial on the subject if I had looked.
I've looked things up before and nothing is as succinct as what he wrote up for me.

This is all his work and even though I made some changes, the credit for it all goes to him.
I thought it was so great, that I had to share it with everyone because I believe that it can help others get up to speed with creating Makefiles.

## What is a make and what is a Makefile

The [GNU Make](https://www.gnu.org/software/make/) project's page describes it as such:

> GNU Make is a tool which controls the generation of executables and other non-source files of a program from the program's source files.

It basically means that you can automate some common tasks with it.
To illustrate what it can do, I am going to show you how Erik converted my bash script.

## The bash script

Here is the script in all its glory...
It's not much.
It was just thrown together pretty quick and it was getting the job done.

{% include_code ../code/gen_book.sh lang:make :hidelink: %}

## Creating the Makefile

### Variables

This is how you assign a string to a variable name in *Make*.
The variable name doesn't have to be all caps and the equal doesn't have
to be snugged up to the variable name; it's just how I write Makefiles

```make
FILENAME= sop
```

### Referencing variables

`$(IDENTIFIER)` is how you reference a variable in Make, you can use `${}` too, but I prefer `$()`.
If you forget the parentheses or the curly braces, eg `$INDENTIFER`, Make will interpret that as `$I` with `NDENTFIER` appended to it.
Probably not what you are expecting.

```make
SOURCE= $(FILENAME).asc

HTML= $(FILENAME).html
PDF= $(FILENAME).pdf
EPUB= $(FILENAME).epub
MOBI= $(FILENAME).mobi
```

### Shell commands

`$(shell shell command )` is how you invoke a command and save the results to a variable.
It gets kinda tricky since every time you reference `$(DATE)` it will execute the command.
The weird assignment operator `:=` means just assign it one time.

```make
DATE := $(shell date +%Y-%m-%d)
```

Again, calling shell. This time using `AWK` to pull out the revision number.

The *$* needs to be doubled in the command string to keep Make from
trying to expand `$2` into something we didn't intend.

I know there was a `grep`|`cut` in the bash version, I prefer to use `awk` for these kinds of *snip* operations since it's a single process invocation.
Those are easier to deal with in this context since you don't have to worry about any pipe weirdness imposed by Make.

```make
REVISION := $(shell awk '/revnumber/ {print $$2}' $(SOURCE))
```

### Functions / macros

Ok this is a "function" definition that we use to build the various  `ASCIIDOCTOR` invocations.
We could have just written the format specific definitions:

```bash
ADOC_HTML= bundle exec asciidoctor
ADOC_PDF= bundle exec asiidoctor-pdf
...
```

The advantage of this technique is you only have to change the `BUNDLE_EXEC` part if the way you invoke *asciidoctor* changes (I don't know why it would change, but the idea is to isolate stuff that's repeated so you don't have to freaking change it everywhere).

Macro or *function* definition

```make
BUNDLE_EXEC= bundle exec $(1)
```

### Using the macro

```make
ASCIIDOCTOR_HTML= $(call BUNDLE_EXEC,asciidoctor)
ASCIIDOCTOR_PDF=  $(call BUNDLE_EXEC,asciidoctor-pdf)
ASCIIDOCTOR_EPUB= $(call BUNDLE_EXEC,asciidoctor-epub3)
ASCIIDOCTOR_MOBI= $(call BUNDLE_EXEC,asciidoctor-epub3)
```

### Shared flags

Here we build the shared flags used by *asciidoctor* by all invocations.
I use the `+=` assignment to show how you can add to a variable after it's initial assignment.

```make
ADOC_FLAGS= --attribute revnumber=$(REVISION)
ADOC_FLAGS+= --attribute revdate=$(DATE)
```

### Default rule

The default rule that *Make* looks for when invoked as `make` is `all`.
To build the `all` target, *make* builds the dependencies listed after the *rulename:*.

```make
rulename: dep1 dep2 dep3 ... depN
command_0
@command_1
...
comand_n

dep1: subdep1 ...
```

Here, the dependencies for `all` are `$(HTML)`, `$(PDF)`, `$(EPUB)` and `$(MOBI)` which expand in to the names of the files that *asciidoctor* will create.
So `make all` will run the *HTML*, *PDF*, *EPUB* and *MOBI* rules in that order.

```make
all: $(HTML) $(PDF) $(EPUB) $(MOBI)
```

### Rules

The `$(HTML)` rule depends on `$(SOURCE)`, and only executes if the source file has changed or the destination file does not exist.
`$@` is an alias for the name of the rule to be used in the body of the recipe.

By default, *make* will print the command that is being executed to stdout followed by it's output.
To suppress printing the command, preface the command with an `@`.

Lastly, the indention is a **TAB** and not **8 spaces**.
*Make* is an old-school tool and will complain if it doesn't get it's tabs.

```make
$(HTML): $(SOURCE)
	@echo Converting $(SOURCE) to $@
	@$(ASCIIDOCTOR_HTML) $(ADOC_FLAGS) $(SOURCE)

$(PDF): $(SOURCE)
	@echo Converting $(SOURCE) to $@
	@$(ASCIIDOCTOR_PDF) $(ADOC_FLAGS) $(SOURCE)

$(EPUB): $(SOURCE)
	@echo Converting $(SOURCE) to $@
	@$(ASCIIDOCTOR_EPUB) $(ADOC_FLAGS) $(SOURCE)

$(MOBI): ADOC_FLAGS += -a ebook-format=kf8
$(MOBI): $(SOURCE)
	@echo Converting $(SOURCE) to $@
	@$(ASCIIDOCTOR_MOBI) $(ADOC_FLAGS) $(SOURCE)
```

### The debug rule

The debug rule is how I checked to make sure all of the variables I constructed contained the things I thought they should.

```make
debug:
	@echo Rule -> $@
	@echo '          SOURCE: $(SOURCE)'
	@echo '        REVISION: $(REVISION)'
	@echo '            HTML: $(HTML)'
	@echo '             PDF: $(PDF)'
	@echo '            EPUB: $(EPUB)'
	@echo '            MOBI: $(MOBI)'
	@echo '       DOC_FLAGS: $(ADOC_FLAGS)'
	@echo 'ASCIIDOCTOR HTML: $(ASCIIDOCTOR_HTML)'
	@echo ' ASCIIDOCTOR PDF: $(ASCIIDOCTOR_PDF)'
	@echo 'ASCIIDOCTOR EPUB: $(ASCIIDOCTOR_EPUB)'
	@echo 'ASCIIDOCTOR MOBI: $(ASCIIDOCTOR_MOBI)'
```

### The clean rule

Often times we want to restart from a known good "clean" state.
A clean rule is a good place to remove transient files so you ensure that all your dependencies in your project are rebuilt.
In this case we just remove the translated files.
We could use wildcards in this rule like `rm *.html` but this can have unintended consequences if we have other files in HTML format that we didn't want to smoke.

Always be as explicit as possible in clean rules.

```make
clean:
	@/bin/rm -f $(HTML) $(PDF) $(EPUB) $(MOBI)
```

## Modifications and additions that I made

I'm lazy.
I didn't want to have to type out `make sop.pdf` each time that I wanted to generate my document in the pdf format.
So I changed a few things around.

### Default rule modifications

```make
all: html pdf epub mobi
```

### Rules modifications

```make
html: $(SOURCE)
	@echo Converting $(SOURCE) to $(HTML)
	@$(ASCIIDOCTOR_HTML) $(ADOC_FLAGS) $(SOURCE)

pdf: $(SOURCE)
	@echo Converting $(SOURCE) to $(PDF)
	@$(ASCIIDOCTOR_PDF) $(ADOC_FLAGS) $(SOURCE)

epub: $(SOURCE)
	@echo Converting $(SOURCE) to $(EPUB)
	@$(ASCIIDOCTOR_EPUB) $(ADOC_FLAGS) $(SOURCE)

mobi: ADOC_FLAGS += -a ebook-format=kf8
mobi: $(SOURCE)
	@echo Converting $(SOURCE) to $(MOBI)
	@$(ASCIIDOCTOR_MOBI) $(ADOC_FLAGS) $(SOURCE)
```

With those changes I can now recreate any of those formats by simply specifying them, as so: `make pdf`

### The help rule

I also added a help rule.
I've found it to be very useful for letting users know what commands are available and what they do.
Mostly it's for me, I forget everything...

```make
help:
	@echo 'Makefile for generating documents from Asciidoc source files              '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make help                           prints this message                '
	@echo '   make all                            generates all of the formats       '
	@echo '   make clean                          remove the generated file formats  '
	@echo '   make debug                          prints all of the variables used   '
	@echo '   make html                           (re)generates an html file         '
	@echo '   make pdf                            (re)generates a pdf file           '
	@echo '   make epub                           (re)generates an epub file         '
	@echo '   make mobi                           (re)generates a mobi file          '
	@echo '   make -n                             prints the commands without        '
	@echo '                                       executing them                     '
	@echo '                                                                          '
```

## Conclusion

*Make* is a very versatile program and can be used for many more things.
For instance Erik uses it to launch his kids Minecraft server!
Now that I know how a *Makefile* is constructed, I will be able to automate other parts of my daily tasks!

The *MOBI* format kept failing on me.
It would leave behind a file with the extension *-kf8.epub* and never generate the *.mobi* one.
My guess is that I need to install some kind of Amazon Kindle app or something, so I removed it from the `all` rule to prevent it from generating by default.

This is the final file:

```make
# Makefile

# Main project file name
FILENAME= pnc-sop

# Variables used
SOURCE= $(FILENAME).asc

HTML= $(FILENAME).html
PDF= $(FILENAME).pdf
EPUB= $(FILENAME).epub
MOBI= $(FILENAME).mobi

# Store the current date
DATE := $(shell date +%Y-%m-%d)

# Grab revision number from the source document
REVISION := $(shell awk '/revnumber/ {print $$2}' $(SOURCE))

# Macro or 'function' definition
BUNDLE_EXEC= bundle exec $(1)

# Assigning the macro
ASCIIDOCTOR_HTML= $(call BUNDLE_EXEC,asciidoctor)
ASCIIDOCTOR_PDF=  $(call BUNDLE_EXEC,asciidoctor-pdf)
ASCIIDOCTOR_EPUB= $(call BUNDLE_EXEC,asciidoctor-epub3)
ASCIIDOCTOR_MOBI= $(call BUNDLE_EXEC,asciidoctor-epub3)

# Shared flags
ADOC_FLAGS= --attribute revnumber=$(REVISION)
ADOC_FLAGS+= --attribute revdate=$(DATE)

# Define the make commands
all: html pdf epub

# Define each of the commands and specifying their outputs
html: $(SOURCE)
	@echo Converting $(SOURCE) to $(HTML)
	@$(ASCIIDOCTOR_HTML) $(ADOC_FLAGS) $(SOURCE)

pdf: $(SOURCE)
	@echo Converting $(SOURCE) to $(PDF)
	@$(ASCIIDOCTOR_PDF) $(ADOC_FLAGS) $(SOURCE)

epub: $(SOURCE)
	@echo Converting $(SOURCE) to $(EPUB)
	@$(ASCIIDOCTOR_EPUB) $(ADOC_FLAGS) $(SOURCE)

mobi: ADOC_FLAGS += -a ebook-format=kf8
mobi: $(SOURCE)
	@echo Converting $(SOURCE) to $(MOBI)
	@$(ASCIIDOCTOR_MOBI) $(ADOC_FLAGS) $(SOURCE)

# Use debug rule to check that all of the variables were
# constructed properly.
debug:
	@echo Rule -> $@
	@echo '          SOURCE: $(SOURCE)'
	@echo '        REVISION: $(REVISION)'
	@echo '            HTML: $(HTML)'
	@echo '             PDF: $(PDF)'
	@echo '            EPUB: $(EPUB)'
	@echo '            MOBI: $(MOBI)'
	@echo '       DOC_FLAGS: $(ADOC_FLAGS)'
	@echo 'ASCIIDOCTOR HTML: $(ASCIIDOCTOR_HTML)'
	@echo ' ASCIIDOCTOR PDF: $(ASCIIDOCTOR_PDF)'
	@echo 'ASCIIDOCTOR MOBI: $(ASCIIDOCTOR_MOBI)'
	@echo 'ASCIIDOCTOR EPUB: $(ASCIIDOCTOR_EPUB)'

# Simple help menu showing what commands are available
# and what they do.
help:
	@echo 'Makefile for generating documents from Asciidoc source files              '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make help                           prints this message                '
	@echo '   make all                            generates all of the file formats  '
	@echo '   make clean                          remove the generated files         '
	@echo '   make debug                          prints all of the variables used   '
	@echo '   make html                           (re)generates an html file         '
	@echo '   make pdf                            (re)generates a pdf file           '
	@echo '   make epub                           (re)generates an epub file         '
	@echo '   make mobi                           (re)generates a mobi file          '
	@echo '   make -n                             prints the commands without        '
	@echo '                                       executing them                     '
	@echo '                                                                          '

# Specify clean-up rules.
clean:
	@/bin/rm -f $(HTML) $(PDF) $(EPUB) $(MOBI) $(FILENAME)-kf8.epub

```

> Thanks again Erik!
