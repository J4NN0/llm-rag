# llama-index-rag

This repository provides documentation and resources for understanding the basic concepts behind Large Language Models (LLMs) and the process of fine-tuning LLMs with custom data from a variety of sources (e.g. text files, web pages, PDFs, etc.) using [LlamaIndex](https://www.llamaindex.ai/) framework.

# Table of Contents

- [Retrieval Augmented Generation (RAG)](#retrieval-augmented-generation-rag)
- [Usage](#usage)
- [Resources](#resources)

# Retrieval Augmented Generation (RAG)

LLMs are a type of artificial intelligence model designed to understand and generate human-like text based on the patterns and structures present in vast amounts of textual data. These models have become increasingly sophisticated thanks to advances in deep learning, particularly using transformer architectures.

While LLMs are trained on large datasets, they lack knowledge of your specific data. Retrieval-Augmented Generation (RAG) bridges this gap by integrating your data. Within RAG, your data undergoes a loading and preparation process called 'indexing'. User queries refine the data into the most relevant context. This, combined with your query and prompt, is presented to RAG to generate a response. For chatbot or agent development, mastering RAG techniques is essential for seamless data integration into your application.

Within the RAG there are five key stages:
- **Loading**: This involves acquiring your data from its source, whether it's stored in text files, PDFs, another website, a database, or an API.
- **Indexing**: Involves generating vector embeddings and employing various metadata strategies to facilitate accurate retrieval of contextually relevant information.
- **Storage**: After indexing, it is often beneficial to store the index and associated metadata to avoid the need for future reindexing.
- **Retrieve**: With various indexing strategies available, you can use LLMs data structures for querying, using techniques such as sub-queries, multi-step queries, and hybrid strategies.
- **Evaluation**: It provides objective metrics to measure the accuracy, fidelity, and speed of your responses to queries.

# Usage

1. Clone the repository

    ```bash
    git clone https://github.com/J4NN0/themis-ai.git
    cd themis-ai
    ```

2. Install requirements

    ```bash
    pip install -r requirements.txt
    ```

3. Set up `config.ini` file
   - Set your OpenAI API key. If you don't have one, you can get one in [platform.openai](https://platform.openai.com/api-keys)
   - Create and/or update your custom data as follows:
     - In `data/simple` folder for following [file types](https://docs.llamaindex.ai/en/stable/module_guides/loading/simpledirectoryreader.html#supported-file-types) (please note only this list of file types is supported within this directory):
       - `.csv` - comma-separated values 
       - `.docx` - Microsoft Word 
       - `.epub` - EPUB ebook format 
       - `.hwp` - Hangul Word Processor 
       - `.ipynb` - Jupyter Notebook 
       - `.jpeg`, .jpg - JPEG image 
       - `.mbox` - MBOX email archive 
       - `.md` - Markdown 
       - `.mp3`, .mp4 - audio and video 
       - `.pdf` - Portable Document Format 
       - `.png` - Portable Network Graphics 
       - `.ppt`, `.pptm`, `.pptx` - Microsoft PowerPoint
     - In `data/json` only for `.json` files. 
     - In `data/web` for web pages:
       - Use `wikipedia_pages.txt` for Wikipedia pages.

     In case you want to connect it to more data sources, please refer to [Data Connectors for LlamaIndex](https://docs.llamaindex.ai/en/stable/api_reference/readers.html#classes) or write your own data reader.

   And optionally:
      - Set level output verbosity: `DEBUG` for verbose or `INFO` for less.
      - Define the index engine you want to use: `CHAT` for chat engine or `QUERY` for Q&A engine.
      - The index storage path: `./storage` by default.

4. Run the chatbot

    ```bash
    python3 main.py
    ```

# Resources

- [LlamaIndex Documentation](https://docs.llamaindex.ai/en/stable/index.html#)
- [Large language models, explained with a minimum of math and jargon](https://seantrott.substack.com/p/large-language-models-explained)
- [Building LLM applications for production](https://huyenchip.com/2023/04/11/llm-engineering.html)
