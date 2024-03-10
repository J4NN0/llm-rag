# llm-rag

This repository provides documentation and resources for understanding the basic concepts behind Large Language Models (LLMs) and the process of augments LLMs prompt with Retrieval Augmented Generation (RAG) by integrating external custom data from a variety of sources (e.g. text files, web pages, PDFs, etc.) using [LlamaIndex](https://www.llamaindex.ai/) framework. This allows you to ask questions about such documents.

# Table of Contents

- [Retrieval Augmented Generation (RAG)](#retrieval-augmented-generation-rag)
- [Environment Setup](#environment-setup)
- [Ingest your data](#ingest-your-data)
- [Chat with your documents](#chat-with-your-documents)
- [Local LLM vs Cloud-based LLM](#local-llm-vs-cloud-based-llm)
- [Quantization methods](#quantization-methods)
- [Resources](#resources)

# Retrieval Augmented Generation (RAG)

LLMs are a type of artificial intelligence model designed to understand and generate human-like text based on the patterns and structures present in vast amounts of textual data. These models have become increasingly sophisticated thanks to advances in deep learning, particularly using transformer architectures.

While LLMs are trained on large datasets, they lack knowledge of your specific data. Retrieval-Augmented Generation (RAG) bridges this gap by integrating your data. In RAG, your data is loaded and prepared for queries or "indexed". User queries act on the index, which filters your data down to the most relevant context. This context and your query then go to the LLM along with a prompt, and the LLM provides a response. For chatbot or agent development, mastering RAG techniques is essential for seamless data integration into your application.

Within the RAG there are five key stages:
- **Loading**: This involves acquiring your data from its source, whether it's stored in text files, PDFs, another website, a database, or an API.
- **Indexing**: Involves generating vector embeddings and employing various metadata strategies to facilitate accurate retrieval of contextually relevant information.
- **Storage**: After indexing, it is often beneficial to store the index and associated metadata to avoid the need for future reindexing.
- **Retrieve**: With various indexing strategies available, you can use LLMs data structures for querying, using techniques such as sub-queries, multi-step queries, and hybrid strategies.
- **Evaluation**: It provides objective metrics to measure the accuracy, fidelity, and speed of your responses to queries.

# Environment Setup

1. The project has been tested with Python `3.10` (version `3.10.11` to be exact). To check your Python version run

       python3 --version

   If you have a different one, you can download version `3.10.X` in the [Python releases archive](https://www.python.org/downloads/). 

2. Clone the repository

       git clone https://github.com/J4NN0/llm-rag.git
       cd llm-rag

3. Install requirements

       pip install -r requirements.txt

4. Copy the example.env template into .env and source them however you like
       
       cp .sample.env .env

5. Decide if you want to use a local LLM or OpenAI model (in case you don't know what to choose, refer to the below section [Local LLM vs Cloud-based LLM](#local-llm-vs-cloud-based-llm) and [Quantization methods](#quantization-methods))
   - If you want to use a **local LLM**:
     - Set `MODEL_TYPE` to the LLM you want to use between the supported ones:
       - `LLAMA2-7B_Q4` - medium, balanced quality (7 billion parameters)
       - `LLAMA2-7B_Q5` - large, very low-quality loss (7 billion parameters)
       - `LLAMA2-13B_Q4` - medium, balanced quality (13 billion parameters)
       - `LLAMA2-13B_Q5` - large, very low-quality loss (13 billion parameters)
       - `MIXTRAL-7B_Q4` - medium, balanced quality (7 billion parameters)
       - `MIXTRAL-7B_Q5` - large, very low-quality loss (7 billion parameters)
       
     Each downloaded model is cached in `~/Users/$USER/Library/Caches/llama_index` to avoid downloading it again.

   - If you want to use **OpenAI model**:
     - Set `MODEL_TYPE` to `DEFAULT`.
     - Set `OPENAI_API_KEY` to your OpenAI API key. If you don't have one, you can get one in [platform.openai](https://platform.openai.com/api-keys).

6. Optionally, you can update the following variables
   - `LOGGING_LEVEL` to set level output verbosity:
     - Set to `DEBUG` for verbose 
     - Set to `INFO` for less.
   - `INDEX_STORAGE` to set the path where to store the index. By default, it is set to `./vector_store`.
   - `DATA_DIR` to set the path where your custom documents are stored. By default, it is set to `./data`.

# Ingest your data

Add all the files you want to chat with in the `data` folder. The following file types are supported:
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

You can also ingest data from Wikipedia pages. To do so, you can use `.wikipedia` file extension and insert as many Wikipedia page titles as you want in the file.
   - Note that only the page name is required, not the full URL.
   - For instance for the Berlin Wikipedia page (at [wikipedia.org/wiki/Berlin](https://en.wikipedia.org/wiki/Berlin)), just insert `Berlin` in the file.

In case you want to connect it to more data sources, please refer to [Data Connectors for LlamaIndex](https://docs.llamaindex.ai/en/stable/api_reference/readers.html#classes), [LlamaHub](https://llamahub.ai/) or write your data reader.

To ingest all the data, run the following command

    python3 main.py --load-data

Or just

    python3 main.py -L

It will create a folder (named `vector_store` by default) containing the local vectorstore. The time of ingestion depends on the size of each single document.

# Chat with your documents

To start chatting with your documents, run the following command

    python3 main.py --query-data

Or just

    python3 main.py -Q

Wait for the local vectorstore to be loaded, and then you can start chatting with your documents. Write your query and hit enter. The model consumes the prompt and prepares the answer (waiting time depends on your machine in case of local LLM, or OpenAI system load)

For instance, asking about myself based on the customs documents fed before:

```
Q: Why is Federico's nickname J4NN0?
```

The model's answer should be:

> Federico's nickname "J4NN0" was given to him by a friend during one of his League of Legends games. The friend started calling him "J4NN0" because he was playing so well that it sounded like "Janna," which is a character in the game. Federico found the nickname funny and decided to keep it as his nickname.

Such information - which is actually not true at all (it was proposed by GitHub Copilot and I accepted it) - is contained in [data/j4nn0.md](https://github.com/J4NN0/llm-rag/blob/main/data/j4nn0.md).

Type `exit` to finish chatting with the documents.

# Local LLM vs Cloud-based LLM

When it comes to running an LLM locally versus using a cloud-based service (such as [ChatGPT](https://chat.openai.com/)), the main differences often concern where the model is hosted and where the calculation takes place. But privacy issues are also an important aspect of this discussion.

Running an LLM locally means that the model is deployed on your own device (e.g., your computer or a server you control). The data and computations associated with the model are confined to your local environment, providing a higher level of privacy as your data doesn't leave your device.

Cloud-based LLM typically involves interacting with a model hosted on a (cloud) server. When a request is sent, the input is processed by the model on the server side. This means your input data is temporarily stored and processed on external servers, raising privacy concerns as the service provider has access to the data you input, at least temporarily.

# Quantization methods

The names of the quantization methods follow the naming convention: "q" + the number of bits + the variant used (in the *attention* and *feedforward* layers). The following `S`, `M` and `L` refer to "Small", "Medium" and "Large" respectively. In the models above, the variant used is omitted as it is always the same i.e., `K_M`. The [lower the quantization](https://github.com/ggerganov/llama.cpp/pull/1684#issuecomment-1579252501), the lower the memory consumption but also the higher the perplexity loss (a metric indicating a model's proficiency in predicting the subsequent word based on the context provide).

As a rule of thumb, it is recommended to use `Q5_K_M` as it preserves most of the model's performance. Alternatively, you can use `Q4_K_M` to save some memory.

Difference in different quantization methods:
```
 2  or  Q4_0   :  3.50G, +0.2499 ppl @ 7B - small, very high quality loss - legacy, prefer using Q3_K_M
 3  or  Q4_1   :  3.90G, +0.1846 ppl @ 7B - small, substantial quality loss - legacy, prefer using Q3_K_L
 8  or  Q5_0   :  4.30G, +0.0796 ppl @ 7B - medium, balanced quality - legacy, prefer using Q4_K_M
 9  or  Q5_1   :  4.70G, +0.0415 ppl @ 7B - medium, low quality loss - legacy, prefer using Q5_K_M
10  or  Q2_K   :  2.67G, +0.8698 ppl @ 7B - smallest, extreme quality loss - not recommended
12  or  Q3_K   : alias for Q3_K_M
11  or  Q3_K_S :  2.75G, +0.5505 ppl @ 7B - very small, very high quality loss
12  or  Q3_K_M :  3.06G, +0.2437 ppl @ 7B - very small, very high quality loss
13  or  Q3_K_L :  3.35G, +0.1803 ppl @ 7B - small, substantial quality loss
15  or  Q4_K   : alias for Q4_K_M
14  or  Q4_K_S :  3.56G, +0.1149 ppl @ 7B - small, significant quality loss
15  or  Q4_K_M :  3.80G, +0.0535 ppl @ 7B - medium, balanced quality - *recommended*
17  or  Q5_K   : alias for Q5_K_M
16  or  Q5_K_S :  4.33G, +0.0353 ppl @ 7B - large, low quality loss - *recommended*
17  or  Q5_K_M :  4.45G, +0.0142 ppl @ 7B - large, very low quality loss - *recommended*
18  or  Q6_K   :  5.15G, +0.0044 ppl @ 7B - very large, extremely low quality loss
 7  or  Q8_0   :  6.70G, +0.0004 ppl @ 7B - very large, extremely low quality loss - not recommended
 1  or  F16    : 13.00G              @ 7B - extremely large, virtually no quality loss - not recommended
 0  or  F32    : 26.00G              @ 7B - absolutely huge, lossless - not recommended
```

# Resources

- [LlamaIndex Documentation](https://docs.llamaindex.ai/en/stable/index.html#)
- [Large language models, explained with a minimum of math and jargon](https://seantrott.substack.com/p/large-language-models-explained)
- [Building LLM applications for production](https://huyenchip.com/2023/04/11/llm-engineering.html)
- [TheBloke - Hugging Face](https://huggingface.co/TheBloke)
