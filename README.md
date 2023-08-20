# CatGPT

![image](https://github.com/lambrou/CatGPT/assets/42124973/34bdbebc-5843-4d02-8e96-919e65317237)


A GPT-powered cat with Google Search that sits on top of all your windows.

## Requirements
```shell
Python 3.11
  poetry (optional, dependency management)
  langchain
  tiktoken
  openai
  google-search-results
  Using Black for code formatting
```

### API Keys
```shell
OPENAI_API_KEY for GPT
SERPAPI_API_KEY for Google Search
```
https://serpapi.com/users/welcome

https://openai.com/

## Usage
Install dependencies manually using pip or using poetry:
```shell
pip install poetry
cd catgpt
poetry install
```

```shell
export OPENAI_API_KEY=YOUR_API_KEY
export SERP_API_KEY=YOUR_API_KEY
python main.py
```
