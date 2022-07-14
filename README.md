# deeptour_lib

Code for a project for the [DevRev hackathon](https://devrevhack0.devpost.com/).

Given a source repository path, it can extract functions and run different models on them like code summarization.
Can work on Python, Javascript, and Java code.

It then saves the output in the form of a [CodeTour](https://github.com/microsoft/codetour) to generate custom AI-made tours for any project.

To run it you need to install requirements.txt and then python3 deeptour.py /project/path/here

On the first run it can take some time because it will be downloading the models to use when generating the tours.

Be prepared to do some, possibly a lot of firefighting to get this working on your machine.
