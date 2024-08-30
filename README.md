# RISE Tool

The Risk Informed Synthetic Embedding (RISE) tool uses the final hidden layer activations of synthetic images to explore the behaviour

All images were generated from a risk log generated by an AI assurer. Additional risks were found using LLama3.1 8B, and then turned into image prompts. Dall-E3 was used to generate synthetic images using these image prompts. 

In order to use the tool, use the `RISE_tool.ipynb` file. 

## Using the RISE tool in Github Codespaces:

1 - Add a branch to this repo. You can do this by going to [here](https://github.com/willpoulett/RISE_Tool_V1/branches) and clicking `New branch`. Name the branch something unique.

2 - Within this branch open a github codespace. You can do this by pressing `.`. Alternatively, click the green `Code` button, and select 'Create a Codespace`

3 - Within your Codespace, navigate to `RISE_tool.ipynb` and connect to a codespace **kernal**.

4 - Run the cells in the  `RISE_tool.ipynb` notebook. You will need ato specify if you would like to use labels.

5 - An interactive tool wil appear, allowing you to explore the data. 

## Using the RISE Tool.

![Diagram explaining the use of the rise tool](content/how_to_use.png)
