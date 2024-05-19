# Project Title

This project is a Python-based application that uses OpenAI's GPT-4 model to answer questions based on a given context. It loads data from a file, formats it, and uses it as a context to answer the provided question. The project uses several libraries including `langchain_chroma`, `langchain_community`, `langchain_core`, `langchain_openai`, and `langchain_text_splitters`.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8 or higher
- pip

### Installing

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required packages using pip:

```bash
pip install -r requirements.txt
```

## Usage

The main script of the project is `question_retriever.py`. It takes a question as an argument and prints the answer to the console. Before running the script, you need to set the OpenAI API key as an environment variable. If it's not set, the script will prompt you to enter it.

Here is an example of how to use the script:

```bash
python question_retriever.py "Your question here"
```

## Built With

- Python
- OpenAI's GPT-4 model
- langchain libraries

## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.

## Acknowledgments

- OpenAI for providing the GPT-4 model
- The langchain libraries for providing the tools to build this project