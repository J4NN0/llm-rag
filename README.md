# themis-ai

This repository provides documentation and resources for understanding basic concepts behind Large Language Models (LLMs), [LlamaIndex](https://www.llamaindex.ai/) framework and  the process of fine-tuning LLMs with custom data.

# Table of Contents

- [Large Language Models (LLMs)](#large-language-models-llms)
- [LlamaIndex Framework](#llamaindex-framework)
- [Fine-Tuning and Retrieval Augmented Generation (RAG)](#fine-tuning-and-retrieval-augmented-generation-rag)
- [Usage](#usage)
- [Resources](#resources)

# Large Language Models (LLMs)

LLMs are a type of artificial intelligence model designed to understand and generate human-like text based on the patterns and structures present in vast amounts of textual data. These models have become increasingly sophisticated, thanks to advancements in deep learning, particularly using transformer architectures. Popular examples of LLMs include OpenAI's [GPT series](https://chat.openai.com/) (e.g., GPT-3), [Llama 2](https://ai.meta.com/llama/) (from Meta), and others. 

Large language models consist of a complex arrangement of neural network layers, each playing a crucial role in processing input text and generating meaningful output content. 

The **embedding layer** is responsible for crafting embeddings from the input text. This specific component of the large language model encapsulates both the semantic and syntactic nuances of the input, facilitating the model's comprehension of contextual information.

At the core of a large language model's architecture is the **feedforward layer**, comprising multiple fully connected layers. These layers serve to transform the input embeddings, enabling the model to extract higher-level abstractions and gain a profound understanding of the user's intent behind the provided text.

To enhance focus on pertinent details, large language models employ an **attention mechanism**. This mechanism allows the model to selectively concentrate on specific parts of the input text relevant to the task at hand, thereby optimizing the generation of precise and contextually accurate outputs.

Large language models come in three primary categories:
- Generic or Raw Language Models: These models predict the next word based on patterns learned from the language in the training data. Their primary function is to perform information retrieval tasks, making them adept at comprehending and generating content.
- Instruction-Tuned Language Models: Specifically trained to predict responses aligned with provided instructions in the input. This specialization equips them to excel in tasks such as sentiment analysis, as well as in generating text or code based on instructional cues.
- Dialog-Tuned Language Models: Tailored to engage in dialogues by predicting the next response. Applications include chatbots and conversational AI, where these models showcase their ability to understand and generate contextually relevant responses within a conversational framework.

# LlamaIndex Framework

LlamaIndex stands as a versatile and uncomplicated data framework tailored for linking custom data sources with expansive language models, offering essential tools to enhance applications using large language models (LLMs). The framework encompasses the following key functionalities:
- Data Ingestion: Seamlessly connect your diverse existing data sources, spanning various formats such as APIs, PDFs, documents, SQL, and more. This integration enables the utilization of these sources within applications powered by large language models.
- Data Indexing: Efficiently store and index your data to accommodate diverse use cases. LlamaIndex facilitates integration with downstream vector stores and database providers, enhancing the accessibility and retrieval of information.
- Query Interface: LlamaIndex features a user-friendly query interface capable of processing any input prompt related to your data. By employing this interface, you can obtain responses enriched with knowledge, contributing to a more informed and contextually relevant user experience.

# Fine-Tuning and Retrieval Augmented Generation (RAG)

LLMs, while trained on vast datasets, lack knowledge of your specific data. Retrieval-Augmented Generation (RAG) bridges this gap by integrating your data. Within RAG, your data undergoes loading and preparation, termed 'indexing.' User queries refine data to the most relevant context. This, combined with your query and prompt, is presented to RAG, generating a response. For chatbot or agent development, mastering RAG techniques is essential for seamless data integration into your application.

Within the RAG there are five key stages:
- Loading: This involves acquiring your data from its source, whether it's stored in text files, PDFs, another website, a database or an API.
- Indexing: Involves generating vector embeddings and employing various metadata strategies to facilitate accurate retrieval of contextually relevant information.
- Storage: After indexing, it is often beneficial to store the index and associated metadata to avoid the need for future reindexing.
- Retrieve: With various indexing strategies available, you can use LLMs data structures for querying, using techniques such as sub-queries, multi-step queries and hybrid strategies.
- Evaluation: It provides objective metrics to measure the accuracy, fidelity and speed of your responses to queries.

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
   - Set your OpenAI API key, you can get one in [platform.openai](https://platform.openai.com/api-keys)
   - Define the query engine you want to use: either `chat` or `query`

4. Run the script

    ```bash
    python3 main.py
    ```

# Resources

- [LlamaIndex Documentation](https://docs.llamaindex.ai/en/stable/index.html#)
- [Large language models](https://seantrott.substack.com/p/large-language-models-explained)
- [Building LLM applications for production](https://huyenchip.com/2023/04/11/llm-engineering.html)
