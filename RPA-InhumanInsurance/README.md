# Template: Python - RPA Inhuman Insurance

### The business Idea
Each year, the Inhuman Insurance, Inc. Artificial Intelligence System (IIIAIS) system collects the lowest road traffic fatality rates globally and submits them to an insurance sales system for selling outrageously over-priced insurances to countries with the lowest fatality rate.

The idea is to scare the potential buyers with alternative facts about the genuine possibility of a nasty accident.

High insurance prices combined with a low risk of actual accidents will guarantee new yachts for the executives of Inhuman Insurance, Inc.! 

### The missing pieces
The only missing piece from the winning formula is integrating the road traffic fatality rate API and the insurance sales system that needs the data for finding the best sales targets.

```
┌──────────┐   ┌───────┐   ┌────────┐
│ Traffic  |   |       |   | Sales  |
| data     │ → │ Robot │ → │ system │ → 🛥💰🥂
| API      |   |       |   | API    |
└──────────┘   └───────┘   └────────┘
```

Doing all that data entry by hand is not an option. It takes too long, has a high risk of manual errors, is mind-bogglingly dull, and would render this course obsolete (we need to pay for our food, too! 🥺).

### Solution
This robot use work items:
- One task  (`Produce traffic data work items`) is to generate the sales system API payload from the raw traffic data (the input).
- The other (`Consume traffic data work items`) is to process that data and submit it to the insurance sales system.

```
┌──────────┐   ┌────────────┐   ┌──────────┐
│ Producer │ → │ Work items │ → │ Consumer │ → 💰
└──────────┘   └────────────┘   └──────────┘
```

The failed entries will need to be retried later or edited and fixed manually in case of business exceptions.

A business exception can be caused by invalid data, for example. Such an exception might require manual handling since retrying will not help if the data is invalid. It is best to try and catch invalid data and flag it for manual inspection.

Application exceptions are any exceptions caused by technical issues. These can usually be resolved by retrying actions until they succeed.


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