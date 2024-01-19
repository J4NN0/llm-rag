# llama-index-rag

This repository provides documentation and resources for understanding the basic concepts behind Large Language Models (LLMs) and the process of fine-tuning LLMs with custom data from a variety of sources (e.g. text files, web pages, PDFs, etc.) using [LlamaIndex](https://www.llamaindex.ai/) framework.

# Table of Contents

- [Retrieval Augmented Generation (RAG)](#retrieval-augmented-generation-rag)
- [Environment Setup](#environment-setup)
- [Ingest your data](#ingest-your-data)
- [Chat with your documents](#chat-with-your-documents)
- [Resources](#resources)

# Retrieval Augmented Generation (RAG)

LLMs are a type of artificial intelligence model designed to understand and generate human-like text based on the patterns and structures present in vast amounts of textual data. These models have become increasingly sophisticated thanks to advances in deep learning, particularly using transformer architectures.

While LLMs are trained on large datasets, they lack knowledge of your specific data. Retrieval-Augmented Generation (RAG) bridges this gap by integrating your data. Within RAG, your data undergoes a loading and preparation process called 'indexing'. User queries refine the data into the most relevant context. Combined with your query and prompt, this is presented to RAG to generate a response. For chatbot or agent development, mastering RAG techniques is essential for seamless data integration into your application.

Within the RAG there are five key stages:
- **Loading**: This involves acquiring your data from its source, whether it's stored in text files, PDFs, another website, a database, or an API.
- **Indexing**: Involves generating vector embeddings and employing various metadata strategies to facilitate accurate retrieval of contextually relevant information.
- **Storage**: After indexing, it is often beneficial to store the index and associated metadata to avoid the need for future reindexing.
- **Retrieve**: With various indexing strategies available, you can use LLMs data structures for querying, using techniques such as sub-queries, multi-step queries, and hybrid strategies.
- **Evaluation**: It provides objective metrics to measure the accuracy, fidelity, and speed of your responses to queries.

# Environment Setup

1. Clone the repository

       git clone https://github.com/J4NN0/llama-index-rag.git
       cd llama-index-rag

2. Install requirements

       pip install -r requirements.txt

3. Copy the example.env template into .env and source them however you like:
       
       cp .sample.env .env

4. Update the variables accordingly
   - Decide if you want to use a local LLM or OpenAI API ChatGPT model
     - If you want to use a **local LLM**:
       - Set `MODEL_TYPE` to `LOCAL`.
       - Set `MODEL_NAME` to the name of the model you want to use.
     - If you want to use OpenAI API **ChatGPT model**:
        - Set `MODEL_TYPE` to `DEFAULT`.
        - Set `OPENAI_API_KEY` to your OpenAI API key. If you don't have one, you can get one in [platform.openai](https://platform.openai.com/api-keys).

5. Optionally, you can update the following variables
   - `LOGGING_LEVEL` to set level output verbosity:
     - Set to `DEBUG` for verbose 
     - Set to `INFO` for less.
   - `INDEX_STORAGE` to set the path where to store the index. By default, it is set to `./storage`.
   - `INDEX_ENGINE` to define the index engine you want to use: 
     - Set to `CHAT` for chat engine
     - Set to `QUERY` for Q&A engine.
   - `DATA_DIR` to set the path where your custom documents are stored. By default, it is set to `./data`.

# Ingest your data

Add all the files you want to chat with in the `data` folder The following file types are supported (please note only this list of file types is supported within this directory):
   - `.csv` - comma-separated values 
   - `.docx` - Microsoft Word 
   - `.epub` - EPUB ebook format 
   - `.hwp` - Hangul Word Processor 
   - `.ipynb` - Jupyter Notebook 
   - `.jpeg`, `.jpg` - JPEG image 
   - `.mbox` - MBOX email archive 
   - `.md` - Markdown 
   - `.mp3`, `.mp4` - audio and video 
   - `.pdf` - Portable Document Format 
   - `.png` - Portable Network Graphics 
   - `.ppt`, `.pptm`, `.pptx` - Microsoft PowerPoint
   - `.json` - JSON file

For Wikipedia pages, you can use `.wikipedia` file extension and insert as many Wikipedia page titles as you want in the file. 
   - Note that only the page name is required, not the full URL.
   - For instance for the Berlin Wikipedia page (at [wikipedia.org/wiki/Berlin](https://en.wikipedia.org/wiki/Berlin)), just insert `Berlin` in the file.

In case you want to connect it to more data sources, please refer to [Data Connectors for LlamaIndex](https://docs.llamaindex.ai/en/stable/api_reference/readers.html#classes), [LlamaHub](https://llamahub.ai/) or write your data reader.

# Chat with your documents

To start chatting with your documents, run the following command:

    python3 main.py

# Resources

- [LlamaIndex Documentation](https://docs.llamaindex.ai/en/stable/index.html#)
- [Large language models, explained with a minimum of math and jargon](https://seantrott.substack.com/p/large-language-models-explained)
- [Building LLM applications for production](https://huyenchip.com/2023/04/11/llm-engineering.html)
