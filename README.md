# :fireworks: ig

<p align="center">
  <img src="extra/graph.gif">
  <br><br>
  `ig` is a tool to visualize include graphs of C++ projects.
  <br><br>
  <img alt="license" src="https://img.shields.io/github/license/mashape/apistatus.svg"/>
</p>

## Overview

Point `ig` at any directory containing C++ source or header files and it will
construct a full graph of all includes, serve you a local website and visualize
the graph interactively with [sigma.js](http://sigmajs.org), for you to admire.

Usage is very easy:

```sh
$ ig -o include
```

will inspect the folder `include`, serve a website on `localhost:8080` and even
open your browser for you. The full set of options currently include:

```sh

```

But does it scale? It scales quite well. The graph you see above is the include
graph for the entire LLVM and clang codebase, which spans more than 5,000 files
and 1.5M LOC. The graph visualization may be a bit sluggish and slightly rape
your GPU, but it still works.

## Installation

Get it with pip:

```sh
$ pip install ig
```

## Authors

[Peter Goldsborough](http://goldsborough.me) + [cat](https://goo.gl/IpUmJn)
:heart:
