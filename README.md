# Welcome to the Large Language Model Testing System(v0.2)!

**2025.03.06**

The Large Language Model Testing System is a system based on artificial intelligence technology, designed to evaluate and test the capabilities of large language models. This system simulates environments for essay and multiple-choice questions to ensure that the models perform as expected in specialized fields. This is version 0.2 of the system.

## Instructions for Use

First, you need to open the `.env` environment file and fill in your large model API key. Additionally, in the `config.txt` file, you should fill in characters that correspond to those before the “_” symbol in `.env`, so that the program can be called correctly.

This project uses the Flask framework. You can start the web page by running the `1.py` file. The libraries required for the project are listed in `requirements.txt`, and the Python version is not particularly important.

The system supports uploading Excel files to automate answering questions and generating answers. You can also call the large language model again to evaluate the quality of the answers provided by the model.

The system supports two types of tests: essay questions and multiple-choice questions. Templates for test files can be found at the bottom of the web page. Please fill in the content strictly according to the template to avoid unexpected errors. Thank you!

The system distinguishes files and their results by filename. "_t" indicates that the file is an essay question result, "_c" indicates a multiple-choice question result, "_r" indicates an evaluation result, and "_a" indicates an answer result. The files you upload will be saved in the "Upload Files" section (Note! It is recommended that you rename your files to avoid containing these characters).
# 欢迎来到大语言模型测试系统(v0.2)！

**2025.03.06**

大语言模型测试系统‌是一种基于人工智能技术的系统，主要用于评估和测试大语言模型的能力。该系统模拟文字题和选择题环境确保其在专业领域的表现符合预期。这是系统的v0.2版本。
  
## 使用须知

首先，您需要打开.env环境填写您的大模型api，并且在config.txt的每行中填写与.env“_”符号前相同的字符，以便程序调用。

本项目使用Flask框架，您可以通过运行1.py文件启用网页。项目所需的库在requirements.txt中，python版本并不十分重要。

该系统支持上传Excel格式的文件，对您的问题自动化作答，生成答案。同时，您可以再次调用大语言模型，对作答模型回答的质量进行评判。

该系统支持选择题和文字题两种形式的测试，测试文件的模板在网页页面下方可见。请您严格按照模板填写内容，避免出现不可预料的错误，谢谢！

该系统以文件名区分文件与文件结果，"_t"表示该文件为文字题结果，"_c"表示该文件为选择题结果，"_r"表示该文件为评测结果，"_a"表示该文件为回答结果。您上传的文件将保存在“上传文件”中(注意！推荐您修改文件名使它们不含这些字符)。
