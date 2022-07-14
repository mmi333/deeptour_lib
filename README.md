# deeptour_lib

Code for a project for the [DevRev hackathon](https://devpost.com/software/deeptour).

Given a source repository path, it can extract functions and runs different models on them like code summarization, code refinement, etc.
Can work on Python, Javascript, and Java code.

It then saves the output in the form of a [CodeTour](https://github.com/microsoft/codetour) to generate custom AI-made tours for any project.

To run it you need to install requirements.txt and then python3 deeptour.py /project/path/here

On the first run it can take some time because it will be downloading the models to use when generating the tours.

Be prepared to do some, possibly a lot of firefighting to get this working on your machine.

## Inspiration

I was looking for a project idea when I stumbled across [codetour](https://github.com/microsoft/codetour) and once I had the idea for this project I had to do it.

## What it does

It basically auto-generates files that work with the codetour extension for code summarization, refinement, translation and any other use case you can come up with!

It allows you to create your own custom tours using your own models, like only using the code refinement model if the defect detection model found a defect. Or maybe you could train a model that links an issue to a line of code and generates a tour for that. The sky's the limit!

 
## How it was built

All the AI models are from HuggingFace. This isn't a requirement but it's much easier than the painful endeavour of trying to make research code work as a simple api  (thanks HuggingFace!) 

There are parsers that get the Abstract Syntax Trees for each file to extract the function bodies and then unparse the AST back into strings. Each different language uses different libraries like ast for python, esprima for javascript, and javalang for java. 

GitPython to get the git blame output for function declarations to get an estimate of when the function was first created.

Some Node.js boilerplate for the extension ¯\_(ツ)_/¯ 


## Challenges I ran into

Oh where to start, where to start:

- While HuggingFace saved me, there doesn't exist nearly enough models fine-tuned on code. Most work on Java only. And a whole lot of models don't have model cards so I either didn't use them or kept scratching my head till I got them working.

- Extracting functions from files is hard. Whether it's ast, esprima, or java. And unparsing Abstract Syntax Trees into strings is even harder. (I mean, yes, I'm calling APIs that do that for me, but even getting those APIs to work is hard.)

- Generating git blame outputs was first done by calling a bash script that does that with the git cli. Then I realized that was stupid and directly used GitPython for a slightly less stupid approach

- Getting the whole thing to work as a VSCode extension (even if it's a wrapper) wasn't easy. Had to figure out how to make node start a python program and act cool throughout. 

## What I learned

1- GitPython
2- A bit more about using HuggingFace models
3- ASTs are awesome
4- ASTs are hard
5- Deep Learning for software engineering still has many gaps to be filled both in research and industry, but maybe more so in industry

