---
title: CommonMark Spec
author: John MacFarlane
version: 0.29  [downloaded from GitHub](https://github.com/commonmark/commonmark-spec/blob/master/spec.txt)
date: '2019-04-06'
license: '[CC-BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/)'
...

# Introduction

## What is Markdown?

Markdown is a plain text format for writing structured documents,
based on conventions for indicating formatting in email
and usenet posts.  It was developed by John Gruber (with
help from Aaron Swartz) and released in 2004 in the form of a
[syntax description](http://daringfireball.net/projects/markdown/syntax)
and a Perl script (`Markdown.pl`) for converting Markdown to
HTML.  In the next decade, dozens of implementations were
developed in many languages.  Some extended the original
Markdown syntax with conventions for footnotes, tables, and
other document elements.  Some allowed Markdown documents to be
rendered in formats other than HTML.  Websites like Reddit,
StackOverflow, and GitHub had millions of people using Markdown.
And Markdown started to be used beyond the web, to author books,
articles, slide shows, letters, and lecture notes.

What distinguishes Markdown from many other lightweight markup
syntaxes, which are often easier to write, is its readability.
As Gruber writes:

> The overriding design goal for Markdown's formatting syntax is
> to make it as readable as possible. The idea is that a
> Markdown-formatted document should be publishable as-is, as
> plain text, without looking like it's been marked up with tags
> or formatting instructions.
> (<http://daringfireball.net/projects/markdown/>)

The point can be illustrated by comparing a sample of
[AsciiDoc](http://www.methods.co.nz/asciidoc/) with
an equivalent sample of Markdown.  Here is a sample of
AsciiDoc from the AsciiDoc manual:

```
1. List item one.
+
List item one continued with a second paragraph followed by an
Indented block.
+
.................
$ ls *.sh
$ mv *.sh ~/tmp
.................
+
List item continued with a third paragraph.

2. List item two continued with an open block.
+
--
This paragraph is part of the preceding list item.

a. This list is nested and does not require explicit item
continuation.
+
This paragraph is part of the preceding list item.

b. List item b.

This paragraph belongs to item two of the outer list.
--
```

And here is the equivalent in Markdown:
```
1.  List item one.

    List item one continued with a second paragraph followed by an
    Indented block.

        $ ls *.sh
        $ mv *.sh ~/tmp

    List item continued with a third paragraph.

2.  List item two continued with an open block.

    This paragraph is part of the preceding list item.

    1. This list is nested and does not require explicit item continuation.

       This paragraph is part of the preceding list item.

    2. List item b.

    This paragraph belongs to item two of the outer list.
```

The AsciiDoc version is, arguably, easier to write. You don't need
to worry about indentation.  But the Markdown version is much easier
to read.  The nesting of list items is apparent to the eye in the
source, not just in the processed document.

## Why is a spec needed?

John Gruber's [canonical description of Markdown's
syntax](http://daringfireball.net/projects/markdown/syntax)
does not specify the syntax unambiguously.  Here are some examples of
questions it does not answer:

1.  How much indentation is needed for a sublist?  The spec says that
    continuation paragraphs need to be indented four spaces, but is
    not fully explicit about sublists.  It is natural to think that
    they, too, must be indented four spaces, but `Markdown.pl` does
    not require that.  This is hardly a "corner case," and divergences
    between implementations on this issue often lead to surprises for
    users in real documents. (See [this comment by John
    Gruber](http://article.gmane.org/gmane.text.markdown.general/1997).)

2.  Is a blank line needed before a block quote or heading?
    Most implementations do not require the blank line.  However,
    this can lead to unexpected results in hard-wrapped text, and
    also to ambiguities in parsing (note that some implementations
    put the heading inside the blockquote, while others do not).
    (John Gruber has also spoken [in favor of requiring the blank
    lines](http://article.gmane.org/gmane.text.markdown.general/2146).)

3.  Is a blank line needed before an indented code block?
    (`Markdown.pl` requires it, but this is not mentioned in the
    documentation, and some implementations do not require it.)

    ``` markdown
    paragraph
        code?
    ```

4.  What is the exact rule for determining when list items get
    wrapped in `<p>` tags?  Can a list be partially "loose" and partially
    "tight"?  What should we do with a list like this?

    ``` markdown
    1. one

    2. two
    3. three
    ```

    Or this?

    ``` markdown
    1.  one
        - a

        - b
    2.  two
    ```

    (There are some relevant comments by John Gruber
    [here](http://article.gmane.org/gmane.text.markdown.general/2554).)

5.  Can list markers be indented?  Can ordered list markers be right-aligned?

    ``` markdown
     8. item 1
     9. item 2
    10. item 2a
    ```

6.  Is this one list with a thematic break in its second item,
    or two lists separated by a thematic break?

    ``` markdown
    * a
    * * * * *
    * b
    ```

7.  When list markers change from numbers to bullets, do we have
    two lists or one?  (The Markdown syntax description suggests two,
    but the perl scripts and many other implementations produce one.)

    ``` markdown
    1. fee
    2. fie
    -  foe
    -  fum
    ```

8.  What are the precedence rules for the markers of inline structure?
    For example, is the following a valid link, or does the code span
    take precedence ?

    ``` markdown
    [a backtick (`)](/url) and [another backtick (`)](/url).
    ```

9.  What are the precedence rules for markers of emphasis and strong
    emphasis?  For example, how should the following be parsed?

    ``` markdown
    *foo *bar* baz*
    ```

10. What are the precedence rules between block-level and inline-level
    structure?  For example, how should the following be parsed?

    ``` markdown
    - `a long code span can contain a hyphen like this
      - and it can screw things up`
    ```

11. Can list items include section headings?  (`Markdown.pl` does not
    allow this, but does allow blockquotes to include headings.)

    ``` markdown
    - # Heading
    ```

12. Can list items be empty?

    ``` markdown
    * a
    *
    * b
    ```

13. Can link references be defined inside block quotes or list items?

    ``` markdown
    > Blockquote *foo*.
    >
    > *foo*: /url
    ```

14. If there are multiple definitions for the same reference, which takes
    precedence?

    ``` markdown
    *foo*: /url1
    *foo*: /url2

    *foo***
    ```

In the absence of a spec, early implementers consulted `Markdown.pl`
to resolve these ambiguities.  But `Markdown.pl` was quite buggy, and
gave manifestly bad results in many cases, so it was not a
satisfactory replacement for a spec.

Because there is no unambiguous spec, implementations have diverged
considerably.  As a result, users are often surprised to find that
a document that renders one way on one system (say, a GitHub wiki)
renders differently on another (say, converting to docbook using
pandoc).  To make matters worse, because nothing in Markdown counts
as a "syntax error," the divergence often isn't discovered right away.

## About this document

This document attempts to specify Markdown syntax unambiguously.
It contains many examples with side-by-side Markdown and
HTML.  These are intended to double as conformance tests.  An
accompanying script `spec_tests.py` can be used to run the tests
against any Markdown program:

    python test/spec_tests.py --spec spec.txt --program PROGRAM

Since this document describes how Markdown is to be parsed into
an abstract syntax tree, it would have made sense to use an abstract
representation of the syntax tree instead of HTML.  But HTML is capable
of representing the structural distinctions we need to make, and the
choice of HTML for the tests makes it possible to run the tests against
an implementation without writing an abstract syntax tree renderer.

This document is generated from a text file, `spec.txt`, written
in Markdown with a small extension for the side-by-side tests.
The script `tools/makespec.py` can be used to convert `spec.txt` into
HTML or CommonMark (which can then be converted into other formats).

In the examples, the `→` character is used to represent tabs.

# Preliminaries

## Characters and lines

Any sequence of *characters* is a valid CommonMark
document.

A **character** is a Unicode code point.  Although some
code points (for example, combining accents) do not correspond to
characters in an intuitive sense, all code points count as characters
for purposes of this spec.

This spec does not specify an encoding; it thinks of lines as composed
of *characters* rather than bytes.  A conforming parser may be limited
to a certain encoding.

A **line** is a sequence of zero or more *characters*
other than newline (`U+000A`) or carriage return (`U+000D`),
followed by a *line ending* or by the end of file.

A **line ending** is a newline (`U+000A`), a carriage return
(`U+000D`) not followed by a newline, or a carriage return and a
following newline.

A line containing no characters, or a line containing only spaces
(`U+0020`) or tabs (`U+0009`), is called a **blank line**.

The following definitions of character classes will be used in this spec:

A **whitespace character** is a space
(`U+0020`), tab (`U+0009`), newline (`U+000A`), line tabulation (`U+000B`),
form feed (`U+000C`), or carriage return (`U+000D`).

**Whitespace** is a sequence of one or more *whitespace
characters*.

A **Unicode whitespace character** is
any code point in the Unicode `Zs` general category, or a tab (`U+0009`),
carriage return (`U+000D`), newline (`U+000A`), or form feed
(`U+000C`).

**Unicode whitespace** is a sequence of one
or more *Unicode whitespace characters*.

A **space** is `U+0020`.

A [non-whitespace character](@) is any character
that is not a *whitespace character*.

An **ASCII control character** is a character between `U+0000–1F` (both
including) or `U+007F`.

An **ASCII punctuation character**
is `!`, `"`, `#`, `$`, `%`, `&`, `'`, `(`, `)`,
`*`, `+`, `,`, `-`, `.`, `/` (U+0021–2F), 
`:`, `;`, `<`, `=`, `>`, `?`, `@` (U+003A–0040),
`[`, `\`, `]`, `^`, `_`, `` ` `` (U+005B–0060), 
`{`, `|`, `}`, or `~` (U+007B–007E).

A **punctuation character** is an *ASCII
punctuation character* or anything in
the general Unicode categories  `Pc`, `Pd`, `Pe`, `Pf`, `Pi`, `Po`, or `Ps`.

## Tabs

Tabs in lines are not expanded to *spaces*.  However,
in contexts where whitespace helps to define block structure,
tabs behave as if they were replaced by spaces with a tab stop
of 4 characters.

Thus, for example, a tab can be used instead of four spaces
in an indented code block.  (Note, however, that internal
tabs are passed through as literal tabs, not expanded to
spaces.)


```
Example:
→foo→baz→→bim

```
---
→foo→baz→→bim

---


```
Example:
  →foo→baz→→bim

```
---
  →foo→baz→→bim

---


```
Example:
    a→a
    ὐ→a

```
---
    a→a
    ὐ→a

---

In the following example, a continuation paragraph of a list
item is indented with a tab; this has exactly the same effect
as indentation with four spaces would:


```
Example:
  - foo

→bar

```
---
  - foo

→bar

---


```
Example:
- foo

→→bar

```
---
- foo

→→bar

---

Normally the `>` that begins a block quote may be followed
optionally by a space, which is not considered part of the
content.  In the following case `>` is followed by a tab,
which is treated as if it were expanded into three spaces.
Since one of these spaces is considered part of the
delimiter, `foo` is considered to be indented six spaces
inside the block quote context, so we get an indented
code block starting with two spaces.


```
Example:
>→→foo

```
---
>→→foo

---


```
Example:
-→→foo

```
---
-→→foo

---



```
Example:
    foo
→bar

```
---
    foo
→bar

---


```
Example:
 - foo
   - bar
→ - baz

```
---
 - foo
   - bar
→ - baz

---


```
Example:
#→Foo

```
---
#→Foo

---


```
Example:
*→*→*→

```
---
*→*→*→

---


## Insecure characters

For security reasons, the Unicode character `U+0000` must be replaced
with the REPLACEMENT CHARACTER (`U+FFFD`).


## Backslash escapes

Any ASCII punctuation character may be backslash-escaped:


```
Example:
\!\"\#\$\%\&\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\\\]\^\_\`\{\|\}\~

```
---
\!\"\#\$\%\&\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\\\]\^\_\`\{\|\}\~

---


Backslashes before other characters are treated as literal
backslashes:


```
Example:
\→\A\a\ \3\φ\«

```
---
\→\A\a\ \3\φ\«

---


Escaped characters are treated as regular characters and do
not have their usual Markdown meanings:


```
Example:
\*not emphasized*
\<br/> not a tag
\[not a link](/foo)
\`not code`
1\. not a list
\* not a list
\# not a heading
\*foo*: /url "not a reference"
\&ouml; not a character entity

```
---
\*not emphasized*
\<br/> not a tag
\[not a link](/foo)
\`not code`
1\. not a list
\* not a list
\# not a heading
\*foo*: /url "not a reference"
\&ouml; not a character entity

---


If a backslash is itself escaped, the following character is not:


```
Example:
\\*emphasis*

```
---
\\*emphasis*

---


A backslash at the end of the line is a *hard line break*:


```
Example:
foo\
bar

```
---
foo\
bar

---


Backslash escapes do not work in code blocks, code spans, autolinks, or
raw HTML:


```
Example:
`` \[\` ``

```
---
`` \[\` ``

---



```
Example:
    \[\]

```
---
    \[\]

---



```
Example:
~~~
\[\]
~~~

```
---
~~~
\[\]
~~~

---



```
Example:
<http://example.com?find=\*>

```
---
<http://example.com?find=\*>

---



```
Example:
<a href="/bar\/)">

```
---
<a href="/bar\/)">

---


But they work in all other contexts, including URLs and link titles,
link references, and *info strings* in *fenced code blocks*:


```
Example:
[foo](/bar\* "ti\*tle")

```
---
[foo](/bar\* "ti\*tle")

---



```
Example:
*foo*

*foo*: /bar\* "ti\*tle"

```
---
*foo*

*foo*: /bar\* "ti\*tle"

---



```
Example:
``` foo\+bar
foo
```

```
---
``` foo\+bar
foo
```

---


## Entity and numeric character references

Valid HTML entity references and numeric character references
can be used in place of the corresponding Unicode character,
with the following exceptions:

- Entity and character references are not recognized in code
  blocks and code spans.

- Entity and character references cannot stand in place of
  special characters that define structural elements in
  CommonMark.  For example, although `&#42;` can be used
  in place of a literal `*` character, `&#42;` cannot replace
  `*` in emphasis delimiters, bullet list markers, or thematic
  breaks.

Conforming CommonMark parsers need not store information about
whether a particular character was represented in the source
using a Unicode character or an entity reference.

**Entity references** consist of `&` + any of the valid
HTML5 entity names + `;`. The
document <https://html.spec.whatwg.org/entities.json>
is used as an authoritative source for the valid entity
references and their corresponding code points.


```
Example:
&nbsp; &amp; &copy; &AElig; &Dcaron;
&frac34; &HilbertSpace; &DifferentialD;
&ClockwiseContourIntegral; &ngE;

```
---
&nbsp; &amp; &copy; &AElig; &Dcaron;
&frac34; &HilbertSpace; &DifferentialD;
&ClockwiseContourIntegral; &ngE;

---


**Decimal numeric character
references**
consist of `&#` + a string of 1--7 arabic digits + `;`. A
numeric character reference is parsed as the corresponding
Unicode character. Invalid Unicode code points will be replaced by
the REPLACEMENT CHARACTER (`U+FFFD`).  For security reasons,
the code point `U+0000` will also be replaced by `U+FFFD`.


```
Example:
&#35; &#1234; &#992; &#0;

```
---
&#35; &#1234; &#992; &#0;

---


**Hexadecimal numeric character
references** consist of `&#` +
either `X` or `x` + a string of 1-6 hexadecimal digits + `;`.
They too are parsed as the corresponding Unicode character (this
time specified with a hexadecimal numeral instead of decimal).


```
Example:
&#X22; &#XD06; &#xcab;

```
---
&#X22; &#XD06; &#xcab;

---


Here are some nonentities:


```
Example:
&nbsp &x; &#; &#x;
&#87654321;
&#abcdef0;
&ThisIsNotDefined; &hi?;

```
---
&nbsp &x; &#; &#x;
&#87654321;
&#abcdef0;
&ThisIsNotDefined; &hi?;

---


Although HTML5 does accept some entity references
without a trailing semicolon (such as `&copy`), these are not
recognized here, because it makes the grammar too ambiguous:


```
Example:
&copy

```
---
&copy

---


Strings that are not on the list of HTML5 named entities are not
recognized as entity references either:


```
Example:
&MadeUpEntity;

```
---
&MadeUpEntity;

---


Entity and numeric character references are recognized in any
context besides code spans or code blocks, including
URLs, *link titles*, and *fenced code block*** *info strings*:


```
Example:
<a href="&ouml;&ouml;.html">

```
---
<a href="&ouml;&ouml;.html">

---



```
Example:
[foo](/f&ouml;&ouml; "f&ouml;&ouml;")

```
---
[foo](/f&ouml;&ouml; "f&ouml;&ouml;")

---



```
Example:
*foo*

*foo*: /f&ouml;&ouml; "f&ouml;&ouml;"

```
---
*foo*

*foo*: /f&ouml;&ouml; "f&ouml;&ouml;"

---



```
Example:
``` f&ouml;&ouml;
foo
```

```
---
``` f&ouml;&ouml;
foo
```

---


Entity and numeric character references are treated as literal
text in code spans and code blocks:


```
Example:
`f&ouml;&ouml;`

```
---
`f&ouml;&ouml;`

---



```
Example:
    f&ouml;f&ouml;

```
---
    f&ouml;f&ouml;

---


Entity and numeric character references cannot be used
in place of symbols indicating structure in CommonMark
documents.


```
Example:
&#42;foo&#42;
*foo*

```
---
&#42;foo&#42;
*foo*

---


```
Example:
&#42; foo

* foo

```
---
&#42; foo

* foo

---


```
Example:
foo&#10;&#10;bar

```
---
foo&#10;&#10;bar

---


```
Example:
&#9;foo

```
---
&#9;foo

---



```
Example:
[a](url &quot;tit&quot;)

```
---
[a](url &quot;tit&quot;)

---



# Blocks and inlines

We can think of a document as a sequence of
**blocks**---structural elements like paragraphs, block
quotations, lists, headings, rules, and code blocks.  Some blocks (like
block quotes and list items) contain other blocks; others (like
headings and paragraphs) contain **inline** content---text,
links, emphasized text, images, code spans, and so on.

## Precedence

Indicators of block structure always take precedence over indicators
of inline structure.  So, for example, the following is a list with
two items, not a list with one item containing a code span:


```
Example:
- `one
- two`

```
---
- `one
- two`

---


This means that parsing can proceed in two steps:  first, the block
structure of the document can be discerned; second, text lines inside
paragraphs, headings, and other block constructs can be parsed for inline
structure.  The second step requires information about link reference
definitions that will be available only at the end of the first
step.  Note that the first step requires processing lines in sequence,
but the second can be parallelized, since the inline parsing of
one block element does not affect the inline parsing of any other.

## Container blocks and leaf blocks

We can divide blocks into two types:
**container blocks**,
which can contain other blocks, and **leaf blocks**,
which cannot.

# Leaf blocks

This section describes the different kinds of leaf block that make up a
Markdown document.

## Thematic breaks

A line consisting of 0-3 spaces of indentation, followed by a sequence
of three or more matching `-`, `_`, or `*` characters, each followed
optionally by any number of spaces or tabs, forms a
**thematic break**.


```
Example:
***
---
___

```
---
***
---
___

---


Wrong characters:


```
Example:
+++

```
---
+++

---



```
Example:
===

```
---
===

---


Not enough characters:


```
Example:
--
**
__

```
---
--
**
__

---


One to three spaces indent are allowed:


```
Example:
 ***
  ***
   ***

```
---
 ***
  ***
   ***

---


Four spaces is too many:


```
Example:
    ***

```
---
    ***

---



```
Example:
Foo
    ***

```
---
Foo
    ***

---


More than three characters may be used:


```
Example:
_____________________________________

```
---
_____________________________________

---


Spaces are allowed between the characters:


```
Example:
 - - -

```
---
 - - -

---



```
Example:
 **  * ** * ** * **

```
---
 **  * ** * ** * **

---



```
Example:
-     -      -      -

```
---
-     -      -      -

---


Spaces are allowed at the end:


```
Example:
- - - -    

```
---
- - - -    

---


However, no other characters may occur in the line:


```
Example:
_ _ _ _ a

a------

---a---

```
---
_ _ _ _ a

a------

---a---

---


It is required that all of the [non-whitespace characters] be the same.
So, this is not a thematic break:


```
Example:
 *-*

```
---
 *-*

---


Thematic breaks do not need blank lines before or after:


```
Example:
- foo
***
- bar

```
---
- foo
***
- bar

---


Thematic breaks can interrupt a paragraph:


```
Example:
Foo
***
bar

```
---
Foo
***
bar

---


If a line of dashes that meets the above conditions for being a
thematic break could also be interpreted as the underline of a *setext
heading*, the interpretation as a
*setext heading* takes precedence. Thus, for example,
this is a setext heading, not a paragraph followed by a thematic break:


```
Example:
Foo
---
bar

```
---
Foo
---
bar

---


When both a thematic break and a list item are possible
interpretations of a line, the thematic break takes precedence:


```
Example:
* Foo
* * *
* Bar

```
---
* Foo
* * *
* Bar

---


If you want a thematic break in a list item, use a different bullet:


```
Example:
- Foo
- * * *

```
---
- Foo
- * * *

---


## ATX headings

An **ATX heading**
consists of a string of characters, parsed as inline content, between an
opening sequence of 1--6 unescaped `#` characters and an optional
closing sequence of any number of unescaped `#` characters.
The opening sequence of `#` characters must be followed by a
*space* or by the end of line. The optional closing sequence of `#`s must be
preceded by a *space* and may be followed by spaces only.  The opening
`#` character may be indented 0-3 spaces.  The raw contents of the
heading are stripped of leading and trailing spaces before being parsed
as inline content.  The heading level is equal to the number of `#`
characters in the opening sequence.

Simple headings:


```
Example:
# foo
## foo
### foo
#### foo
##### foo
###### foo

```
---
# foo
## foo
### foo
#### foo
##### foo
###### foo

---


More than six `#` characters is not a heading:


```
Example:
####### foo

```
---
####### foo

---


At least one space is required between the `#` characters and the
heading's contents, unless the heading is empty.  Note that many
implementations currently do not require the space.  However, the
space was required by the
[original ATX implementation](http://www.aaronsw.com/2002/atx/atx.py),
and it helps prevent things like the following from being parsed as
headings:


```
Example:
#5 bolt

#hashtag

```
---
#5 bolt

#hashtag

---


This is not a heading, because the first `#` is escaped:


```
Example:
\## foo

```
---
\## foo

---


Contents are parsed as inlines:


```
Example:
# foo *bar* \*baz\*

```
---
# foo *bar* \*baz\*

---


Leading and trailing *whitespace* is ignored in parsing inline content:


```
Example:
#                  foo                     

```
---
#                  foo                     

---


One to three spaces indentation are allowed:


```
Example:
 ### foo
  ## foo
   # foo

```
---
 ### foo
  ## foo
   # foo

---


Four spaces are too much:


```
Example:
    # foo

```
---
    # foo

---



```
Example:
foo
    # bar

```
---
foo
    # bar

---


A closing sequence of `#` characters is optional:


```
Example:
## foo ##
  ###   bar    ###

```
---
## foo ##
  ###   bar    ###

---


It need not be the same length as the opening sequence:


```
Example:
# foo ##################################
##### foo ##

```
---
# foo ##################################
##### foo ##

---


Spaces are allowed after the closing sequence:


```
Example:
### foo ###     

```
---
### foo ###     

---


A sequence of `#` characters with anything but *spaces* following it
is not a closing sequence, but counts as part of the contents of the
heading:


```
Example:
### foo ### b

```
---
### foo ### b

---


The closing sequence must be preceded by a space:


```
Example:
# foo#

```
---
# foo#

---


Backslash-escaped `#` characters do not count as part
of the closing sequence:


```
Example:
### foo \###
## foo #\##
# foo \#

```
---
### foo \###
## foo #\##
# foo \#

---


ATX headings need not be separated from surrounding content by blank
lines, and they can interrupt paragraphs:


```
Example:
****
## foo
****

```
---
****
## foo
****

---



```
Example:
Foo bar
# baz
Bar foo

```
---
Foo bar
# baz
Bar foo

---


ATX headings can be empty:


```
Example:
## 
#
### ###

```
---
## 
#
### ###

---


## Setext headings

A **setext heading** consists of one or more
lines of text, each containing at least one [non-whitespace
character], with no more than 3 spaces indentation, followed by
a *setext heading underline*.  The lines of text must be such
that, were they not followed by the setext heading underline,
they would be interpreted as a paragraph:  they cannot be
interpretable as a *code fence*, *ATX heading**ATX headings*,
*block quote**block quotes*, *thematic break**thematic breaks*,
*list item**list items*, or *HTML block**HTML blocks*.

A **setext heading underline** is a sequence of
`=` characters or a sequence of `-` characters, with no more than 3
spaces indentation and any number of trailing spaces.  If a line
containing a single `-` can be interpreted as an
empty *list items*, it should be interpreted this way
and not as a *setext heading underline*.

The heading is a level 1 heading if `=` characters are used in
the *setext heading underline*, and a level 2 heading if `-`
characters are used.  The contents of the heading are the result
of parsing the preceding lines of text as CommonMark inline
content.

In general, a setext heading need not be preceded or followed by a
blank line.  However, it cannot interrupt a paragraph, so when a
setext heading comes after a paragraph, a blank line is needed between
them.

Simple examples:


```
Example:
Foo *bar*
=========

Foo *bar*
---------

```
---
Foo *bar*
=========

Foo *bar*
---------

---


The content of the header may span more than one line:


```
Example:
Foo *bar
baz*
====

```
---
Foo *bar
baz*
====

---

The contents are the result of parsing the headings's raw
content as inlines.  The heading's raw content is formed by
concatenating the lines and removing initial and final
*whitespace*.


```
Example:
  Foo *bar
baz*→
====

```
---
  Foo *bar
baz*→
====

---


The underlining can be any length:


```
Example:
Foo
-------------------------

Foo
=

```
---
Foo
-------------------------

Foo
=

---


The heading content can be indented up to three spaces, and need
not line up with the underlining:


```
Example:
   Foo
---

  Foo
-----

  Foo
  ===

```
---
   Foo
---

  Foo
-----

  Foo
  ===

---


Four spaces indent is too much:


```
Example:
    Foo
    ---

    Foo
---

```
---
    Foo
    ---

    Foo
---

---


The setext heading underline can be indented up to three spaces, and
may have trailing spaces:


```
Example:
Foo
   ----      

```
---
Foo
   ----      

---


Four spaces is too much:


```
Example:
Foo
    ---

```
---
Foo
    ---

---


The setext heading underline cannot contain internal spaces:


```
Example:
Foo
= =

Foo
--- -

```
---
Foo
= =

Foo
--- -

---


Trailing spaces in the content line do not cause a line break:


```
Example:
Foo  
-----

```
---
Foo  
-----

---


Nor does a backslash at the end:


```
Example:
Foo\
----

```
---
Foo\
----

---


Since indicators of block structure take precedence over
indicators of inline structure, the following are setext headings:


```
Example:
`Foo
----
`

<a title="a lot
---
of dashes"/>

```
---
`Foo
----
`

<a title="a lot
---
of dashes"/>

---


The setext heading underline cannot be a *lazy continuation
line* in a list item or block quote:


```
Example:
> Foo
---

```
---
> Foo
---

---



```
Example:
> foo
bar
===

```
---
> foo
bar
===

---



```
Example:
- Foo
---

```
---
- Foo
---

---


A blank line is needed between a paragraph and a following
setext heading, since otherwise the paragraph becomes part
of the heading's content:


```
Example:
Foo
Bar
---

```
---
Foo
Bar
---

---


But in general a blank line is not required before or after
setext headings:


```
Example:
---
Foo
---
Bar
---
Baz

```
---
---
Foo
---
Bar
---
Baz

---


Setext headings cannot be empty:


```
Example:

====

```
---

====

---


Setext heading text lines must not be interpretable as block
constructs other than paragraphs.  So, the line of dashes
in these examples gets interpreted as a thematic break:


```
Example:
---
---

```
---
---
---

---



```
Example:
- foo
-----

```
---
- foo
-----

---



```
Example:
    foo
---

```
---
    foo
---

---



```
Example:
> foo
-----

```
---
> foo
-----

---


If you want a heading with `> foo` as its literal text, you can
use backslash escapes:


```
Example:
\> foo
------

```
---
\> foo
------

---


**Compatibility note:**  Most existing Markdown implementations
do not allow the text of setext headings to span multiple lines.
But there is no consensus about how to interpret

``` markdown
Foo
bar
---
baz
```

One can find four different interpretations:

1. paragraph "Foo", heading "bar", paragraph "baz"
2. paragraph "Foo bar", thematic break, paragraph "baz"
3. paragraph "Foo bar --- baz"
4. heading "Foo bar", paragraph "baz"

We find interpretation 4 most natural, and interpretation 4
increases the expressive power of CommonMark, by allowing
multiline headings.  Authors who want interpretation 1 can
put a blank line after the first paragraph:


```
Example:
Foo

bar
---
baz

```
---
Foo

bar
---
baz

---


Authors who want interpretation 2 can put blank lines around
the thematic break,


```
Example:
Foo
bar

---

baz

```
---
Foo
bar

---

baz

---


or use a thematic break that cannot count as a *setext heading
underline*, such as


```
Example:
Foo
bar
* * *
baz

```
---
Foo
bar
* * *
baz

---


Authors who want interpretation 3 can use backslash escapes:


```
Example:
Foo
bar
\---
baz

```
---
Foo
bar
\---
baz

---


## Indented code blocks

An **indented code block** is composed of one or more
*indented chunks* separated by blank lines.
An **indented chunk** is a sequence of non-blank lines,
each indented four or more spaces. The contents of the code block are
the literal contents of the lines, including trailing
*line endings*, minus four spaces of indentation.
An indented code block has no *info string*.

An indented code block cannot interrupt a paragraph, so there must be
a blank line between a paragraph and a following indented code block.
(A blank line is not needed, however, between a code block and a following
paragraph.)


```
Example:
    a simple
      indented code block

```
---
    a simple
      indented code block

---


If there is any ambiguity between an interpretation of indentation
as a code block and as indicating that material belongs to a *list
item**list items*, the list item interpretation takes precedence:


```
Example:
  - foo

    bar

```
---
  - foo

    bar

---



```
Example:
1.  foo

    - bar

```
---
1.  foo

    - bar

---



The contents of a code block are literal text, and do not get parsed
as Markdown:


```
Example:
    <a/>
    *hi*

    - one

```
---
    <a/>
    *hi*

    - one

---


Here we have three chunks separated by blank lines:


```
Example:
    chunk1

    chunk2
  
 
 
    chunk3

```
---
    chunk1

    chunk2
  
 
 
    chunk3

---


Any initial spaces beyond four will be included in the content, even
in interior blank lines:


```
Example:
    chunk1
      
      chunk2

```
---
    chunk1
      
      chunk2

---


An indented code block cannot interrupt a paragraph.  (This
allows hanging indents and the like.)


```
Example:
Foo
    bar


```
---
Foo
    bar


---


However, any non-blank line with fewer than four leading spaces ends
the code block immediately.  So a paragraph may occur immediately
after indented code:


```
Example:
    foo
bar

```
---
    foo
bar

---


And indented code can occur immediately before and after other kinds of
blocks:


```
Example:
# Heading
    foo
Heading
------
    foo
----

```
---
# Heading
    foo
Heading
------
    foo
----

---


The first line can be indented more than four spaces:


```
Example:
        foo
    bar

```
---
        foo
    bar

---


Blank lines preceding or following an indented code block
are not included in it:


```
Example:

    
    foo
    


```
---

    
    foo
    


---


Trailing spaces are included in the code block's content:


```
Example:
    foo  

```
---
    foo  

---



## Fenced code blocks

A **code fence** is a sequence
of at least three consecutive backtick characters (`` ` ``) or
tildes (`~`).  (Tildes and backticks cannot be mixed.)
A **fenced code block**
begins with a code fence, indented no more than three spaces.

The line with the opening code fence may optionally contain some text
following the code fence; this is trimmed of leading and trailing
whitespace and called the **info string**. If the *info string* comes
after a backtick fence, it may not contain any backtick
characters.  (The reason for this restriction is that otherwise
some inline code would be incorrectly interpreted as the
beginning of a fenced code block.)

The content of the code block consists of all subsequent lines, until
a closing *code fence* of the same type as the code block
began with (backticks or tildes), and with at least as many backticks
or tildes as the opening code fence.  If the leading code fence is
indented N spaces, then up to N spaces of indentation are removed from
each line of the content (if present).  (If a content line is not
indented, it is preserved unchanged.  If it is indented less than N
spaces, all of the indentation is removed.)

The closing code fence may be indented up to three spaces, and may be
followed only by spaces, which are ignored.  If the end of the
containing block (or document) is reached and no closing code fence
has been found, the code block contains all of the lines after the
opening code fence until the end of the containing block (or
document).  (An alternative spec would require backtracking in the
event that a closing code fence is not found.  But this makes parsing
much less efficient, and there seems to be no real down side to the
behavior described here.)

A fenced code block may interrupt a paragraph, and does not require
a blank line either before or after.

The content of a code fence is treated as literal text, not parsed
as inlines.  The first word of the *info string* is typically used to
specify the language of the code sample, and rendered in the `class`
attribute of the `code` tag.  However, this spec does not mandate any
particular treatment of the *info string*.

Here is a simple example with backticks:


```
Example:
```
<
 >
```

```
---
```
<
 >
```

---


With tildes:


```
Example:
~~~
<
 >
~~~

```
---
~~~
<
 >
~~~

---

Fewer than three backticks is not enough:


```
Example:
``
foo
``

```
---
``
foo
``

---

The closing code fence must use the same character as the opening
fence:


```
Example:
```
aaa
~~~
```

```
---
```
aaa
~~~
```

---



```
Example:
~~~
aaa
```
~~~

```
---
~~~
aaa
```
~~~

---


The closing code fence must be at least as long as the opening fence:


```
Example:
````
aaa
```
``````

```
---
````
aaa
```
``````

---



```
Example:
~~~~
aaa
~~~
~~~~

```
---
~~~~
aaa
~~~
~~~~

---


Unclosed code blocks are closed by the end of the document
(or the enclosing *block quote**block quotes* or *list item**list items*):


```
Example:
```

```
---
```

---



```
Example:
`````

```
aaa

```
---
`````

```
aaa

---



```
Example:
> ```
> aaa

bbb

```
---
> ```
> aaa

bbb

---


A code block can have all empty lines as its content:


```
Example:
```

  
```

```
---
```

  
```

---


A code block can be empty:


```
Example:
```
```

```
---
```
```

---


Fences can be indented.  If the opening fence is indented,
content lines will have equivalent opening indentation removed,
if present:


```
Example:
 ```
 aaa
aaa
```

```
---
 ```
 aaa
aaa
```

---



```
Example:
  ```
aaa
  aaa
aaa
  ```

```
---
  ```
aaa
  aaa
aaa
  ```

---



```
Example:
   ```
   aaa
    aaa
  aaa
   ```

```
---
   ```
   aaa
    aaa
  aaa
   ```

---


Four spaces indentation produces an indented code block:


```
Example:
    ```
    aaa
    ```

```
---
    ```
    aaa
    ```

---


Closing fences may be indented by 0-3 spaces, and their indentation
need not match that of the opening fence:


```
Example:
```
aaa
  ```

```
---
```
aaa
  ```

---



```
Example:
   ```
aaa
  ```

```
---
   ```
aaa
  ```

---


This is not a closing fence, because it is indented 4 spaces:


```
Example:
```
aaa
    ```

```
---
```
aaa
    ```

---



Code fences (opening and closing) cannot contain internal spaces:


```
Example:
``` ```
aaa

```
---
``` ```
aaa

---



```
Example:
~~~~~~
aaa
~~~ ~~

```
---
~~~~~~
aaa
~~~ ~~

---


Fenced code blocks can interrupt paragraphs, and can be followed
directly by paragraphs, without a blank line between:


```
Example:
foo
```
bar
```
baz

```
---
foo
```
bar
```
baz

---


Other blocks can also occur before and after fenced code blocks
without an intervening blank line:


```
Example:
foo
---
~~~
bar
~~~
# baz

```
---
foo
---
~~~
bar
~~~
# baz

---


An *info string* can be provided after the opening code fence.
Although this spec doesn't mandate any particular treatment of
the info string, the first word is typically used to specify
the language of the code block. In HTML output, the language is
normally indicated by adding a class to the `code` element consisting
of `language-` followed by the language name.


```
Example:
```ruby
def foo(x)
  return 3
end
```

```
---
```ruby
def foo(x)
  return 3
end
```

---



```
Example:
~~~~    ruby startline=3 $%@#$
def foo(x)
  return 3
end
~~~~~~~

```
---
~~~~    ruby startline=3 $%@#$
def foo(x)
  return 3
end
~~~~~~~

---



```
Example:
````;
````

```
---
````;
````

---


*Info strings* for backtick code blocks cannot contain backticks:


```
Example:
``` aa ```
foo

```
---
``` aa ```
foo

---


*Info strings* for tilde code blocks can contain backticks and tildes:


```
Example:
~~~ aa ``` ~~~
foo
~~~

```
---
~~~ aa ``` ~~~
foo
~~~

---


Closing code fences cannot have *info strings*:


```
Example:
```
``` aaa
```

```
---
```
``` aaa
```

---



## HTML blocks

An **HTML block** is a group of lines that is treated
as raw HTML (and will not be escaped in HTML output).

There are seven kinds of *HTML block*, which can be defined by their
start and end conditions.  The block begins with a line that meets a
**start condition** (after up to three spaces optional indentation).
It ends with the first subsequent line that meets a matching **end
condition**, or the last line of the document, or the last line of
the [container block](#container-blocks) containing the current HTML
block, if no line is encountered that meets the *end condition*.  If
the first line meets both the *start condition* and the *end
condition*, the block will contain just that line.

1.  **Start condition:**  line begins with the string `<script`,
`<pre`, or `<style` (case-insensitive), followed by whitespace,
the string `>`, or the end of the line.\
**End condition:**  line contains an end tag
`</script>`, `</pre>`, or `</style>` (case-insensitive; it
need not match the start tag).

2.  **Start condition:** line begins with the string `<!--`.\
**End condition:**  line contains the string `-->`.

3.  **Start condition:** line begins with the string `<?`.\
**End condition:** line contains the string `?>`.

4.  **Start condition:** line begins with the string `<!`
followed by an ASCII letter.\
**End condition:** line contains the character `>`.

5.  **Start condition:**  line begins with the string
`<![CDATA[`.\
**End condition:** line contains the string `]]>`.

6.  **Start condition:** line begins the string `<` or `</`
followed by one of the strings (case-insensitive) `address`,
`article`, `aside`, `base`, `basefont`, `blockquote`, `body`,
`caption`, `center`, `col`, `colgroup`, `dd`, `details`, `dialog`,
`dir`, `div`, `dl`, `dt`, `fieldset`, `figcaption`, `figure`,
`footer`, `form`, `frame`, `frameset`,
`h1`, `h2`, `h3`, `h4`, `h5`, `h6`, `head`, `header`, `hr`,
`html`, `iframe`, `legend`, `li`, `link`, `main`, `menu`, `menuitem`,
`nav`, `noframes`, `ol`, `optgroup`, `option`, `p`, `param`,
`section`, `source`, `summary`, `table`, `tbody`, `td`,
`tfoot`, `th`, `thead`, `title`, `tr`, `track`, `ul`, followed
by *whitespace*, the end of the line, the string `>`, or
the string `/>`.\
**End condition:** line is followed by a *blank line*.

7.  **Start condition:**  line begins with a complete *open tag*
(with any *tag name* other than `script`,
`style`, or `pre`) or a complete *closing tag*,
followed only by *whitespace* or the end of the line.\
**End condition:** line is followed by a *blank line*.

HTML blocks continue until they are closed by their appropriate
*end condition*, or the last line of the document or other [container
block](#container-blocks).  This means any HTML **within an HTML
block** that might otherwise be recognised as a start condition will
be ignored by the parser and passed through as-is, without changing
the parser's state.

For instance, `<pre>` within an HTML block started by `<table>` will not affect
the parser state; as the HTML block was started in by start condition 6, it
will end at any blank line. This can be surprising:


```
Example:
<table><tr><td>
<pre>
**Hello**,

_world_.
</pre>
</td></tr></table>

```
---
<table><tr><td>
<pre>
**Hello**,

_world_.
</pre>
</td></tr></table>

---

In this case, the HTML block is terminated by the newline — the `**Hello**`
text remains verbatim — and regular parsing resumes, with a paragraph,
emphasised `world` and inline and block HTML following.

All types of *HTML blocks* except type 7 may interrupt
a paragraph.  Blocks of type 7 may not interrupt a paragraph.
(This restriction is intended to prevent unwanted interpretation
of long tags inside a wrapped paragraph as starting HTML blocks.)

Some simple examples follow.  Here are some basic HTML blocks
of type 6:


```
Example:
<table>
  <tr>
    <td>
           hi
    </td>
  </tr>
</table>

okay.

```
---
<table>
  <tr>
    <td>
           hi
    </td>
  </tr>
</table>

okay.

---



```
Example:
 <div>
  *hello*
         <foo><a>

```
---
 <div>
  *hello*
         <foo><a>

---


A block can also start with a closing tag:


```
Example:
</div>
*foo*

```
---
</div>
*foo*

---


Here we have two HTML blocks with a Markdown paragraph between them:


```
Example:
<DIV CLASS="foo">

*Markdown*

</DIV>

```
---
<DIV CLASS="foo">

*Markdown*

</DIV>

---


The tag on the first line can be partial, as long
as it is split where there would be whitespace:


```
Example:
<div id="foo"
  class="bar">
</div>

```
---
<div id="foo"
  class="bar">
</div>

---



```
Example:
<div id="foo" class="bar
  baz">
</div>

```
---
<div id="foo" class="bar
  baz">
</div>

---


An open tag need not be closed:

```
Example:
<div>
*foo*

*bar*

```
---
<div>
*foo*

*bar*

---



A partial tag need not even be completed (garbage
in, garbage out):


```
Example:
<div id="foo"
*hi*

```
---
<div id="foo"
*hi*

---



```
Example:
<div class
foo

```
---
<div class
foo

---


The initial tag doesn't even need to be a valid
tag, as long as it starts like one:


```
Example:
<div *???-&&&-<---
*foo*

```
---
<div *???-&&&-<---
*foo*

---


In type 6 blocks, the initial tag need not be on a line by
itself:


```
Example:
<div><a href="bar">*foo*</a></div>

```
---
<div><a href="bar">*foo*</a></div>

---



```
Example:
<table><tr><td>
foo
</td></tr></table>

```
---
<table><tr><td>
foo
</td></tr></table>

---


Everything until the next blank line or end of document
gets included in the HTML block.  So, in the following
example, what looks like a Markdown code block
is actually part of the HTML block, which continues until a blank
line or the end of the document is reached:


```
Example:
<div></div>
``` c
int x = 33;
```

```
---
<div></div>
``` c
int x = 33;
```

---


To start an *HTML block* with a tag that is *not* in the
list of block-level tags in (6), you must put the tag by
itself on the first line (and it must be complete):


```
Example:
<a href="foo">
*bar*
</a>

```
---
<a href="foo">
*bar*
</a>

---


In type 7 blocks, the *tag name* can be anything:


```
Example:
<Warning>
*bar*
</Warning>

```
---
<Warning>
*bar*
</Warning>

---



```
Example:
<i class="foo">
*bar*
</i>

```
---
<i class="foo">
*bar*
</i>

---



```
Example:
</ins>
*bar*

```
---
</ins>
*bar*

---


These rules are designed to allow us to work with tags that
can function as either block-level or inline-level tags.
The `<del>` tag is a nice example.  We can surround content with
`<del>` tags in three different ways.  In this case, we get a raw
HTML block, because the `<del>` tag is on a line by itself:


```
Example:
<del>
*foo*
</del>

```
---
<del>
*foo*
</del>

---


In this case, we get a raw HTML block that just includes
the `<del>` tag (because it ends with the following blank
line).  So the contents get interpreted as CommonMark:


```
Example:
<del>

*foo*

</del>

```
---
<del>

*foo*

</del>

---


Finally, in this case, the `<del>` tags are interpreted
as *raw HTML* *inside* the CommonMark paragraph.  (Because
the tag is not on a line by itself, we get inline HTML
rather than an *HTML block*.)


```
Example:
<del>*foo*</del>

```
---
<del>*foo*</del>

---


HTML tags designed to contain literal content
(`script`, `style`, `pre`), comments, processing instructions,
and declarations are treated somewhat differently.
Instead of ending at the first blank line, these blocks
end at the first line containing a corresponding end tag.
As a result, these blocks can contain blank lines:

A pre tag (type 1):


```
Example:
<pre language="haskell"><code>
import Text.HTML.TagSoup

main :: IO ()
main = print $ parseTags tags
</code></pre>
okay

```
---
<pre language="haskell"><code>
import Text.HTML.TagSoup

main :: IO ()
main = print $ parseTags tags
</code></pre>
okay

---


A script tag (type 1):


```
Example:
<script type="text/javascript">
// JavaScript example

document.getElementById("demo").innerHTML = "Hello JavaScript!";
</script>
okay

```
---
<script type="text/javascript">
// JavaScript example

document.getElementById("demo").innerHTML = "Hello JavaScript!";
</script>
okay

---


A style tag (type 1):


```
Example:
<style
  type="text/css">
h1 {color:red;}

p {color:blue;}
</style>
okay

```
---
<style
  type="text/css">
h1 {color:red;}

p {color:blue;}
</style>
okay

---


If there is no matching end tag, the block will end at the
end of the document (or the enclosing *block quote**block quotes*
or *list item**list items*):


```
Example:
<style
  type="text/css">

foo

```
---
<style
  type="text/css">

foo

---



```
Example:
> <div>
> foo

bar

```
---
> <div>
> foo

bar

---



```
Example:
- <div>
- foo

```
---
- <div>
- foo

---


The end tag can occur on the same line as the start tag:


```
Example:
<style>p{color:red;}</style>
*foo*

```
---
<style>p{color:red;}</style>
*foo*

---



```
Example:
<!-- foo -->*bar*
*baz*

```
---
<!-- foo -->*bar*
*baz*

---


Note that anything on the last line after the
end tag will be included in the *HTML block*:


```
Example:
<script>
foo
</script>1. *bar*

```
---
<script>
foo
</script>1. *bar*

---


A comment (type 2):


```
Example:
<!-- Foo

bar
   baz -->
okay

```
---
<!-- Foo

bar
   baz -->
okay

---



A processing instruction (type 3):


```
Example:
<?php

  echo '>';

?>
okay

```
---
<?php

  echo '>';

?>
okay

---


A declaration (type 4):


```
Example:
<!DOCTYPE html>

```
---
<!DOCTYPE html>

---


CDATA (type 5):


```
Example:
<![CDATA[
function matchwo(a,b)
{
  if (a < b && a < 0) then {
    return 1;

  } else {

    return 0;
  }
}
]]>
okay

```
---
<![CDATA[
function matchwo(a,b)
{
  if (a < b && a < 0) then {
    return 1;

  } else {

    return 0;
  }
}
]]>
okay

---


The opening tag can be indented 1-3 spaces, but not 4:


```
Example:
  <!-- foo -->

    <!-- foo -->

```
---
  <!-- foo -->

    <!-- foo -->

---



```
Example:
  <div>

    <div>

```
---
  <div>

    <div>

---


An HTML block of types 1--6 can interrupt a paragraph, and need not be
preceded by a blank line.


```
Example:
Foo
<div>
bar
</div>

```
---
Foo
<div>
bar
</div>

---


However, a following blank line is needed, except at the end of
a document, and except for blocks of types 1--5, *above**HTML
block*:


```
Example:
<div>
bar
</div>
*foo*

```
---
<div>
bar
</div>
*foo*

---


HTML blocks of type 7 cannot interrupt a paragraph:


```
Example:
Foo
<a href="bar">
baz

```
---
Foo
<a href="bar">
baz

---


This rule differs from John Gruber's original Markdown syntax
specification, which says:

> The only restrictions are that block-level HTML elements —
> e.g. `<div>`, `<table>`, `<pre>`, `<p>`, etc. — must be separated from
> surrounding content by blank lines, and the start and end tags of the
> block should not be indented with tabs or spaces.

In some ways Gruber's rule is more restrictive than the one given
here:

- It requires that an HTML block be preceded by a blank line.
- It does not allow the start tag to be indented.
- It requires a matching end tag, which it also does not allow to
  be indented.

Most Markdown implementations (including some of Gruber's own) do not
respect all of these restrictions.

There is one respect, however, in which Gruber's rule is more liberal
than the one given here, since it allows blank lines to occur inside
an HTML block.  There are two reasons for disallowing them here.
First, it removes the need to parse balanced tags, which is
expensive and can require backtracking from the end of the document
if no matching end tag is found. Second, it provides a very simple
and flexible way of including Markdown content inside HTML tags:
simply separate the Markdown from the HTML using blank lines:

Compare:


```
Example:
<div>

*Emphasized* text.

</div>

```
---
<div>

*Emphasized* text.

</div>

---



```
Example:
<div>
*Emphasized* text.
</div>

```
---
<div>
*Emphasized* text.
</div>

---


Some Markdown implementations have adopted a convention of
interpreting content inside tags as text if the open tag has
the attribute `markdown=1`.  The rule given above seems a simpler and
more elegant way of achieving the same expressive power, which is also
much simpler to parse.

The main potential drawback is that one can no longer paste HTML
blocks into Markdown documents with 100% reliability.  However,
*in most cases* this will work fine, because the blank lines in
HTML are usually followed by HTML block tags.  For example:


```
Example:
<table>

<tr>

<td>
Hi
</td>

</tr>

</table>

```
---
<table>

<tr>

<td>
Hi
</td>

</tr>

</table>

---


There are problems, however, if the inner tags are indented
*and* separated by spaces, as then they will be interpreted as
an indented code block:


```
Example:
<table>

  <tr>

    <td>
      Hi
    </td>

  </tr>

</table>

```
---
<table>

  <tr>

    <td>
      Hi
    </td>

  </tr>

</table>

---


Fortunately, blank lines are usually not necessary and can be
deleted.  The exception is inside `<pre>` tags, but as described
*above**HTML blocks*, raw HTML blocks starting with `<pre>`
*can* contain blank lines.

## Link reference definitions

A **link reference definition**
consists of a *link label*, indented up to three spaces, followed
by a colon (`:`), optional *whitespace* (including up to one
*line ending*), a *link destination*,
optional *whitespace* (including up to one
*line ending*), and an optional *link
title*, which if it is present must be separated
from the *link destination* by *whitespace*.
No further [non-whitespace characters] may occur on the line.

A *link reference definition*
does not correspond to a structural element of a document.  Instead, it
defines a label which can be used in *reference links*
and reference-style *images* elsewhere in the document.  *Link
reference definitions* can come either before or after the links that use
them.


```
Example:
*foo*: /url "title"

*foo*

```
---
*foo*: /url "title"

*foo*

---



```
Example:
   *foo*: 
      /url  
           'the title'  

*foo*

```
---
   *foo*: 
      /url  
           'the title'  

*foo*

---



```
Example:
[Foo*bar\]]:my_(url) 'title (with parens)'

[Foo*bar\]]

```
---
[Foo*bar\]]:my_(url) 'title (with parens)'

[Foo*bar\]]

---



```
Example:
*Foo bar*:
<my url>
'title'

*Foo bar*

```
---
*Foo bar*:
<my url>
'title'

*Foo bar*

---


The title may extend over multiple lines:


```
Example:
*foo*: /url '
title
line1
line2
'

*foo*

```
---
*foo*: /url '
title
line1
line2
'

*foo*

---


However, it may not contain a *blank line*:


```
Example:
*foo*: /url 'title

with blank line'

*foo*

```
---
*foo*: /url 'title

with blank line'

*foo*

---


The title may be omitted:


```
Example:
*foo*:
/url

*foo*

```
---
*foo*:
/url

*foo*

---


The link destination may not be omitted:


```
Example:
*foo*:

*foo*

```
---
*foo*:

*foo*

---

 However, an empty link destination may be specified using
 angle brackets:


```
Example:
*foo*: <>

*foo*

```
---
*foo*: <>

*foo*

---

The title must be separated from the link destination by
whitespace:


```
Example:
*foo*: <bar>(baz)

*foo*

```
---
*foo*: <bar>(baz)

*foo*

---


Both title and destination can contain backslash escapes
and literal backslashes:


```
Example:
*foo*: /url\bar\*baz "foo\"bar\baz"

*foo*

```
---
*foo*: /url\bar\*baz "foo\"bar\baz"

*foo*

---


A link can come before its corresponding definition:


```
Example:
*foo*

*foo*: url

```
---
*foo*

*foo*: url

---


If there are several matching definitions, the first one takes
precedence:


```
Example:
*foo*

*foo*: first
*foo*: second

```
---
*foo*

*foo*: first
*foo*: second

---


As noted in the section on *Links*, matching of labels is
case-insensitive (see *matches*).


```
Example:
*FOO*: /url

*Foo*

```
---
*FOO*: /url

*Foo*

---



```
Example:
*ΑΓΩ*: /φου

*αγω*

```
---
*ΑΓΩ*: /φου

*αγω*

---


Here is a link reference definition with no corresponding link.
It contributes nothing to the document.


```
Example:
*foo*: /url

```
---
*foo*: /url

---


Here is another one:


```
Example:
*
foo
*: /url
bar

```
---
*
foo
*: /url
bar

---


This is not a link reference definition, because there are
[non-whitespace characters] after the title:


```
Example:
*foo*: /url "title" ok

```
---
*foo*: /url "title" ok

---


This is a link reference definition, but it has no title:


```
Example:
*foo*: /url
"title" ok

```
---
*foo*: /url
"title" ok

---


This is not a link reference definition, because it is indented
four spaces:


```
Example:
    *foo*: /url "title"

*foo*

```
---
    *foo*: /url "title"

*foo*

---


This is not a link reference definition, because it occurs inside
a code block:


```
Example:
```
*foo*: /url
```

*foo*

```
---
```
*foo*: /url
```

*foo*

---


A *link reference definition* cannot interrupt a paragraph.


```
Example:
Foo
*bar*: /baz

*bar*

```
---
Foo
*bar*: /baz

*bar*

---


However, it can directly follow other block elements, such as headings
and thematic breaks, and it need not be followed by a blank line.


```
Example:
# *Foo*
*foo*: /url
> bar

```
---
# *Foo*
*foo*: /url
> bar

---


```
Example:
*foo*: /url
bar
===
*foo*

```
---
*foo*: /url
bar
===
*foo*

---


```
Example:
*foo*: /url
===
*foo*

```
---
*foo*: /url
===
*foo*

---


Several *link reference definitions*
can occur one after another, without intervening blank lines.


```
Example:
*foo*: /foo-url "foo"
*bar*: /bar-url
  "bar"
*baz*: /baz-url

*foo*,
*bar*,
*baz*

```
---
*foo*: /foo-url "foo"
*bar*: /bar-url
  "bar"
*baz*: /baz-url

*foo*,
*bar*,
*baz*

---


*Link reference definitions* can occur
inside block containers, like lists and block quotations.  They
affect the entire document, not just the container in which they
are defined:


```
Example:
*foo*

> *foo*: /url

```
---
*foo*

> *foo*: /url

---


Whether something is a *link reference definition* is
independent of whether the link reference it defines is
used in the document.  Thus, for example, the following
document contains just a link reference definition, and
no visible content:


```
Example:
*foo*: /url

```
---
*foo*: /url

---


## Paragraphs

A sequence of non-blank lines that cannot be interpreted as other
kinds of blocks forms a **paragraph**.
The contents of the paragraph are the result of parsing the
paragraph's raw content as inlines.  The paragraph's raw content
is formed by concatenating the lines and removing initial and final
*whitespace*.

A simple example with two paragraphs:


```
Example:
aaa

bbb

```
---
aaa

bbb

---


Paragraphs can contain multiple lines, but no blank lines:


```
Example:
aaa
bbb

ccc
ddd

```
---
aaa
bbb

ccc
ddd

---


Multiple blank lines between paragraphs have no effect:


```
Example:
aaa


bbb

```
---
aaa


bbb

---


Leading spaces are skipped:


```
Example:
  aaa
 bbb

```
---
  aaa
 bbb

---


Lines after the first may be indented any amount, since indented
code blocks cannot interrupt paragraphs.


```
Example:
aaa
             bbb
                                       ccc

```
---
aaa
             bbb
                                       ccc

---


However, the first line may be indented at most three spaces,
or an indented code block will be triggered:


```
Example:
   aaa
bbb

```
---
   aaa
bbb

---



```
Example:
    aaa
bbb

```
---
    aaa
bbb

---


Final spaces are stripped before inline parsing, so a paragraph
that ends with two or more spaces will not end with a *hard line
break*:


```
Example:
aaa     
bbb     

```
---
aaa     
bbb     

---


## Blank lines

*Blank lines* between block-level elements are ignored,
except for the role they play in determining whether a *list*
is *tight* or *loose*.

Blank lines at the beginning and end of the document are also ignored.


```
Example:
  

aaa
  

# aaa

  

```
---
  

aaa
  

# aaa

  

---



# Container blocks

A [container block](#container-blocks) is a block that has other
blocks as its contents.  There are two basic kinds of container blocks:
*block quotes* and *list items*.
*Lists* are meta-containers for *list items*.

We define the syntax for container blocks recursively.  The general
form of the definition is:

> If X is a sequence of blocks, then the result of
> transforming X in such-and-such a way is a container of type Y
> with these blocks as its content.

So, we explain what counts as a block quote or list item by explaining
how these can be *generated* from their contents. This should suffice
to define the syntax, although it does not give a recipe for *parsing*
these constructions.  (A recipe is provided below in the section entitled
[A parsing strategy](#appendix-a-parsing-strategy).)

## Block quotes

A **block quote marker**
consists of 0-3 spaces of initial indent, plus (a) the character `>` together
with a following space, or (b) a single character `>` not followed by a space.

The following rules define *block quotes*:

1.  **Basic case.**  If a string of lines *Ls* constitute a sequence
    of blocks *Bs*, then the result of prepending a *block quote
    marker* to the beginning of each line in *Ls*
    is a [block quote](#block-quotes) containing *Bs*.

2.  **Laziness.**  If a string of lines *Ls* constitute a [block
    quote](#block-quotes) with contents *Bs*, then the result of deleting
    the initial *block quote marker* from one or
    more lines in which the next [non-whitespace character] after the *block
    quote marker* is *paragraph continuation
    text* is a block quote with *Bs* as its content.
    **Paragraph continuation text** is text
    that will be parsed as part of the content of a paragraph, but does
    not occur at the beginning of the paragraph.

3.  **Consecutiveness.**  A document cannot contain two *block
    quotes* in a row unless there is a *blank line* between them.

Nothing else counts as a [block quote](#block-quotes).

Here is a simple example:


```
Example:
> # Foo
> bar
> baz

```
---
> # Foo
> bar
> baz

---


The spaces after the `>` characters can be omitted:


```
Example:
># Foo
>bar
> baz

```
---
># Foo
>bar
> baz

---


The `>` characters can be indented 1-3 spaces:


```
Example:
   > # Foo
   > bar
 > baz

```
---
   > # Foo
   > bar
 > baz

---


Four spaces gives us a code block:


```
Example:
    > # Foo
    > bar
    > baz

```
---
    > # Foo
    > bar
    > baz

---


The Laziness clause allows us to omit the `>` before
*paragraph continuation text*:


```
Example:
> # Foo
> bar
baz

```
---
> # Foo
> bar
baz

---


A block quote can contain some lazy and some non-lazy
continuation lines:


```
Example:
> bar
baz
> foo

```
---
> bar
baz
> foo

---


Laziness only applies to lines that would have been continuations of
paragraphs had they been prepended with *block quote markers*.
For example, the `> ` cannot be omitted in the second line of

``` markdown
> foo
> ---
```

without changing the meaning:


```
Example:
> foo
---

```
---
> foo
---

---


Similarly, if we omit the `> ` in the second line of

``` markdown
> - foo
> - bar
```

then the block quote ends after the first line:


```
Example:
> - foo
- bar

```
---
> - foo
- bar

---


For the same reason, we can't omit the `> ` in front of
subsequent lines of an indented or fenced code block:


```
Example:
>     foo
    bar

```
---
>     foo
    bar

---



```
Example:
> ```
foo
```

```
---
> ```
foo
```

---


Note that in the following case, we have a *lazy
continuation line*:


```
Example:
> foo
    - bar

```
---
> foo
    - bar

---


To see why, note that in

```markdown
> foo
>     - bar
```

the `- bar` is indented too far to start a list, and can't
be an indented code block because indented code blocks cannot
interrupt paragraphs, so it is *paragraph continuation text*.

A block quote can be empty:


```
Example:
>

```
---
>

---



```
Example:
>
>  
> 

```
---
>
>  
> 

---


A block quote can have initial or final blank lines:


```
Example:
>
> foo
>  

```
---
>
> foo
>  

---


A blank line always separates block quotes:


```
Example:
> foo

> bar

```
---
> foo

> bar

---


(Most current Markdown implementations, including John Gruber's
original `Markdown.pl`, will parse this example as a single block quote
with two paragraphs.  But it seems better to allow the author to decide
whether two block quotes or one are wanted.)

Consecutiveness means that if we put these block quotes together,
we get a single block quote:


```
Example:
> foo
> bar

```
---
> foo
> bar

---


To get a block quote with two paragraphs, use:


```
Example:
> foo
>
> bar

```
---
> foo
>
> bar

---


Block quotes can interrupt paragraphs:


```
Example:
foo
> bar

```
---
foo
> bar

---


In general, blank lines are not needed before or after block
quotes:


```
Example:
> aaa
***
> bbb

```
---
> aaa
***
> bbb

---


However, because of laziness, a blank line is needed between
a block quote and a following paragraph:


```
Example:
> bar
baz

```
---
> bar
baz

---



```
Example:
> bar

baz

```
---
> bar

baz

---



```
Example:
> bar
>
baz

```
---
> bar
>
baz

---


It is a consequence of the Laziness rule that any number
of initial `>`s may be omitted on a continuation line of a
nested block quote:


```
Example:
> > > foo
bar

```
---
> > > foo
bar

---



```
Example:
>>> foo
> bar
>>baz

```
---
>>> foo
> bar
>>baz

---


When including an indented code block in a block quote,
remember that the *block quote marker* includes
both the `>` and a following space.  So *five spaces* are needed after
the `>`:


```
Example:
>     code

>    not code

```
---
>     code

>    not code

---



## List items

A **list marker** is a
*bullet list marker* or an *ordered list marker*.

A **bullet list marker**
is a `-`, `+`, or `*` character.

An **ordered list marker**
is a sequence of 1--9 arabic digits (`0-9`), followed by either a
`.` character or a `)` character.  (The reason for the length
limit is that with 10 digits we start seeing integer overflows
in some browsers.)

The following rules define *list items*:

1.  **Basic case.**  If a sequence of lines *Ls* constitute a sequence of
    blocks *Bs* starting with a [non-whitespace character], and *M* is a
    list marker of width *W* followed by 1 ≤ *N* ≤ 4 spaces, then the result
    of prepending *M* and the following spaces to the first line of
    *Ls*, and indenting subsequent lines of *Ls* by *W + N* spaces, is a
    list item with *Bs* as its contents.  The type of the list item
    (bullet or ordered) is determined by the type of its list marker.
    If the list item is ordered, then it is also assigned a start
    number, based on the ordered list marker.

    Exceptions:

    1. When the first list item in a *list* interrupts
       a paragraph---that is, when it starts on a line that would
       otherwise count as *paragraph continuation text*---then (a)
       the lines *Ls* must not begin with a blank line, and (b) if
       the list item is ordered, the start number must be 1.
    2. If any line is a *thematic break**thematic breaks* then
       that line is not a list item.

For example, let *Ls* be the lines


```
Example:
A paragraph
with two lines.

    indented code

> A block quote.

```
---
A paragraph
with two lines.

    indented code

> A block quote.

---


And let *M* be the marker `1.`, and *N* = 2.  Then rule #1 says
that the following is an ordered list item with start number 1,
and the same contents as *Ls*:


```
Example:
1.  A paragraph
    with two lines.

        indented code

    > A block quote.

```
---
1.  A paragraph
    with two lines.

        indented code

    > A block quote.

---


The most important thing to notice is that the position of
the text after the list marker determines how much indentation
is needed in subsequent blocks in the list item.  If the list
marker takes up two spaces, and there are three spaces between
the list marker and the next [non-whitespace character], then blocks
must be indented five spaces in order to fall under the list
item.

Here are some examples showing how far content must be indented to be
put under the list item:


```
Example:
- one

 two

```
---
- one

 two

---



```
Example:
- one

  two

```
---
- one

  two

---



```
Example:
 -    one

     two

```
---
 -    one

     two

---



```
Example:
 -    one

      two

```
---
 -    one

      two

---


It is tempting to think of this in terms of columns:  the continuation
blocks must be indented at least to the column of the first
[non-whitespace character] after the list marker. However, that is not quite right.
The spaces after the list marker determine how much relative indentation
is needed.  Which column this indentation reaches will depend on
how the list item is embedded in other constructions, as shown by
this example:


```
Example:
   > > 1.  one
>>
>>     two

```
---
   > > 1.  one
>>
>>     two

---


Here `two` occurs in the same column as the list marker `1.`,
but is actually contained in the list item, because there is
sufficient indentation after the last containing blockquote marker.

The converse is also possible.  In the following example, the word `two`
occurs far to the right of the initial text of the list item, `one`, but
it is not considered part of the list item, because it is not indented
far enough past the blockquote marker:


```
Example:
>>- one
>>
  >  > two

```
---
>>- one
>>
  >  > two

---


Note that at least one space is needed between the list marker and
any following content, so these are not list items:


```
Example:
-one

2.two

```
---
-one

2.two

---


A list item may contain blocks that are separated by more than
one blank line.


```
Example:
- foo


  bar

```
---
- foo


  bar

---


A list item may contain any kind of block:


```
Example:
1.  foo

    ```
    bar
    ```

    baz

    > bam

```
---
1.  foo

    ```
    bar
    ```

    baz

    > bam

---


A list item that contains an indented code block will preserve
empty lines within the code block verbatim.


```
Example:
- Foo

      bar


      baz

```
---
- Foo

      bar


      baz

---

Note that ordered list start numbers must be nine digits or less:


```
Example:
123456789. ok

```
---
123456789. ok

---



```
Example:
1234567890. not ok

```
---
1234567890. not ok

---


A start number may begin with 0s:


```
Example:
0. ok

```
---
0. ok

---



```
Example:
003. ok

```
---
003. ok

---


A start number may not be negative:


```
Example:
-1. not ok

```
---
-1. not ok

---



2.  **Item starting with indented code.**  If a sequence of lines *Ls*
    constitute a sequence of blocks *Bs* starting with an indented code
    block, and *M* is a list marker of width *W* followed by
    one space, then the result of prepending *M* and the following
    space to the first line of *Ls*, and indenting subsequent lines of
    *Ls* by *W + 1* spaces, is a list item with *Bs* as its contents.
    If a line is empty, then it need not be indented.  The type of the
    list item (bullet or ordered) is determined by the type of its list
    marker.  If the list item is ordered, then it is also assigned a
    start number, based on the ordered list marker.

An indented code block will have to be indented four spaces beyond
the edge of the region where text will be included in the list item.
In the following case that is 6 spaces:


```
Example:
- foo

      bar

```
---
- foo

      bar

---


And in this case it is 11 spaces:


```
Example:
  10.  foo

           bar

```
---
  10.  foo

           bar

---


If the *first* block in the list item is an indented code block,
then by rule #2, the contents must be indented *one* space after the
list marker:


```
Example:
    indented code

paragraph

    more code

```
---
    indented code

paragraph

    more code

---



```
Example:
1.     indented code

   paragraph

       more code

```
---
1.     indented code

   paragraph

       more code

---


Note that an additional space indent is interpreted as space
inside the code block:


```
Example:
1.      indented code

   paragraph

       more code

```
---
1.      indented code

   paragraph

       more code

---


Note that rules #1 and #2 only apply to two cases:  (a) cases
in which the lines to be included in a list item begin with a
[non-whitespace character], and (b) cases in which
they begin with an indented code
block.  In a case like the following, where the first block begins with
a three-space indent, the rules do not allow us to form a list item by
indenting the whole thing and prepending a list marker:


```
Example:
   foo

bar

```
---
   foo

bar

---



```
Example:
-    foo

  bar

```
---
-    foo

  bar

---


This is not a significant restriction, because when a block begins
with 1-3 spaces indent, the indentation can always be removed without
a change in interpretation, allowing rule #1 to be applied.  So, in
the above case:


```
Example:
-  foo

   bar

```
---
-  foo

   bar

---


3.  **Item starting with a blank line.**  If a sequence of lines *Ls*
    starting with a single *blank line* constitute a (possibly empty)
    sequence of blocks *Bs*, and *M* is a list marker of width *W*,
    then the result of prepending *M* to the first line of *Ls*, and
    indenting subsequent lines of *Ls* by *W + 1* spaces, is a list
    item with *Bs* as its contents.
    If a line is empty, then it need not be indented.  The type of the
    list item (bullet or ordered) is determined by the type of its list
    marker.  If the list item is ordered, then it is also assigned a
    start number, based on the ordered list marker.

Here are some list items that start with a blank line but are not empty:


```
Example:
-
  foo
-
  ```
  bar
  ```
-
      baz

```
---
-
  foo
-
  ```
  bar
  ```
-
      baz

---

When the list item starts with a blank line, the number of spaces
following the list marker doesn't change the required indentation:


```
Example:
-   
  foo

```
---
-   
  foo

---


A list item can begin with at most one blank line.
In the following example, `foo` is not part of the list
item:


```
Example:
-

  foo

```
---
-

  foo

---


Here is an empty bullet list item:


```
Example:
- foo
-
- bar

```
---
- foo
-
- bar

---


It does not matter whether there are spaces following the *list marker*:


```
Example:
- foo
-   
- bar

```
---
- foo
-   
- bar

---


Here is an empty ordered list item:


```
Example:
1. foo
2.
3. bar

```
---
1. foo
2.
3. bar

---


A list may start or end with an empty list item:


```
Example:
*

```
---
*

---

However, an empty list item cannot interrupt a paragraph:


```
Example:
foo
*

foo
1.

```
---
foo
*

foo
1.

---


4.  **Indentation.**  If a sequence of lines *Ls* constitutes a list item
    according to rule #1, #2, or #3, then the result of indenting each line
    of *Ls* by 1-3 spaces (the same for each line) also constitutes a
    list item with the same contents and attributes.  If a line is
    empty, then it need not be indented.

Indented one space:


```
Example:
 1.  A paragraph
     with two lines.

         indented code

     > A block quote.

```
---
 1.  A paragraph
     with two lines.

         indented code

     > A block quote.

---


Indented two spaces:


```
Example:
  1.  A paragraph
      with two lines.

          indented code

      > A block quote.

```
---
  1.  A paragraph
      with two lines.

          indented code

      > A block quote.

---


Indented three spaces:


```
Example:
   1.  A paragraph
       with two lines.

           indented code

       > A block quote.

```
---
   1.  A paragraph
       with two lines.

           indented code

       > A block quote.

---


Four spaces indent gives a code block:


```
Example:
    1.  A paragraph
        with two lines.

            indented code

        > A block quote.

```
---
    1.  A paragraph
        with two lines.

            indented code

        > A block quote.

---



5.  **Laziness.**  If a string of lines *Ls* constitute a [list
    item](#list-items) with contents *Bs*, then the result of deleting
    some or all of the indentation from one or more lines in which the
    next [non-whitespace character] after the indentation is
    *paragraph continuation text* is a
    list item with the same contents and attributes.  The unindented
    lines are called
    **lazy continuation line**s.

Here is an example with *lazy continuation lines*:


```
Example:
  1.  A paragraph
with two lines.

          indented code

      > A block quote.

```
---
  1.  A paragraph
with two lines.

          indented code

      > A block quote.

---


Indentation can be partially deleted:


```
Example:
  1.  A paragraph
    with two lines.

```
---
  1.  A paragraph
    with two lines.

---


These examples show how laziness can work in nested structures:


```
Example:
> 1. > Blockquote
continued here.

```
---
> 1. > Blockquote
continued here.

---



```
Example:
> 1. > Blockquote
> continued here.

```
---
> 1. > Blockquote
> continued here.

---



6.  **That's all.** Nothing that is not counted as a list item by rules
    #1--5 counts as a [list item](#list-items).

The rules for sublists follow from the general rules
*above**List items*.  A sublist must be indented the same number
of spaces a paragraph would need to be in order to be included
in the list item.

So, in this case we need two spaces indent:


```
Example:
- foo
  - bar
    - baz
      - boo

```
---
- foo
  - bar
    - baz
      - boo

---


One is not enough:


```
Example:
- foo
 - bar
  - baz
   - boo

```
---
- foo
 - bar
  - baz
   - boo

---


Here we need four, because the list marker is wider:


```
Example:
10) foo
    - bar

```
---
10) foo
    - bar

---


Three is not enough:


```
Example:
10) foo
   - bar

```
---
10) foo
   - bar

---


A list may be the first block in a list item:


```
Example:
- - foo

```
---
- - foo

---



```
Example:
1. - 2. foo

```
---
1. - 2. foo

---


A list item can contain a heading:


```
Example:
- # Foo
- Bar
  ---
  baz

```
---
- # Foo
- Bar
  ---
  baz

---


### Motivation

John Gruber's Markdown spec says the following about list items:

1. "List markers typically start at the left margin, but may be indented
   by up to three spaces. List markers must be followed by one or more
   spaces or a tab."

2. "To make lists look nice, you can wrap items with hanging indents....
   But if you don't want to, you don't have to."

3. "List items may consist of multiple paragraphs. Each subsequent
   paragraph in a list item must be indented by either 4 spaces or one
   tab."

4. "It looks nice if you indent every line of the subsequent paragraphs,
   but here again, Markdown will allow you to be lazy."

5. "To put a blockquote within a list item, the blockquote's `>`
   delimiters need to be indented."

6. "To put a code block within a list item, the code block needs to be
   indented twice — 8 spaces or two tabs."

These rules specify that a paragraph under a list item must be indented
four spaces (presumably, from the left margin, rather than the start of
the list marker, but this is not said), and that code under a list item
must be indented eight spaces instead of the usual four.  They also say
that a block quote must be indented, but not by how much; however, the
example given has four spaces indentation.  Although nothing is said
about other kinds of block-level content, it is certainly reasonable to
infer that *all* block elements under a list item, including other
lists, must be indented four spaces.  This principle has been called the
*four-space rule*.

The four-space rule is clear and principled, and if the reference
implementation `Markdown.pl` had followed it, it probably would have
become the standard.  However, `Markdown.pl` allowed paragraphs and
sublists to start with only two spaces indentation, at least on the
outer level.  Worse, its behavior was inconsistent: a sublist of an
outer-level list needed two spaces indentation, but a sublist of this
sublist needed three spaces.  It is not surprising, then, that different
implementations of Markdown have developed very different rules for
determining what comes under a list item.  (Pandoc and python-Markdown,
for example, stuck with Gruber's syntax description and the four-space
rule, while discount, redcarpet, marked, PHP Markdown, and others
followed `Markdown.pl`'s behavior more closely.)

Unfortunately, given the divergences between implementations, there
is no way to give a spec for list items that will be guaranteed not
to break any existing documents.  However, the spec given here should
correctly handle lists formatted with either the four-space rule or
the more forgiving `Markdown.pl` behavior, provided they are laid out
in a way that is natural for a human to read.

The strategy here is to let the width and indentation of the list marker
determine the indentation necessary for blocks to fall under the list
item, rather than having a fixed and arbitrary number.  The writer can
think of the body of the list item as a unit which gets indented to the
right enough to fit the list marker (and any indentation on the list
marker).  (The laziness rule, #5, then allows continuation lines to be
unindented if needed.)

This rule is superior, we claim, to any rule requiring a fixed level of
indentation from the margin.  The four-space rule is clear but
unnatural. It is quite unintuitive that

``` markdown
- foo

  bar

  - baz
```

should be parsed as two lists with an intervening paragraph,

``` html
<ul>
<li>foo</li>
</ul>
<p>bar</p>
<ul>
<li>baz</li>
</ul>
```

as the four-space rule demands, rather than a single list,

``` html
<ul>
<li>
<p>foo</p>
<p>bar</p>
<ul>
<li>baz</li>
</ul>
</li>
</ul>
```

The choice of four spaces is arbitrary.  It can be learned, but it is
not likely to be guessed, and it trips up beginners regularly.

Would it help to adopt a two-space rule?  The problem is that such
a rule, together with the rule allowing 1--3 spaces indentation of the
initial list marker, allows text that is indented *less than* the
original list marker to be included in the list item. For example,
`Markdown.pl` parses

``` markdown
   - one

  two
```

as a single list item, with `two` a continuation paragraph:

``` html
<ul>
<li>
<p>one</p>
<p>two</p>
</li>
</ul>
```

and similarly

``` markdown
>   - one
>
>  two
```

as

``` html
<blockquote>
<ul>
<li>
<p>one</p>
<p>two</p>
</li>
</ul>
</blockquote>
```

This is extremely unintuitive.

Rather than requiring a fixed indent from the margin, we could require
a fixed indent (say, two spaces, or even one space) from the list marker (which
may itself be indented).  This proposal would remove the last anomaly
discussed.  Unlike the spec presented above, it would count the following
as a list item with a subparagraph, even though the paragraph `bar`
is not indented as far as the first paragraph `foo`:

``` markdown
 10. foo

   bar  
```

Arguably this text does read like a list item with `bar` as a subparagraph,
which may count in favor of the proposal.  However, on this proposal indented
code would have to be indented six spaces after the list marker.  And this
would break a lot of existing Markdown, which has the pattern:

``` markdown
1.  foo

        indented code
```

where the code is indented eight spaces.  The spec above, by contrast, will
parse this text as expected, since the code block's indentation is measured
from the beginning of `foo`.

The one case that needs special treatment is a list item that *starts*
with indented code.  How much indentation is required in that case, since
we don't have a "first paragraph" to measure from?  Rule #2 simply stipulates
that in such cases, we require one space indentation from the list marker
(and then the normal four spaces for the indented code).  This will match the
four-space rule in cases where the list marker plus its initial indentation
takes four spaces (a common case), but diverge in other cases.

## Lists

A **list** is a sequence of one or more
list items *of the same type*.  The list items
may be separated by any number of blank lines.

Two list items are **of the same type**
if they begin with a *list marker* of the same type.
Two list markers are of the
same type if (a) they are bullet list markers using the same character
(`-`, `+`, or `*`) or (b) they are ordered list numbers with the same
delimiter (either `.` or `)`).

A list is an **ordered list**
if its constituent list items begin with
*ordered list markers*, and a
**bullet list** if its constituent list
items begin with *bullet list markers*.

The **start number**
of an *ordered list* is determined by the list number of
its initial list item.  The numbers of subsequent list items are
disregarded.

A list is **loose** if any of its constituent
list items are separated by blank lines, or if any of its constituent
list items directly contain two block-level elements with a blank line
between them.  Otherwise a list is **tight**.
(The difference in HTML output is that paragraphs in a loose list are
wrapped in `<p>` tags, while paragraphs in a tight list are not.)

Changing the bullet or ordered list delimiter starts a new list:


```
Example:
- foo
- bar
+ baz

```
---
- foo
- bar
+ baz

---



```
Example:
1. foo
2. bar
3) baz

```
---
1. foo
2. bar
3) baz

---


In CommonMark, a list can interrupt a paragraph. That is,
no blank line is needed to separate a paragraph from a following
list:


```
Example:
Foo
- bar
- baz

```
---
Foo
- bar
- baz

---

`Markdown.pl` does not allow this, through fear of triggering a list
via a numeral in a hard-wrapped line:

``` markdown
The number of windows in my house is
14.  The number of doors is 6.
```

Oddly, though, `Markdown.pl` *does* allow a blockquote to
interrupt a paragraph, even though the same considerations might
apply.

In CommonMark, we do allow lists to interrupt paragraphs, for
two reasons.  First, it is natural and not uncommon for people
to start lists without blank lines:

``` markdown
I need to buy
- new shoes
- a coat
- a plane ticket
```

Second, we are attracted to a

> **principle of uniformity**:
> if a chunk of text has a certain
> meaning, it will continue to have the same meaning when put into a
> container block (such as a list item or blockquote).

(Indeed, the spec for *list items* and *block quotes* presupposes
this principle.) This principle implies that if

``` markdown
  * I need to buy
    - new shoes
    - a coat
    - a plane ticket
```

is a list item containing a paragraph followed by a nested sublist,
as all Markdown implementations agree it is (though the paragraph
may be rendered without `<p>` tags, since the list is "tight"),
then

``` markdown
I need to buy
- new shoes
- a coat
- a plane ticket
```

by itself should be a paragraph followed by a nested sublist.

Since it is well established Markdown practice to allow lists to
interrupt paragraphs inside list items, the *principle of
uniformity* requires us to allow this outside list items as
well.  ([reStructuredText](http://docutils.sourceforge.net/rst.html)
takes a different approach, requiring blank lines before lists
even inside other list items.)

In order to solve of unwanted lists in paragraphs with
hard-wrapped numerals, we allow only lists starting with `1` to
interrupt paragraphs.  Thus,


```
Example:
The number of windows in my house is
14.  The number of doors is 6.

```
---
The number of windows in my house is
14.  The number of doors is 6.

---

We may still get an unintended result in cases like


```
Example:
The number of windows in my house is
1.  The number of doors is 6.

```
---
The number of windows in my house is
1.  The number of doors is 6.

---

but this rule should prevent most spurious list captures.

There can be any number of blank lines between items:


```
Example:
- foo

- bar


- baz

```
---
- foo

- bar


- baz

---


```
Example:
- foo
  - bar
    - baz


      bim

```
---
- foo
  - bar
    - baz


      bim

---


To separate consecutive lists of the same type, or to separate a
list from an indented code block that would otherwise be parsed
as a subparagraph of the final list item, you can insert a blank HTML
comment:


```
Example:
- foo
- bar

<!-- -->

- baz
- bim

```
---
- foo
- bar

<!-- -->

- baz
- bim

---



```
Example:
-   foo

    notcode

-   foo

<!-- -->

    code

```
---
-   foo

    notcode

-   foo

<!-- -->

    code

---


List items need not be indented to the same level.  The following
list items will be treated as items at the same list level,
since none is indented enough to belong to the previous list
item:


```
Example:
- a
 - b
  - c
   - d
  - e
 - f
- g

```
---
- a
 - b
  - c
   - d
  - e
 - f
- g

---



```
Example:
1. a

  2. b

   3. c

```
---
1. a

  2. b

   3. c

---

Note, however, that list items may not be indented more than
three spaces.  Here `- e` is treated as a paragraph continuation
line, because it is indented more than three spaces:


```
Example:
- a
 - b
  - c
   - d
    - e

```
---
- a
 - b
  - c
   - d
    - e

---

And here, `3. c` is treated as in indented code block,
because it is indented four spaces and preceded by a
blank line.


```
Example:
1. a

  2. b

    3. c

```
---
1. a

  2. b

    3. c

---


This is a loose list, because there is a blank line between
two of the list items:


```
Example:
- a
- b

- c

```
---
- a
- b

- c

---


So is this, with a empty second item:


```
Example:
* a
*

* c

```
---
* a
*

* c

---


These are loose lists, even though there is no space between the items,
because one of the items directly contains two block-level elements
with a blank line between them:


```
Example:
- a
- b

  c
- d

```
---
- a
- b

  c
- d

---



```
Example:
- a
- b

  *ref*: /url
- d

```
---
- a
- b

  *ref*: /url
- d

---


This is a tight list, because the blank lines are in a code block:


```
Example:
- a
- ```
  b


  ```
- c

```
---
- a
- ```
  b


  ```
- c

---


This is a tight list, because the blank line is between two
paragraphs of a sublist.  So the sublist is loose while
the outer list is tight:


```
Example:
- a
  - b

    c
- d

```
---
- a
  - b

    c
- d

---


This is a tight list, because the blank line is inside the
block quote:


```
Example:
* a
  > b
  >
* c

```
---
* a
  > b
  >
* c

---


This list is tight, because the consecutive block elements
are not separated by blank lines:


```
Example:
- a
  > b
  ```
  c
  ```
- d

```
---
- a
  > b
  ```
  c
  ```
- d

---


A single-paragraph list is tight:


```
Example:
- a

```
---
- a

---



```
Example:
- a
  - b

```
---
- a
  - b

---


This list is loose, because of the blank line between the
two block elements in the list item:


```
Example:
1. ```
   foo
   ```

   bar

```
---
1. ```
   foo
   ```

   bar

---


Here the outer list is loose, the inner list tight:


```
Example:
* foo
  * bar

  baz

```
---
* foo
  * bar

  baz

---



```
Example:
- a
  - b
  - c

- d
  - e
  - f

```
---
- a
  - b
  - c

- d
  - e
  - f

---


# Inlines

Inlines are parsed sequentially from the beginning of the character
stream to the end (left to right, in left-to-right languages).
Thus, for example, in


```
Example:
`hi`lo`

```
---
`hi`lo`

---

`hi` is parsed as code, leaving the backtick at the end as a literal
backtick.



## Code spans

A **backtick string**
is a string of one or more backtick characters (`` ` ``) that is neither
preceded nor followed by a backtick.

A **code span** begins with a backtick string and ends with
a backtick string of equal length.  The contents of the code span are
the characters between these two backtick strings, normalized in the
following ways:

- First, *line endings* are converted to *spaces*.
- If the resulting string both begins *and* ends with a *space*
  character, but does not consist entirely of *space*
  characters, a single *space* character is removed from the
  front and back.  This allows you to include code that begins
  or ends with backtick characters, which must be separated by
  whitespace from the opening or closing backtick strings.

This is a simple code span:


```
Example:
`foo`

```
---
`foo`

---


Here two backticks are used, because the code contains a backtick.
This example also illustrates stripping of a single leading and
trailing space:


```
Example:
`` foo ` bar ``

```
---
`` foo ` bar ``

---


This example shows the motivation for stripping leading and trailing
spaces:


```
Example:
` `` `

```
---
` `` `

---

Note that only *one* space is stripped:


```
Example:
`  ``  `

```
---
`  ``  `

---

The stripping only happens if the space is on both
sides of the string:


```
Example:
` a`

```
---
` a`

---

Only *spaces*, and not *unicode whitespace* in general, are
stripped in this way:


```
Example:
` b `

```
---
` b `

---

No stripping occurs if the code span contains only spaces:


```
Example:
` `
`  `

```
---
` `
`  `

---


*Line endings* are treated like spaces:


```
Example:
``
foo
bar  
baz
``

```
---
``
foo
bar  
baz
``

---


```
Example:
``
foo 
``

```
---
``
foo 
``

---


Interior spaces are not collapsed:


```
Example:
`foo   bar 
baz`

```
---
`foo   bar 
baz`

---

Note that browsers will typically collapse consecutive spaces
when rendering `<code>` elements, so it is recommended that
the following CSS be used:

    code{white-space: pre-wrap;}


Note that backslash escapes do not work in code spans. All backslashes
are treated literally:


```
Example:
`foo\`bar`

```
---
`foo\`bar`

---


Backslash escapes are never needed, because one can always choose a
string of *n* backtick characters as delimiters, where the code does
not contain any strings of exactly *n* backtick characters.


```
Example:
``foo`bar``

```
---
``foo`bar``

---


```
Example:
` foo `` bar `

```
---
` foo `` bar `

---


Code span backticks have higher precedence than any other inline
constructs except HTML tags and autolinks.  Thus, for example, this is
not parsed as emphasized text, since the second `*` is part of a code
span:


```
Example:
*foo`*`

```
---
*foo`*`

---


And this is not parsed as a link:


```
Example:
[not a `link](/foo`)

```
---
[not a `link](/foo`)

---


Code spans, HTML tags, and autolinks have the same precedence.
Thus, this is code:


```
Example:
`<a href="`">`

```
---
`<a href="`">`

---


But this is an HTML tag:


```
Example:
<a href="`">`

```
---
<a href="`">`

---


And this is code:


```
Example:
`<http://foo.bar.`baz>`

```
---
`<http://foo.bar.`baz>`

---


But this is an autolink:


```
Example:
<http://foo.bar.`baz>`

```
---
<http://foo.bar.`baz>`

---


When a backtick string is not closed by a matching backtick string,
we just have literal backticks:


```
Example:
```foo``

```
---
```foo``

---



```
Example:
`foo

```
---
`foo

---

The following case also illustrates the need for opening and
closing backtick strings to be equal in length:


```
Example:
`foo``bar``

```
---
`foo``bar``

---


## Emphasis and strong emphasis

John Gruber's original [Markdown syntax
description](http://daringfireball.net/projects/markdown/syntax#em) says:

> Markdown treats asterisks (`*`) and underscores (`_`) as indicators of
> emphasis. Text wrapped with one `*` or `_` will be wrapped with an HTML
> `<em>` tag; double `*`'s or `_`'s will be wrapped with an HTML `<strong>`
> tag.

This is enough for most users, but these rules leave much undecided,
especially when it comes to nested emphasis.  The original
`Markdown.pl` test suite makes it clear that triple `***` and
`___` delimiters can be used for strong emphasis, and most
implementations have also allowed the following patterns:

``` markdown
***strong emph***
***strong** in emph*
***emph* in strong**
**in strong *emph***
*in emph **strong***
```

The following patterns are less widely supported, but the intent
is clear and they are useful (especially in contexts like bibliography
entries):

``` markdown
*emph *with emph* in it*
**strong **with strong** in it**
```

Many implementations have also restricted intraword emphasis to
the `*` forms, to avoid unwanted emphasis in words containing
internal underscores.  (It is best practice to put these in code
spans, but users often do not.)

``` markdown
internal emphasis: foo*bar*baz
no emphasis: foo_bar_baz
```

The rules given below capture all of these patterns, while allowing
for efficient parsing strategies that do not backtrack.

First, some definitions.  A **delimiter run** is either
a sequence of one or more `*` characters that is not preceded or
followed by a non-backslash-escaped `*` character, or a sequence
of one or more `_` characters that is not preceded or followed by
a non-backslash-escaped `_` character.

A [left-flanking delimiter run](@) is
a *delimiter run* that is (1) not followed by *Unicode whitespace*,
and either (2a) not followed by a *punctuation character*, or
(2b) followed by a *punctuation character* and
preceded by *Unicode whitespace* or a *punctuation character*.
For purposes of this definition, the beginning and the end of
the line count as Unicode whitespace.

A [right-flanking delimiter run](@) is
a *delimiter run* that is (1) not preceded by *Unicode whitespace*,
and either (2a) not preceded by a *punctuation character*, or
(2b) preceded by a *punctuation character* and
followed by *Unicode whitespace* or a *punctuation character*.
For purposes of this definition, the beginning and the end of
the line count as Unicode whitespace.

Here are some examples of delimiter runs.

  - left-flanking but not right-flanking:

    ```
    ***abc
      _abc
    **"abc"
     _"abc"
    ```

  - right-flanking but not left-flanking:

    ```
     abc***
     abc_
    "abc"**
    "abc"_
    ```

  - Both left and right-flanking:

    ```
     abc***def
    "abc"_"def"
    ```

  - Neither left nor right-flanking:

    ```
    abc *** def
    a _ b
    ```

(The idea of distinguishing left-flanking and right-flanking
delimiter runs based on the character before and the character
after comes from Roopesh Chander's
[vfmd](http://www.vfmd.org/vfmd-spec/specification/#procedure-for-identifying-emphasis-tags).
vfmd uses the terminology "emphasis indicator string" instead of "delimiter
run," and its rules for distinguishing left- and right-flanking runs
are a bit more complex than the ones given here.)

The following rules define emphasis and strong emphasis:

1.  A single `*` character **can open emphasis**
    iff (if and only if) it is part of a [left-flanking delimiter run].

2.  A single `_` character *can open emphasis* iff
    it is part of a [left-flanking delimiter run]
    and either (a) not part of a [right-flanking delimiter run]
    or (b) part of a [right-flanking delimiter run]
    preceded by punctuation.

3.  A single `*` character **can close emphasis**
    iff it is part of a [right-flanking delimiter run].

4.  A single `_` character *can close emphasis* iff
    it is part of a [right-flanking delimiter run]
    and either (a) not part of a [left-flanking delimiter run]
    or (b) part of a [left-flanking delimiter run]
    followed by punctuation.

5.  A double `**` **can open strong emphasis**
    iff it is part of a [left-flanking delimiter run].

6.  A double `__` *can open strong emphasis* iff
    it is part of a [left-flanking delimiter run]
    and either (a) not part of a [right-flanking delimiter run]
    or (b) part of a [right-flanking delimiter run]
    preceded by punctuation.

7.  A double `**` **can close strong emphasis**
    iff it is part of a [right-flanking delimiter run].

8.  A double `__` *can close strong emphasis* iff
    it is part of a [right-flanking delimiter run]
    and either (a) not part of a [left-flanking delimiter run]
    or (b) part of a [left-flanking delimiter run]
    followed by punctuation.

9.  Emphasis begins with a delimiter that *can open emphasis* and ends
    with a delimiter that *can close emphasis*, and that uses the same
    character (`_` or `*`) as the opening delimiter.  The
    opening and closing delimiters must belong to separate
    *delimiter runs*.  If one of the delimiters can both
    open and close emphasis, then the sum of the lengths of the
    delimiter runs containing the opening and closing delimiters
    must not be a multiple of 3 unless both lengths are
    multiples of 3.

10. Strong emphasis begins with a delimiter that
    *can open strong emphasis* and ends with a delimiter that
    *can close strong emphasis*, and that uses the same character
    (`_` or `*`) as the opening delimiter.  The
    opening and closing delimiters must belong to separate
    *delimiter runs*.  If one of the delimiters can both open
    and close strong emphasis, then the sum of the lengths of
    the delimiter runs containing the opening and closing
    delimiters must not be a multiple of 3 unless both lengths
    are multiples of 3.

11. A literal `*` character cannot occur at the beginning or end of
    `*`-delimited emphasis or `**`-delimited strong emphasis, unless it
    is backslash-escaped.

12. A literal `_` character cannot occur at the beginning or end of
    `_`-delimited emphasis or `__`-delimited strong emphasis, unless it
    is backslash-escaped.

Where rules 1--12 above are compatible with multiple parsings,
the following principles resolve ambiguity:

13. The number of nestings should be minimized. Thus, for example,
    an interpretation `<strong>...</strong>` is always preferred to
    `<em><em>...</em></em>`.

14. An interpretation `<em><strong>...</strong></em>` is always
    preferred to `<strong><em>...</em></strong>`.

15. When two potential emphasis or strong emphasis spans overlap,
    so that the second begins before the first ends and ends after
    the first ends, the first takes precedence. Thus, for example,
    `*foo _bar* baz_` is parsed as `<em>foo _bar</em> baz_` rather
    than `*foo <em>bar* baz</em>`.

16. When there are two potential emphasis or strong emphasis spans
    with the same closing delimiter, the shorter one (the one that
    opens later) takes precedence. Thus, for example,
    `**foo **bar baz**` is parsed as `**foo <strong>bar baz</strong>`
    rather than `<strong>foo **bar baz</strong>`.

17. Inline code spans, links, images, and HTML tags group more tightly
    than emphasis.  So, when there is a choice between an interpretation
    that contains one of these elements and one that does not, the
    former always wins.  Thus, for example, `*[foo*](bar)` is
    parsed as `*<a href="bar">foo*</a>` rather than as
    `<em>[foo</em>](bar)`.

These rules can be illustrated through a series of examples.

Rule 1:


```
Example:
*foo bar*

```
---
*foo bar*

---


This is not emphasis, because the opening `*` is followed by
whitespace, and hence not part of a [left-flanking delimiter run]:


```
Example:
a * foo bar*

```
---
a * foo bar*

---


This is not emphasis, because the opening `*` is preceded
by an alphanumeric and followed by punctuation, and hence
not part of a [left-flanking delimiter run]:


```
Example:
a*"foo"*

```
---
a*"foo"*

---


Unicode nonbreaking spaces count as whitespace, too:


```
Example:
* a *

```
---
* a *

---


Intraword emphasis with `*` is permitted:


```
Example:
foo*bar*

```
---
foo*bar*

---



```
Example:
5*6*78

```
---
5*6*78

---


Rule 2:


```
Example:
_foo bar_

```
---
_foo bar_

---


This is not emphasis, because the opening `_` is followed by
whitespace:


```
Example:
_ foo bar_

```
---
_ foo bar_

---


This is not emphasis, because the opening `_` is preceded
by an alphanumeric and followed by punctuation:


```
Example:
a_"foo"_

```
---
a_"foo"_

---


Emphasis with `_` is not allowed inside words:


```
Example:
foo_bar_

```
---
foo_bar_

---



```
Example:
5_6_78

```
---
5_6_78

---



```
Example:
пристаням_стремятся_

```
---
пристаням_стремятся_

---


Here `_` does not generate emphasis, because the first delimiter run
is right-flanking and the second left-flanking:


```
Example:
aa_"bb"_cc

```
---
aa_"bb"_cc

---


This is emphasis, even though the opening delimiter is
both left- and right-flanking, because it is preceded by
punctuation:


```
Example:
foo-_(bar)_

```
---
foo-_(bar)_

---


Rule 3:

This is not emphasis, because the closing delimiter does
not match the opening delimiter:


```
Example:
_foo*

```
---
_foo*

---


This is not emphasis, because the closing `*` is preceded by
whitespace:


```
Example:
*foo bar *

```
---
*foo bar *

---


A newline also counts as whitespace:


```
Example:
*foo bar
*

```
---
*foo bar
*

---


This is not emphasis, because the second `*` is
preceded by punctuation and followed by an alphanumeric
(hence it is not part of a [right-flanking delimiter run]:


```
Example:
*(*foo)

```
---
*(*foo)

---


The point of this restriction is more easily appreciated
with this example:


```
Example:
*(*foo*)*

```
---
*(*foo*)*

---


Intraword emphasis with `*` is allowed:


```
Example:
*foo*bar

```
---
*foo*bar

---



Rule 4:

This is not emphasis, because the closing `_` is preceded by
whitespace:


```
Example:
_foo bar _

```
---
_foo bar _

---


This is not emphasis, because the second `_` is
preceded by punctuation and followed by an alphanumeric:


```
Example:
_(_foo)

```
---
_(_foo)

---


This is emphasis within emphasis:


```
Example:
_(_foo_)_

```
---
_(_foo_)_

---


Intraword emphasis is disallowed for `_`:


```
Example:
_foo_bar

```
---
_foo_bar

---



```
Example:
_пристаням_стремятся

```
---
_пристаням_стремятся

---



```
Example:
_foo_bar_baz_

```
---
_foo_bar_baz_

---


This is emphasis, even though the closing delimiter is
both left- and right-flanking, because it is followed by
punctuation:


```
Example:
_(bar)_.

```
---
_(bar)_.

---


Rule 5:


```
Example:
**foo bar**

```
---
**foo bar**

---


This is not strong emphasis, because the opening delimiter is
followed by whitespace:


```
Example:
** foo bar**

```
---
** foo bar**

---


This is not strong emphasis, because the opening `**` is preceded
by an alphanumeric and followed by punctuation, and hence
not part of a [left-flanking delimiter run]:


```
Example:
a**"foo"**

```
---
a**"foo"**

---


Intraword strong emphasis with `**` is permitted:


```
Example:
foo**bar**

```
---
foo**bar**

---


Rule 6:


```
Example:
__foo bar__

```
---
__foo bar__

---


This is not strong emphasis, because the opening delimiter is
followed by whitespace:


```
Example:
__ foo bar__

```
---
__ foo bar__

---


A newline counts as whitespace:

```
Example:
__
foo bar__

```
---
__
foo bar__

---


This is not strong emphasis, because the opening `__` is preceded
by an alphanumeric and followed by punctuation:


```
Example:
a__"foo"__

```
---
a__"foo"__

---


Intraword strong emphasis is forbidden with `__`:


```
Example:
foo__bar__

```
---
foo__bar__

---



```
Example:
5__6__78

```
---
5__6__78

---



```
Example:
пристаням__стремятся__

```
---
пристаням__стремятся__

---



```
Example:
__foo, __bar__, baz__

```
---
__foo, __bar__, baz__

---


This is strong emphasis, even though the opening delimiter is
both left- and right-flanking, because it is preceded by
punctuation:


```
Example:
foo-__(bar)__

```
---
foo-__(bar)__

---



Rule 7:

This is not strong emphasis, because the closing delimiter is preceded
by whitespace:


```
Example:
**foo bar **

```
---
**foo bar **

---


(Nor can it be interpreted as an emphasized `*foo bar *`, because of
Rule 11.)

This is not strong emphasis, because the second `**` is
preceded by punctuation and followed by an alphanumeric:


```
Example:
**(**foo)

```
---
**(**foo)

---


The point of this restriction is more easily appreciated
with these examples:


```
Example:
*(**foo**)*

```
---
*(**foo**)*

---



```
Example:
**Gomphocarpus (*Gomphocarpus physocarpus*, syn.
*Asclepias physocarpa*)**

```
---
**Gomphocarpus (*Gomphocarpus physocarpus*, syn.
*Asclepias physocarpa*)**

---



```
Example:
**foo "*bar*" foo**

```
---
**foo "*bar*" foo**

---


Intraword emphasis:


```
Example:
**foo**bar

```
---
**foo**bar

---


Rule 8:

This is not strong emphasis, because the closing delimiter is
preceded by whitespace:


```
Example:
__foo bar __

```
---
__foo bar __

---


This is not strong emphasis, because the second `__` is
preceded by punctuation and followed by an alphanumeric:


```
Example:
__(__foo)

```
---
__(__foo)

---


The point of this restriction is more easily appreciated
with this example:


```
Example:
_(__foo__)_

```
---
_(__foo__)_

---


Intraword strong emphasis is forbidden with `__`:


```
Example:
__foo__bar

```
---
__foo__bar

---



```
Example:
__пристаням__стремятся

```
---
__пристаням__стремятся

---



```
Example:
__foo__bar__baz__

```
---
__foo__bar__baz__

---


This is strong emphasis, even though the closing delimiter is
both left- and right-flanking, because it is followed by
punctuation:


```
Example:
__(bar)__.

```
---
__(bar)__.

---


Rule 9:

Any nonempty sequence of inline elements can be the contents of an
emphasized span.


```
Example:
*foo [bar](/url)*

```
---
*foo [bar](/url)*

---



```
Example:
*foo
bar*

```
---
*foo
bar*

---


In particular, emphasis and strong emphasis can be nested
inside emphasis:


```
Example:
_foo __bar__ baz_

```
---
_foo __bar__ baz_

---



```
Example:
_foo _bar_ baz_

```
---
_foo _bar_ baz_

---



```
Example:
__foo_ bar_

```
---
__foo_ bar_

---



```
Example:
*foo *bar**

```
---
*foo *bar**

---



```
Example:
*foo **bar** baz*

```
---
*foo **bar** baz*

---


```
Example:
*foo**bar**baz*

```
---
*foo**bar**baz*

---

Note that in the preceding case, the interpretation

``` markdown
<p><em>foo</em><em>bar<em></em>baz</em></p>
```


is precluded by the condition that a delimiter that
can both open and close (like the `*` after `foo`)
cannot form emphasis if the sum of the lengths of
the delimiter runs containing the opening and
closing delimiters is a multiple of 3 unless
both lengths are multiples of 3.


For the same reason, we don't get two consecutive
emphasis sections in this example:


```
Example:
*foo**bar*

```
---
*foo**bar*

---


The same condition ensures that the following
cases are all strong emphasis nested inside
emphasis, even when the interior spaces are
omitted:



```
Example:
***foo** bar*

```
---
***foo** bar*

---



```
Example:
*foo **bar***

```
---
*foo **bar***

---



```
Example:
*foo**bar***

```
---
*foo**bar***

---


When the lengths of the interior closing and opening
delimiter runs are *both* multiples of 3, though,
they can match to create emphasis:


```
Example:
foo***bar***baz

```
---
foo***bar***baz

---


```
Example:
foo******bar*********baz

```
---
foo******bar*********baz

---


Indefinite levels of nesting are possible:


```
Example:
*foo **bar *baz* bim** bop*

```
---
*foo **bar *baz* bim** bop*

---



```
Example:
*foo [*bar*](/url)*

```
---
*foo [*bar*](/url)*

---


There can be no empty emphasis or strong emphasis:


```
Example:
** is not an empty emphasis

```
---
** is not an empty emphasis

---



```
Example:
**** is not an empty strong emphasis

```
---
**** is not an empty strong emphasis

---



Rule 10:

Any nonempty sequence of inline elements can be the contents of an
strongly emphasized span.


```
Example:
**foo [bar](/url)**

```
---
**foo [bar](/url)**

---



```
Example:
**foo
bar**

```
---
**foo
bar**

---


In particular, emphasis and strong emphasis can be nested
inside strong emphasis:


```
Example:
__foo _bar_ baz__

```
---
__foo _bar_ baz__

---



```
Example:
__foo __bar__ baz__

```
---
__foo __bar__ baz__

---



```
Example:
____foo__ bar__

```
---
____foo__ bar__

---



```
Example:
**foo **bar****

```
---
**foo **bar****

---



```
Example:
**foo *bar* baz**

```
---
**foo *bar* baz**

---



```
Example:
**foo*bar*baz**

```
---
**foo*bar*baz**

---



```
Example:
***foo* bar**

```
---
***foo* bar**

---



```
Example:
**foo *bar***

```
---
**foo *bar***

---


Indefinite levels of nesting are possible:


```
Example:
**foo *bar **baz**
bim* bop**

```
---
**foo *bar **baz**
bim* bop**

---



```
Example:
**foo [*bar*](/url)**

```
---
**foo [*bar*](/url)**

---


There can be no empty emphasis or strong emphasis:


```
Example:
__ is not an empty emphasis

```
---
__ is not an empty emphasis

---



```
Example:
____ is not an empty strong emphasis

```
---
____ is not an empty strong emphasis

---



Rule 11:


```
Example:
foo ***

```
---
foo ***

---



```
Example:
foo *\**

```
---
foo *\**

---



```
Example:
foo *_*

```
---
foo *_*

---



```
Example:
foo *****

```
---
foo *****

---



```
Example:
foo **\***

```
---
foo **\***

---



```
Example:
foo **_**

```
---
foo **_**

---


Note that when delimiters do not match evenly, Rule 11 determines
that the excess literal `*` characters will appear outside of the
emphasis, rather than inside it:


```
Example:
**foo*

```
---
**foo*

---



```
Example:
*foo**

```
---
*foo**

---



```
Example:
***foo**

```
---
***foo**

---



```
Example:
****foo*

```
---
****foo*

---



```
Example:
**foo***

```
---
**foo***

---



```
Example:
*foo****

```
---
*foo****

---



Rule 12:


```
Example:
foo ___

```
---
foo ___

---



```
Example:
foo _\__

```
---
foo _\__

---



```
Example:
foo _*_

```
---
foo _*_

---



```
Example:
foo _____

```
---
foo _____

---



```
Example:
foo __\___

```
---
foo __\___

---



```
Example:
foo __*__

```
---
foo __*__

---



```
Example:
__foo_

```
---
__foo_

---


Note that when delimiters do not match evenly, Rule 12 determines
that the excess literal `_` characters will appear outside of the
emphasis, rather than inside it:


```
Example:
_foo__

```
---
_foo__

---



```
Example:
___foo__

```
---
___foo__

---



```
Example:
____foo_

```
---
____foo_

---



```
Example:
__foo___

```
---
__foo___

---



```
Example:
_foo____

```
---
_foo____

---


Rule 13 implies that if you want emphasis nested directly inside
emphasis, you must use different delimiters:


```
Example:
**foo**

```
---
**foo**

---



```
Example:
*_foo_*

```
---
*_foo_*

---



```
Example:
__foo__

```
---
__foo__

---



```
Example:
_*foo*_

```
---
_*foo*_

---


However, strong emphasis within strong emphasis is possible without
switching delimiters:


```
Example:
****foo****

```
---
****foo****

---



```
Example:
____foo____

```
---
____foo____

---



Rule 13 can be applied to arbitrarily long sequences of
delimiters:


```
Example:
******foo******

```
---
******foo******

---


Rule 14:


```
Example:
***foo***

```
---
***foo***

---



```
Example:
_____foo_____

```
---
_____foo_____

---


Rule 15:


```
Example:
*foo _bar* baz_

```
---
*foo _bar* baz_

---



```
Example:
*foo __bar *baz bim__ bam*

```
---
*foo __bar *baz bim__ bam*

---


Rule 16:


```
Example:
**foo **bar baz**

```
---
**foo **bar baz**

---



```
Example:
*foo *bar baz*

```
---
*foo *bar baz*

---


Rule 17:


```
Example:
*[bar*](/url)

```
---
*[bar*](/url)

---



```
Example:
_foo [bar_](/url)

```
---
_foo [bar_](/url)

---



```
Example:
*<img src="foo" title="*"/>

```
---
*<img src="foo" title="*"/>

---



```
Example:
**<a href="**">

```
---
**<a href="**">

---



```
Example:
__<a href="__">

```
---
__<a href="__">

---



```
Example:
*a `*`*

```
---
*a `*`*

---



```
Example:
_a `_`_

```
---
_a `_`_

---



```
Example:
**a<http://foo.bar/?q=**>

```
---
**a<http://foo.bar/?q=**>

---



```
Example:
__a<http://foo.bar/?q=__>

```
---
__a<http://foo.bar/?q=__>

---



## Links

A link contains *link text* (the visible text), a *link destination*
(the URI that is the link destination), and optionally a *link title*.
There are two basic kinds of links in Markdown.  In *inline links* the
destination and title are given immediately after the link text.  In
*reference links* the destination and title are defined elsewhere in
the document.

A **link text** consists of a sequence of zero or more
inline elements enclosed by square brackets (`[` and `]`).  The
following rules apply:

- Links may not contain other links, at any level of nesting. If
  multiple otherwise valid link definitions appear nested inside each
  other, the inner-most definition is used.

- Brackets are allowed in the *link text* only if (a) they
  are backslash-escaped or (b) they appear as a matched pair of brackets,
  with an open bracket `[`, a sequence of zero or more inlines, and
  a close bracket `]`.

- Backtick *code spans*, *autolinks*, and raw *HTML tags* bind more tightly
  than the brackets in link text.  Thus, for example,
  `` [foo`]` `` could not be a link text, since the second `]`
  is part of a code span.

- The brackets in link text bind more tightly than markers for
  *emphasis and strong emphasis*. Thus, for example, `*[foo*](url)` is a link.

A **link destination** consists of either

- a sequence of zero or more characters between an opening `<` and a
  closing `>` that contains no line breaks or unescaped
  `<` or `>` characters, or

- a nonempty sequence of characters that does not start with `<`,
  does not include *ASCII control characters**ASCII control character*
  or *whitespace***, and includes parentheses only if (a) they are
  backslash-escaped or (b) they are part of a balanced pair of
  unescaped parentheses.
  (Implementations may impose limits on parentheses nesting to
  avoid performance issues, but at least three levels of nesting
  should be supported.)

A **link title**  consists of either

- a sequence of zero or more characters between straight double-quote
  characters (`"`), including a `"` character only if it is
  backslash-escaped, or

- a sequence of zero or more characters between straight single-quote
  characters (`'`), including a `'` character only if it is
  backslash-escaped, or

- a sequence of zero or more characters between matching parentheses
  (`(...)`), including a `(` or `)` character only if it is
  backslash-escaped.

Although *link titles* may span multiple lines, they may not contain
a *blank line*.

An **inline link** consists of a *link text* followed immediately
by a left parenthesis `(`, optional *whitespace*, an optional
*link destination*, an optional *link title* separated from the link
destination by *whitespace*, optional *whitespace*, and a right
parenthesis `)`. The link's text consists of the inlines contained
in the *link text* (excluding the enclosing square brackets).
The link's URI consists of the link destination, excluding enclosing
`<...>` if present, with backslash-escapes in effect as described
above.  The link's title consists of the link title, excluding its
enclosing delimiters, with backslash-escapes in effect as described
above.

Here is a simple inline link:


```
Example:
[link](/uri "title")

```
---
[link](/uri "title")

---


The title may be omitted:


```
Example:
[link](/uri)

```
---
[link](/uri)

---


Both the title and the destination may be omitted:


```
Example:
[link]()

```
---
[link]()

---



```
Example:
[link](<>)

```
---
[link](<>)

---

The destination can only contain spaces if it is
enclosed in pointy brackets:


```
Example:
[link](/my uri)

```
---
[link](/my uri)

---


```
Example:
[link](</my uri>)

```
---
[link](</my uri>)

---

The destination cannot contain line breaks,
even if enclosed in pointy brackets:


```
Example:
[link](foo
bar)

```
---
[link](foo
bar)

---


```
Example:
[link](<foo
bar>)

```
---
[link](<foo
bar>)

---

The destination can contain `)` if it is enclosed
in pointy brackets:


```
Example:
[a](<b)c>)

```
---
[a](<b)c>)

---

Pointy brackets that enclose links must be unescaped:


```
Example:
[link](<foo\>)

```
---
[link](<foo\>)

---

These are not links, because the opening pointy bracket
is not matched properly:


```
Example:
[a](<b)c
[a](<b)c>
[a](<b>c)

```
---
[a](<b)c
[a](<b)c>
[a](<b>c)

---

Parentheses inside the link destination may be escaped:


```
Example:
[link](\(foo\))

```
---
[link](\(foo\))

---

Any number of parentheses are allowed without escaping, as long as they are
balanced:


```
Example:
[link](foo(and(bar)))

```
---
[link](foo(and(bar)))

---

However, if you have unbalanced parentheses, you need to escape or use the
`<...>` form:


```
Example:
[link](foo(and(bar))

```
---
[link](foo(and(bar))

---



```
Example:
[link](foo\(and\(bar\))

```
---
[link](foo\(and\(bar\))

---



```
Example:
[link](<foo(and(bar)>)

```
---
[link](<foo(and(bar)>)

---


Parentheses and other symbols can also be escaped, as usual
in Markdown:


```
Example:
[link](foo\)\:)

```
---
[link](foo\)\:)

---


A link can contain fragment identifiers and queries:


```
Example:
[link](#fragment)

[link](http://example.com#fragment)

[link](http://example.com?foo=3#frag)

```
---
[link](#fragment)

[link](http://example.com#fragment)

[link](http://example.com?foo=3#frag)

---


Note that a backslash before a non-escapable character is
just a backslash:


```
Example:
[link](foo\bar)

```
---
[link](foo\bar)

---


URL-escaping should be left alone inside the destination, as all
URL-escaped characters are also valid URL characters. Entity and
numerical character references in the destination will be parsed
into the corresponding Unicode code points, as usual.  These may
be optionally URL-escaped when written as HTML, but this spec
does not enforce any particular policy for rendering URLs in
HTML or other formats.  Renderers may make different decisions
about how to escape or normalize URLs in the output.


```
Example:
[link](foo%20b&auml;)

```
---
[link](foo%20b&auml;)

---


Note that, because titles can often be parsed as destinations,
if you try to omit the destination and keep the title, you'll
get unexpected results:


```
Example:
[link]("title")

```
---
[link]("title")

---


Titles may be in single quotes, double quotes, or parentheses:


```
Example:
[link](/url "title")
[link](/url 'title')
[link](/url (title))

```
---
[link](/url "title")
[link](/url 'title')
[link](/url (title))

---


Backslash escapes and entity and numeric character references
may be used in titles:


```
Example:
[link](/url "title \"&quot;")

```
---
[link](/url "title \"&quot;")

---


Titles must be separated from the link using a *whitespace*.
Other *Unicode whitespace* like non-breaking space doesn't work.


```
Example:
[link](/url "title")

```
---
[link](/url "title")

---


Nested balanced quotes are not allowed without escaping:


```
Example:
[link](/url "title "and" title")

```
---
[link](/url "title "and" title")

---


But it is easy to work around this by using a different quote type:


```
Example:
[link](/url 'title "and" title')

```
---
[link](/url 'title "and" title')

---


(Note:  `Markdown.pl` did allow double quotes inside a double-quoted
title, and its test suite included a test demonstrating this.
But it is hard to see a good rationale for the extra complexity this
brings, since there are already many ways---backslash escaping,
entity and numeric character references, or using a different
quote type for the enclosing title---to write titles containing
double quotes.  `Markdown.pl`'s handling of titles has a number
of other strange features.  For example, it allows single-quoted
titles in inline links, but not reference links.  And, in
reference links but not inline links, it allows a title to begin
with `"` and end with `)`.  `Markdown.pl` 1.0.1 even allows
titles with no closing quotation mark, though 1.0.2b8 does not.
It seems preferable to adopt a simple, rational rule that works
the same way in inline links and link reference definitions.)

*Whitespace* is allowed around the destination and title:


```
Example:
[link](   /uri
  "title"  )

```
---
[link](   /uri
  "title"  )

---


But it is not allowed between the link text and the
following parenthesis:


```
Example:
*link* (/uri)

```
---
*link* (/uri)

---


The link text may contain balanced brackets, but not unbalanced ones,
unless they are escaped:


```
Example:
[link [foo *bar*]](/uri)

```
---
[link [foo *bar*]](/uri)

---



```
Example:
*link* bar](/uri)

```
---
*link* bar](/uri)

---



```
Example:
[link [bar](/uri)

```
---
[link [bar](/uri)

---



```
Example:
[link \[bar](/uri)

```
---
[link \[bar](/uri)

---


The link text may contain inline content:


```
Example:
[link *foo **bar** `#`*](/uri)

```
---
[link *foo **bar** `#`*](/uri)

---



```
Example:
[![moon](../input/moon.jpg)](/uri)

```
---
[![moon](../input/moon.jpg)](/uri)

---


However, links may not contain other links, at any level of nesting.


```
Example:
[foo [bar](/uri)](/uri)

```
---
[foo [bar](/uri)](/uri)

---



```
Example:
[foo *[bar [baz](/uri)](/uri)*](/uri)

```
---
[foo *[bar [baz](/uri)](/uri)*](/uri)

---



```
Example:
![[[foo](uri1)](uri2)](uri3)

```
---
![[[foo](uri1)](uri2)](uri3)

---


These cases illustrate the precedence of link text grouping over
emphasis grouping:


```
Example:
*[foo*](/uri)

```
---
*[foo*](/uri)

---



```
Example:
[foo *bar](baz*)

```
---
[foo *bar](baz*)

---


Note that brackets that *aren't* part of links do not take
precedence:


```
Example:
*foo [bar* baz]

```
---
*foo [bar* baz]

---


These cases illustrate the precedence of HTML tags, code spans,
and autolinks over link grouping:


```
Example:
[foo <bar attr="](baz)">

```
---
[foo <bar attr="](baz)">

---



```
Example:
[foo`](/uri)`

```
---
[foo`](/uri)`

---



```
Example:
[foo<http://example.com/?search=](uri)>

```
---
[foo<http://example.com/?search=](uri)>

---


There are three kinds of **reference link**s:
[full](#full-reference-link), [collapsed](#collapsed-reference-link),
and [shortcut](#shortcut-reference-link).

A **full reference link**
consists of a *link text* immediately followed by a *link label*
that *matches* a *link reference definition* elsewhere in the document.

A **link label**  begins with a left bracket (`[`) and ends
with the first right bracket (`]`) that is not backslash-escaped.
Between these brackets there must be at least one [non-whitespace character].
Unescaped square bracket characters are not allowed inside the
opening and closing square brackets of *link labels*.  A link
label can have at most 999 characters inside the square
brackets.

One label **matches**
another just in case their normalized forms are equal.  To normalize a
label, strip off the opening and closing brackets,
perform the *Unicode case fold*, strip leading and trailing
*whitespace* and collapse consecutive internal
*whitespace* to a single space.  If there are multiple
matching reference link definitions, the one that comes first in the
document is used.  (It is desirable in such cases to emit a warning.)

The link's URI and title are provided by the matching *link
reference definition*.

Here is a simple example:


```
Example:
*foo**bar*

*bar*: /url "title"

```
---
*foo**bar*

*bar*: /url "title"

---


The rules for the *link text* are the same as with
*inline links*.  Thus:

The link text may contain balanced brackets, but not unbalanced ones,
unless they are escaped:


```
Example:
[link [foo *bar*]]*ref*

*ref*: /uri

```
---
[link [foo *bar*]]*ref*

*ref*: /uri

---



```
Example:
[link \*bar**ref*

*ref*: /uri

```
---
[link \*bar**ref*

*ref*: /uri

---


The link text may contain inline content:


```
Example:
[link *foo **bar** `#`*]*ref*

*ref*: /uri

```
---
[link *foo **bar** `#`*]*ref*

*ref*: /uri

---



```
Example:
[![moon](../input/moon.jpg)]*ref*

*ref*: /uri

```
---
[![moon](../input/moon.jpg)]*ref*

*ref*: /uri

---


However, links may not contain other links, at any level of nesting.


```
Example:
[foo [bar](/uri)]*ref*

*ref*: /uri

```
---
[foo [bar](/uri)]*ref*

*ref*: /uri

---



```
Example:
[foo *bar *baz**ref**]*ref*

*ref*: /uri

```
---
[foo *bar *baz**ref**]*ref*

*ref*: /uri

---


(In the examples above, we have two *shortcut reference links*
instead of one *full reference link*.)

The following cases illustrate the precedence of link text grouping over
emphasis grouping:


```
Example:
*[foo*]*ref*

*ref*: /uri

```
---
*[foo*]*ref*

*ref*: /uri

---



```
Example:
[foo *bar]*ref**

*ref*: /uri

```
---
[foo *bar]*ref**

*ref*: /uri

---


These cases illustrate the precedence of HTML tags, code spans,
and autolinks over link grouping:


```
Example:
[foo <bar attr="]*ref*">

*ref*: /uri

```
---
[foo <bar attr="]*ref*">

*ref*: /uri

---



```
Example:
[foo`]*ref*`

*ref*: /uri

```
---
[foo`]*ref*`

*ref*: /uri

---



```
Example:
[foo<http://example.com/?search=]*ref*>

*ref*: /uri

```
---
[foo<http://example.com/?search=]*ref*>

*ref*: /uri

---


Matching is case-insensitive:


```
Example:
*foo**BaR*

*bar*: /url "title"

```
---
*foo**BaR*

*bar*: /url "title"

---


Unicode case fold is used:


```
Example:
*ẞ*

*SS*: /url

```
---
*ẞ*

*SS*: /url

---


Consecutive internal *whitespace* is treated as one space for
purposes of determining matching:


```
Example:
*Foo
  bar*: /url

*Baz**Foo bar*

```
---
*Foo
  bar*: /url

*Baz**Foo bar*

---


No *whitespace* is allowed between the *link text* and the
*link label*:


```
Example:
*foo* *bar*

*bar*: /url "title"

```
---
*foo* *bar*

*bar*: /url "title"

---



```
Example:
*foo*
*bar*

*bar*: /url "title"

```
---
*foo*
*bar*

*bar*: /url "title"

---


This is a departure from John Gruber's original Markdown syntax
description, which explicitly allows whitespace between the link
text and the link label.  It brings reference links in line with
*inline links*, which (according to both original Markdown and
this spec) cannot have whitespace after the link text.  More
importantly, it prevents inadvertent capture of consecutive
*shortcut reference links*. If whitespace is allowed between the
link text and the link label, then in the following we will have
a single reference link, not two shortcut reference links, as
intended:

``` markdown
*foo*
*bar*

*foo*: /url1
*bar*: /url2
```

(Note that *shortcut reference links* were introduced by Gruber
himself in a beta version of `Markdown.pl`, but never included
in the official syntax description.  Without shortcut reference
links, it is harmless to allow space between the link text and
link label; but once shortcut references are introduced, it is
too dangerous to allow this, as it frequently leads to
unintended results.)

When there are multiple matching *link reference definitions*,
the first is used:


```
Example:
*foo*: /url1

*foo*: /url2

*bar**foo*

```
---
*foo*: /url1

*foo*: /url2

*bar**foo*

---


Note that matching is performed on normalized strings, not parsed
inline content.  So the following does not match, even though the
labels define equivalent inline content:


```
Example:
*bar*[foo\!]

[foo!]: /url

```
---
*bar*[foo\!]

[foo!]: /url

---


*Link labels* cannot contain brackets, unless they are
backslash-escaped:


```
Example:
*foo*[ref**

[ref**: /uri

```
---
*foo*[ref**

[ref**: /uri

---



```
Example:
*foo*[ref*bar*]

[ref*bar*]: /uri

```
---
*foo*[ref*bar*]

[ref*bar*]: /uri

---



```
Example:
[[*foo*]]

[[*foo*]]: /url

```
---
[[*foo*]]

[[*foo*]]: /url

---



```
Example:
*foo*[ref\**

[ref\**: /uri

```
---
*foo*[ref\**

[ref\**: /uri

---


Note that in this example `]` is not backslash-escaped:


```
Example:
[bar\\]: /uri

[bar\\]

```
---
[bar\\]: /uri

[bar\\]

---


A *link label* must contain at least one [non-whitespace character]:


```
Example:
**

**: /uri

```
---
**

**: /uri

---



```
Example:
*
 *

*
 *: /uri

```
---
*
 *

*
 *: /uri

---


A **collapsed reference link**
consists of a *link label* that *matches* a
*link reference definition* elsewhere in the
document, followed by the string `**`.
The contents of the first link label are parsed as inlines,
which are used as the link's text.  The link's URI and title are
provided by the matching reference link definition.  Thus,
`*foo***` is equivalent to `*foo**foo*`.


```
Example:
*foo***

*foo*: /url "title"

```
---
*foo***

*foo*: /url "title"

---



```
Example:
[*foo* bar]**

[*foo* bar]: /url "title"

```
---
[*foo* bar]**

[*foo* bar]: /url "title"

---


The link labels are case-insensitive:


```
Example:
*Foo***

*foo*: /url "title"

```
---
*Foo***

*foo*: /url "title"

---



As with full reference links, *whitespace* is not
allowed between the two sets of brackets:


```
Example:
*foo* 
**

*foo*: /url "title"

```
---
*foo* 
**

*foo*: /url "title"

---


A **shortcut reference link**
consists of a *link label* that *matches* a
*link reference definition* elsewhere in the
document and is not followed by `**` or a link label.
The contents of the first link label are parsed as inlines,
which are used as the link's text.  The link's URI and title
are provided by the matching link reference definition.
Thus, `*foo*` is equivalent to `*foo***`.


```
Example:
*foo*

*foo*: /url "title"

```
---
*foo*

*foo*: /url "title"

---



```
Example:
[*foo* bar]

[*foo* bar]: /url "title"

```
---
[*foo* bar]

[*foo* bar]: /url "title"

---



```
Example:
[[*foo* bar]]

[*foo* bar]: /url "title"

```
---
[[*foo* bar]]

[*foo* bar]: /url "title"

---



```
Example:
[[bar *foo*

*foo*: /url

```
---
[[bar *foo*

*foo*: /url

---


The link labels are case-insensitive:


```
Example:
*Foo*

*foo*: /url "title"

```
---
*Foo*

*foo*: /url "title"

---


A space after the link text should be preserved:


```
Example:
*foo* bar

*foo*: /url

```
---
*foo* bar

*foo*: /url

---


If you just want bracketed text, you can backslash-escape the
opening bracket to avoid links:


```
Example:
\*foo*

*foo*: /url "title"

```
---
\*foo*

*foo*: /url "title"

---


Note that this is a link, because a link label ends with the first
following closing bracket:


```
Example:
[foo*]: /url

*[foo*]

```
---
[foo*]: /url

*[foo*]

---


Full and compact references take precedence over shortcut
references:


```
Example:
*foo**bar*

*foo*: /url1
*bar*: /url2

```
---
*foo**bar*

*foo*: /url1
*bar*: /url2

---


```
Example:
*foo***

*foo*: /url1

```
---
*foo***

*foo*: /url1

---

Inline links also take precedence:


```
Example:
[foo]()

*foo*: /url1

```
---
[foo]()

*foo*: /url1

---


```
Example:
[foo](not a link)

*foo*: /url1

```
---
[foo](not a link)

*foo*: /url1

---

In the following case `*bar**baz*` is parsed as a reference,
`*foo*` as normal text:


```
Example:
*foo**bar**baz*

*baz*: /url

```
---
*foo**bar**baz*

*baz*: /url

---


Here, though, `*foo**bar*` is parsed as a reference, since
`*bar*` is defined:


```
Example:
*foo**bar**baz*

*baz*: /url1
*bar*: /url2

```
---
*foo**bar**baz*

*baz*: /url1
*bar*: /url2

---


Here `*foo*` is not parsed as a shortcut reference, because it
is followed by a link label (even though `*bar*` is not defined):


```
Example:
*foo**bar**baz*

*baz*: /url1
*foo*: /url2

```
---
*foo**bar**baz*

*baz*: /url1
*foo*: /url2

---



## Images

Syntax for images is like the syntax for links, with one
difference. Instead of *link text*, we have an
**image description**.  The rules for this are the
same as for *link text*, except that (a) an
image description starts with `![` rather than `[`, and
(b) an image description may contain links.
An image description has inline elements
as its contents.  When an image is rendered to HTML,
this is standardly used as the image's `alt` attribute.


```
Example:
![foo](/url "title")

```
---
![foo](/url "title")

---



```
Example:
![foo *bar*]

[foo *bar*]: train.jpg "train & tracks"

```
---
![foo *bar*]

[foo *bar*]: train.jpg "train & tracks"

---



```
Example:
![foo ![bar](/url)](/url2)

```
---
![foo ![bar](/url)](/url2)

---



```
Example:
![foo [bar](/url)](/url2)

```
---
![foo [bar](/url)](/url2)

---


Though this spec is concerned with parsing, not rendering, it is
recommended that in rendering to HTML, only the plain string content
of the *image description* be used.  Note that in
the above example, the alt attribute's value is `foo bar`, not `foo
[bar](/url)` or `foo <a href="/url">bar</a>`.  Only the plain string
content is rendered, without formatting.


```
Example:
![foo *bar*]**

[foo *bar*]: train.jpg "train & tracks"

```
---
![foo *bar*]**

[foo *bar*]: train.jpg "train & tracks"

---



```
Example:
![foo *bar*]*foobar*

*FOOBAR*: train.jpg "train & tracks"

```
---
![foo *bar*]*foobar*

*FOOBAR*: train.jpg "train & tracks"

---



```
Example:
![foo](train.jpg)

```
---
![foo](train.jpg)

---



```
Example:
My ![foo bar](/path/to/train.jpg  "title"   )

```
---
My ![foo bar](/path/to/train.jpg  "title"   )

---



```
Example:
![foo](<url>)

```
---
![foo](<url>)

---



```
Example:
![](/url)

```
---
![](/url)

---


Reference-style:


```
Example:
!*foo**bar*

*bar*: /url

```
---
!*foo**bar*

*bar*: /url

---



```
Example:
!*foo**bar*

*BAR*: /url

```
---
!*foo**bar*

*BAR*: /url

---


Collapsed:


```
Example:
!*foo***

*foo*: /url "title"

```
---
!*foo***

*foo*: /url "title"

---



```
Example:
![*foo* bar]**

[*foo* bar]: /url "title"

```
---
![*foo* bar]**

[*foo* bar]: /url "title"

---


The labels are case-insensitive:


```
Example:
!*Foo***

*foo*: /url "title"

```
---
!*Foo***

*foo*: /url "title"

---


As with reference links, *whitespace* is not allowed
between the two sets of brackets:


```
Example:
!*foo* 
**

*foo*: /url "title"

```
---
!*foo* 
**

*foo*: /url "title"

---


Shortcut:


```
Example:
!*foo*

*foo*: /url "title"

```
---
!*foo*

*foo*: /url "title"

---



```
Example:
![*foo* bar]

[*foo* bar]: /url "title"

```
---
![*foo* bar]

[*foo* bar]: /url "title"

---


Note that link labels cannot contain unescaped brackets:


```
Example:
![*foo*]

[*foo*]: /url "title"

```
---
![*foo*]

[*foo*]: /url "title"

---


The link labels are case-insensitive:


```
Example:
!*Foo*

*foo*: /url "title"

```
---
!*Foo*

*foo*: /url "title"

---


If you just want a literal `!` followed by bracketed text, you can
backslash-escape the opening `[`:


```
Example:
!\*foo*

*foo*: /url "title"

```
---
!\*foo*

*foo*: /url "title"

---


If you want a link after a literal `!`, backslash-escape the
`!`:


```
Example:
\!*foo*

*foo*: /url "title"

```
---
\!*foo*

*foo*: /url "title"

---


## Autolinks

**Autolink**s are absolute URIs and email addresses inside
`<` and `>`. They are parsed as links, with the URL or email address
as the link label.

A **URI autolink** consists of `<`, followed by an
*absolute URI* followed by `>`.  It is parsed as
a link to the URI, with the URI as the link's label.

An **absolute URI**,
for these purposes, consists of a *scheme* followed by a colon (`:`)
followed by zero or more characters other *ASCII control
characters**ASCII control character* or *whitespace*** , `<`, and `>`.
If the URI includes these characters, they must be percent-encoded
(e.g. `%20` for a space).

For purposes of this spec, a **scheme** is any sequence
of 2--32 characters beginning with an ASCII letter and followed
by any combination of ASCII letters, digits, or the symbols plus
("+"), period ("."), or hyphen ("-").

Here are some valid autolinks:


```
Example:
<http://foo.bar.baz>

```
---
<http://foo.bar.baz>

---



```
Example:
<http://foo.bar.baz/test?q=hello&id=22&boolean>

```
---
<http://foo.bar.baz/test?q=hello&id=22&boolean>

---



```
Example:
<irc://foo.bar:2233/baz>

```
---
<irc://foo.bar:2233/baz>

---


Uppercase is also fine:


```
Example:
<MAILTO:FOO@BAR.BAZ>

```
---
<MAILTO:FOO@BAR.BAZ>

---


Note that many strings that count as *absolute URIs* for
purposes of this spec are not valid URIs, because their
schemes are not registered or because of other problems
with their syntax:


```
Example:
<a+b+c:d>

```
---
<a+b+c:d>

---



```
Example:
<made-up-scheme://foo,bar>

```
---
<made-up-scheme://foo,bar>

---



```
Example:
<http://../>

```
---
<http://../>

---



```
Example:
<localhost:5001/foo>

```
---
<localhost:5001/foo>

---


Spaces are not allowed in autolinks:


```
Example:
<http://foo.bar/baz bim>

```
---
<http://foo.bar/baz bim>

---


Backslash-escapes do not work inside autolinks:


```
Example:
<http://example.com/\[\>

```
---
<http://example.com/\[\>

---


An **email autolink**
consists of `<`, followed by an *email address*,
followed by `>`.  The link's label is the email address,
and the URL is `mailto:` followed by the email address.

An **email address**,
for these purposes, is anything that matches
the [non-normative regex from the HTML5
spec](https://html.spec.whatwg.org/multipage/forms.html#e-mail-state-(type=email)):

    /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?
    (?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/

Examples of email autolinks:


```
Example:
<foo@bar.example.com>

```
---
<foo@bar.example.com>

---



```
Example:
<foo+special@Bar.baz-bar0.com>

```
---
<foo+special@Bar.baz-bar0.com>

---


Backslash-escapes do not work inside email autolinks:


```
Example:
<foo\+@bar.example.com>

```
---
<foo\+@bar.example.com>

---


These are not autolinks:


```
Example:
<>

```
---
<>

---



```
Example:
< http://foo.bar >

```
---
< http://foo.bar >

---



```
Example:
<m:abc>

```
---
<m:abc>

---



```
Example:
<foo.bar.baz>

```
---
<foo.bar.baz>

---



```
Example:
http://example.com

```
---
http://example.com

---



```
Example:
foo@bar.example.com

```
---
foo@bar.example.com

---


## Raw HTML

Text between `<` and `>` that looks like an HTML tag is parsed as a
raw HTML tag and will be rendered in HTML without escaping.
Tag and attribute names are not limited to current HTML tags,
so custom tags (and even, say, DocBook tags) may be used.

Here is the grammar for tags:

A **tag name** consists of an ASCII letter
followed by zero or more ASCII letters, digits, or
hyphens (`-`).

An **attribute** consists of *whitespace*,
an *attribute name*, and an optional
*attribute value specification*.

An **attribute name**
consists of an ASCII letter, `_`, or `:`, followed by zero or more ASCII
letters, digits, `_`, `.`, `:`, or `-`.  (Note:  This is the XML
specification restricted to ASCII.  HTML5 is laxer.)

An **attribute value specification**
consists of optional *whitespace*,
a `=` character, optional *whitespace*, and an *attribute
value*.

An **attribute value**
consists of an *unquoted attribute value*,
a [single-quoted attribute value], or a [double-quoted attribute value].

An **unquoted attribute value**
is a nonempty string of characters not
including *whitespace*, `"`, `'`, `=`, `<`, `>`, or `` ` ``.

A [single-quoted attribute value](@)
consists of `'`, zero or more
characters not including `'`, and a final `'`.

A [double-quoted attribute value](@)
consists of `"`, zero or more
characters not including `"`, and a final `"`.

An **open tag** consists of a `<` character, a *tag name*,
zero or more *attributes*, optional *whitespace*, an optional `/`
character, and a `>` character.

A **closing tag** consists of the string `</`, a
*tag name*, optional *whitespace*, and the character `>`.

An **HTML comment** consists of `<!--` + *text* + `-->`,
where *text* does not start with `>` or `->`, does not end with `-`,
and does not contain `--`.  (See the
[HTML5 spec](http://www.w3.org/TR/html5/syntax.html#comments).)

A **processing instruction**
consists of the string `<?`, a string
of characters not including the string `?>`, and the string
`?>`.

A **declaration** consists of the string `<!`, an ASCII letter, zero or more
characters not including the character `>`, and the character `>`.

A **CDATA section** consists of
the string `<![CDATA[`, a string of characters not including the string
`]]>`, and the string `]]>`.

An **HTML tag** consists of an *open tag*, a *closing tag*,
an *HTML comment*, a *processing instruction*, a *declaration*,
or a *CDATA section*.

Here are some simple open tags:


```
Example:
<a><bab><c2c>

```
---
<a><bab><c2c>

---


Empty elements:


```
Example:
<a/><b2/>

```
---
<a/><b2/>

---


*Whitespace* is allowed:


```
Example:
<a  /><b2
data="foo" >

```
---
<a  /><b2
data="foo" >

---


With attributes:


```
Example:
<a foo="bar" bam = 'baz <em>"</em>'
_boolean zoop:33=zoop:33 />

```
---
<a foo="bar" bam = 'baz <em>"</em>'
_boolean zoop:33=zoop:33 />

---


Custom tag names can be used:


```
Example:
Foo <responsive-image src="foo.jpg" />

```
---
Foo <responsive-image src="foo.jpg" />

---


Illegal tag names, not parsed as HTML:


```
Example:
<33> <__>

```
---
<33> <__>

---


Illegal attribute names:


```
Example:
<a h*#ref="hi">

```
---
<a h*#ref="hi">

---


Illegal attribute values:


```
Example:
<a href="hi'> <a href=hi'>

```
---
<a href="hi'> <a href=hi'>

---


Illegal *whitespace*:


```
Example:
< a><
foo><bar/ >
<foo bar=baz
bim!bop />

```
---
< a><
foo><bar/ >
<foo bar=baz
bim!bop />

---


Missing *whitespace*:


```
Example:
<a href='bar'title=title>

```
---
<a href='bar'title=title>

---


Closing tags:


```
Example:
</a></foo >

```
---
</a></foo >

---


Illegal attributes in closing tag:


```
Example:
</a href="foo">

```
---
</a href="foo">

---


Comments:


```
Example:
foo <!-- this is a
comment - with hyphen -->

```
---
foo <!-- this is a
comment - with hyphen -->

---



```
Example:
foo <!-- not a comment -- two hyphens -->

```
---
foo <!-- not a comment -- two hyphens -->

---


Not comments:


```
Example:
foo <!--> foo -->

foo <!-- foo--->

```
---
foo <!--> foo -->

foo <!-- foo--->

---


Processing instructions:


```
Example:
foo <?php echo $a; ?>

```
---
foo <?php echo $a; ?>

---


Declarations:


```
Example:
foo <!ELEMENT br EMPTY>

```
---
foo <!ELEMENT br EMPTY>

---


CDATA sections:


```
Example:
foo <![CDATA[>&<]]>

```
---
foo <![CDATA[>&<]]>

---


Entity and numeric character references are preserved in HTML
attributes:


```
Example:
foo <a href="&ouml;">

```
---
foo <a href="&ouml;">

---


Backslash escapes do not work in HTML attributes:


```
Example:
foo <a href="\*">

```
---
foo <a href="\*">

---



```
Example:
<a href="\"">

```
---
<a href="\"">

---


## Hard line breaks

A line break (not in a code span or HTML tag) that is preceded
by two or more spaces and does not occur at the end of a block
is parsed as a **hard line break** (rendered
in HTML as a `<br />` tag):


```
Example:
foo  
baz

```
---
foo  
baz

---


For a more visible alternative, a backslash before the
*line ending* may be used instead of two spaces:


```
Example:
foo\
baz

```
---
foo\
baz

---


More than two spaces can be used:


```
Example:
foo       
baz

```
---
foo       
baz

---


Leading spaces at the beginning of the next line are ignored:


```
Example:
foo  
     bar

```
---
foo  
     bar

---



```
Example:
foo\
     bar

```
---
foo\
     bar

---


Line breaks can occur inside emphasis, links, and other constructs
that allow inline content:


```
Example:
*foo  
bar*

```
---
*foo  
bar*

---



```
Example:
*foo\
bar*

```
---
*foo\
bar*

---


Line breaks do not occur inside code spans


```
Example:
`code 
span`

```
---
`code 
span`

---



```
Example:
`code\
span`

```
---
`code\
span`

---


or HTML tags:


```
Example:
<a href="foo  
bar">

```
---
<a href="foo  
bar">

---



```
Example:
<a href="foo\
bar">

```
---
<a href="foo\
bar">

---


Hard line breaks are for separating inline content within a block.
Neither syntax for hard line breaks works at the end of a paragraph or
other block element:


```
Example:
foo\

```
---
foo\

---



```
Example:
foo  

```
---
foo  

---



```
Example:
### foo\

```
---
### foo\

---



```
Example:
### foo  

```
---
### foo  

---


## Soft line breaks

A regular line break (not in a code span or HTML tag) that is not
preceded by two or more spaces or a backslash is parsed as a
**softbreak**.  (A softbreak may be rendered in HTML either as a
*line ending* or as a space. The result will be the same in
browsers. In the examples here, a *line ending* will be used.)


```
Example:
foo
baz

```
---
foo
baz

---


Spaces at the end of the line and beginning of the next line are
removed:


```
Example:
foo 
 baz

```
---
foo 
 baz

---


A conforming parser may render a soft line break in HTML either as a
line break or as a space.

A renderer may also provide an option to render soft line breaks
as hard line breaks.

## Textual content

Any characters not given an interpretation by the above rules will
be parsed as plain textual content.


```
Example:
hello $.;'there

```
---
hello $.;'there

---



```
Example:
Foo χρῆν

```
---
Foo χρῆν

---


Internal spaces are preserved verbatim:


```
Example:
Multiple     spaces

```
---
Multiple     spaces

---


<!-- END TESTS -->

# Appendix: A parsing strategy

In this appendix we describe some features of the parsing strategy
used in the CommonMark reference implementations.

## Overview

Parsing has two phases:

1. In the first phase, lines of input are consumed and the block
structure of the document---its division into paragraphs, block quotes,
list items, and so on---is constructed.  Text is assigned to these
blocks but not parsed. Link reference definitions are parsed and a
map of links is constructed.

2. In the second phase, the raw text contents of paragraphs and headings
are parsed into sequences of Markdown inline elements (strings,
code spans, links, emphasis, and so on), using the map of link
references constructed in phase 1.

At each point in processing, the document is represented as a tree of
**blocks**.  The root of the tree is a `document` block.  The `document`
may have any number of other blocks as **children**.  These children
may, in turn, have other blocks as children.  The last child of a block
is normally considered **open**, meaning that subsequent lines of input
can alter its contents.  (Blocks that are not open are **closed**.)
Here, for example, is a possible document tree, with the open blocks
marked by arrows:

``` tree
-> document
  -> block_quote
       paragraph
         "Lorem ipsum dolor\nsit amet."
    -> list (type=bullet tight=true bullet_char=-)
         list_item
           paragraph
             "Qui *quodsi iracundia*"
      -> list_item
        -> paragraph
             "aliquando id"
```

## Phase 1: block structure

Each line that is processed has an effect on this tree.  The line is
analyzed and, depending on its contents, the document may be altered
in one or more of the following ways:

1. One or more open blocks may be closed.
2. One or more new blocks may be created as children of the
   last open block.
3. Text may be added to the last (deepest) open block remaining
   on the tree.

Once a line has been incorporated into the tree in this way,
it can be discarded, so input can be read in a stream.

For each line, we follow this procedure:

1. First we iterate through the open blocks, starting with the
root document, and descending through last children down to the last
open block.  Each block imposes a condition that the line must satisfy
if the block is to remain open.  For example, a block quote requires a
`>` character.  A paragraph requires a non-blank line.
In this phase we may match all or just some of the open
blocks.  But we cannot close unmatched blocks yet, because we may have a
*lazy continuation line*.

2.  Next, after consuming the continuation markers for existing
blocks, we look for new block starts (e.g. `>` for a block quote).
If we encounter a new block start, we close any blocks unmatched
in step 1 before creating the new block as a child of the last
matched container block.

3.  Finally, we look at the remainder of the line (after block
markers like `>`, list markers, and indentation have been consumed).
This is text that can be incorporated into the last open
block (a paragraph, code block, heading, or raw HTML).

Setext headings are formed when we see a line of a paragraph
that is a *setext heading underline*.

Reference link definitions are detected when a paragraph is closed;
the accumulated text lines are parsed to see if they begin with
one or more reference link definitions.  Any remainder becomes a
normal paragraph.

We can see how this works by considering how the tree above is
generated by four lines of Markdown:

``` markdown
> Lorem ipsum dolor
sit amet.
> - Qui *quodsi iracundia*
> - aliquando id
```

At the outset, our document model is just

``` tree
-> document
```

The first line of our text,

``` markdown
> Lorem ipsum dolor
```

causes a `block_quote` block to be created as a child of our
open `document` block, and a `paragraph` block as a child of
the `block_quote`.  Then the text is added to the last open
block, the `paragraph`:

``` tree
-> document
  -> block_quote
    -> paragraph
         "Lorem ipsum dolor"
```

The next line,

``` markdown
sit amet.
```

is a "lazy continuation" of the open `paragraph`, so it gets added
to the paragraph's text:

``` tree
-> document
  -> block_quote
    -> paragraph
         "Lorem ipsum dolor\nsit amet."
```

The third line,

``` markdown
> - Qui *quodsi iracundia*
```

causes the `paragraph` block to be closed, and a new `list` block
opened as a child of the `block_quote`.  A `list_item` is also
added as a child of the `list`, and a `paragraph` as a child of
the `list_item`.  The text is then added to the new `paragraph`:

``` tree
-> document
  -> block_quote
       paragraph
         "Lorem ipsum dolor\nsit amet."
    -> list (type=bullet tight=true bullet_char=-)
      -> list_item
        -> paragraph
             "Qui *quodsi iracundia*"
```

The fourth line,

``` markdown
> - aliquando id
```

causes the `list_item` (and its child the `paragraph`) to be closed,
and a new `list_item` opened up as child of the `list`.  A `paragraph`
is added as a child of the new `list_item`, to contain the text.
We thus obtain the final tree:

``` tree
-> document
  -> block_quote
       paragraph
         "Lorem ipsum dolor\nsit amet."
    -> list (type=bullet tight=true bullet_char=-)
         list_item
           paragraph
             "Qui *quodsi iracundia*"
      -> list_item
        -> paragraph
             "aliquando id"
```

## Phase 2: inline structure

Once all of the input has been parsed, all open blocks are closed.

We then "walk the tree," visiting every node, and parse raw
string contents of paragraphs and headings as inlines.  At this
point we have seen all the link reference definitions, so we can
resolve reference links as we go.

``` tree
document
  block_quote
    paragraph
      str "Lorem ipsum dolor"
      softbreak
      str "sit amet."
    list (type=bullet tight=true bullet_char=-)
      list_item
        paragraph
          str "Qui "
          emph
            str "quodsi iracundia"
      list_item
        paragraph
          str "aliquando id"
```

Notice how the *line ending* in the first paragraph has
been parsed as a `softbreak`, and the asterisks in the first list item
have become an `emph`.

### An algorithm for parsing nested emphasis and links

By far the trickiest part of inline parsing is handling emphasis,
strong emphasis, links, and images.  This is done using the following
algorithm.

When we're parsing inlines and we hit either

- a run of `*` or `_` characters, or
- a `[` or `![`

we insert a text node with these symbols as its literal content, and we
add a pointer to this text node to the **delimiter stack**.

The *delimiter stack* is a doubly linked list.  Each
element contains a pointer to a text node, plus information about

- the type of delimiter (`[`, `![`, `*`, `_`)
- the number of delimiters,
- whether the delimiter is "active" (all are active to start), and
- whether the delimiter is a potential opener, a potential closer,
  or both (which depends on what sort of characters precede
  and follow the delimiters).

When we hit a `]` character, we call the *look for link or image*
procedure (see below).

When we hit the end of the input, we call the *process emphasis*
procedure (see below), with `stack_bottom` = NULL.

#### *look for link or image*

Starting at the top of the delimiter stack, we look backwards
through the stack for an opening `[` or `![` delimiter.

- If we don't find one, we return a literal text node `]`.

- If we do find one, but it's not *active*, we remove the inactive
  delimiter from the stack, and return a literal text node `]`.

- If we find one and it's active, then we parse ahead to see if
  we have an inline link/image, reference link/image, compact reference
  link/image, or shortcut reference link/image.

  + If we don't, then we remove the opening delimiter from the
    delimiter stack and return a literal text node `]`.

  + If we do, then

    * We return a link or image node whose children are the inlines
      after the text node pointed to by the opening delimiter.

    * We run *process emphasis* on these inlines, with the `[` opener
      as `stack_bottom`.

    * We remove the opening delimiter.

    * If we have a link (and not an image), we also set all
      `[` delimiters before the opening delimiter to *inactive*.  (This
      will prevent us from getting links within links.)

#### *process emphasis*

Parameter `stack_bottom` sets a lower bound to how far we
descend in the *delimiter stack*.  If it is NULL, we can
go all the way to the bottom.  Otherwise, we stop before
visiting `stack_bottom`.

Let `current_position` point to the element on the *delimiter stack*
just above `stack_bottom` (or the first element if `stack_bottom`
is NULL).

We keep track of the `openers_bottom` for each delimiter
type (`*`, `_`) and each length of the closing delimiter run
(modulo 3).  Initialize this to `stack_bottom`.

Then we repeat the following until we run out of potential
closers:

- Move `current_position` forward in the delimiter stack (if needed)
  until we find the first potential closer with delimiter `*` or `_`.
  (This will be the potential closer closest
  to the beginning of the input -- the first one in parse order.)

- Now, look back in the stack (staying above `stack_bottom` and
  the `openers_bottom` for this delimiter type) for the
  first matching potential opener ("matching" means same delimiter).

- If one is found:

  + Figure out whether we have emphasis or strong emphasis:
    if both closer and opener spans have length >= 2, we have
    strong, otherwise regular.

  + Insert an emph or strong emph node accordingly, after
    the text node corresponding to the opener.

  + Remove any delimiters between the opener and closer from
    the delimiter stack.

  + Remove 1 (for regular emph) or 2 (for strong emph) delimiters
    from the opening and closing text nodes.  If they become empty
    as a result, remove them and remove the corresponding element
    of the delimiter stack.  If the closing node is removed, reset
    `current_position` to the next element in the stack.

- If none is found:

  + Set `openers_bottom` to the element before `current_position`.
    (We know that there are no openers for this kind of closer up to and
    including this point, so this puts a lower bound on future searches.)

  + If the closer at `current_position` is not a potential opener,
    remove it from the delimiter stack (since we know it can't
    be a closer either).

  + Advance `current_position` to the next element in the stack.

After we're done, we remove all delimiters above `stack_bottom` from the
delimiter stack.
