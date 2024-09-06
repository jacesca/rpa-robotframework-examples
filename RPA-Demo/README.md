# Template: Python - RPA Demo - 
The process is used once a week to manually insert sales performance data for 
all Sales Representatives into the intranet, and to generate a PDF report. 
The company sets weekly sales goals for each sales representative. 
At the end of the week, their results are exported from an existing system 
(not included in this process) into an Excel spreadsheet. 

Currently, the intranet administrator manually executes these operations: 

1. Each week a Microsoft Excel spreadsheet is exported and uploaded to the intranet webserver. 
2. The employee downloads the exported spreadsheet from the intranet webserver. 
3. The employee manually logs into the intranet website. 
4. The employee inserts the information for each sales representative. 
5. Data is collected in a table on the site, which also adds up the sales goal and the actual sales for the week. 
6. The employee selects the table in the browser, pastes the code into Microsoft Word, and prints the resulting document as a PDF. 


## Running

#### VS Code
1. Get [Robocorp Code](https://robocorp.com/docs/developer-tools/visual-studio-code/extension-features) -extension for VS Code.
1. You'll get an easy-to-use side panel and powerful command-palette commands for running, debugging, code completion, docs, etc.

#### Command line

1. [Get RCC](https://github.com/robocorp/rcc?tab=readme-ov-file#getting-started)
1. Use the command: `rcc run`

## Results

🚀 After running the bot, check out the `log.html` under the `output` -folder.

## Dependencies

We strongly recommend getting familiar with adding your dependencies in [conda.yaml](conda.yaml) to control your Python dependencies and the whole Python environment for your automation.

<details>
  <summary>🙋‍♂️ "Why not just pip install...?"</summary>

Think of [conda.yaml](conda.yaml) as an equivalent of the requirements.txt, but much better. 👩‍💻 With `conda.yaml`, you are not just controlling your PyPI dependencies; you control the complete Python environment, which makes things repeatable and easy.

👉 You will probably need to run your code on another machine quite soon, so by using `conda.yaml`:
- You can avoid `Works on my machine` -cases
- You do not need to manage Python installations on all the machines
- You can control exactly which version of Python your automation will run on 
  - You'll also control the pip version to avoid dep. resolution changes
- No need for venv, pyenv, ... tooling and knowledge sharing inside your team.
- Define dependencies in conda.yaml, let our tooling do the heavy lifting.
- You get all the content of [conda-forge](https://prefix.dev/channels/conda-forge) without any extra tooling

> Dive deeper with [these](https://github.com/robocorp/rcc/blob/master/docs/recipes.md#what-is-in-condayaml) resources.

</details>
<br/>

> The full power of [rpaframework](https://robocorp.com/docs/python/rpa-framework) -libraries is also available on Python as a backup while we implement the new Python libraries.

## What now?

🚀 Now, go get'em

Start writing Python and remember that the AI/LLM's out there are getting really good and creating Python code specifically.

👉 Try out [Robocorp ReMark 💬](https://chat.robocorp.com)

For more information, do not forget to check out the following:
- [Robocorp Documentation -site](https://robocorp.com/docs)
- [Portal for more examples](https://robocorp.com/portal)
- Follow our main [robocorp -repository](https://github.com/robocorp/robocorp) as it is the main location where we developed the libraries and the framework.