# Resin

**Resin** is a Sofware Development Kit and a Framework for AI applications. Resin allows you to test, build and package Retrieval Augmented Applications with Pinecone Vector Database. **Resin** is desinged to be well packaged and easy to use. It can be used as-a-library or as-a-service and designed to be modular, so you can use only the parts that you need. 

* **Ease of use** - Installed with a single command and can deploy an AI application in minutes. **Resin** is designed to be easy to use and easy to integrate with your existing applications and compatible with OpenAI /chat/completions API. 

* **Operational & Production ready** - Resin is built on top of **Pinecone** and can Scale to billions of vectors. Unlike other AI frameworks, **Resin** optimizes for production use cases it allows developers to set up operating point to have better control over token consumption in prompt or in generation. **Resin** can maximize context quality and relevance while controlling the cost of the AI system.

* **Open source** - **Resin** is open source and free to use. It is also designed to be open and extensible, so you can easily add your own components and extend the functionality.


## What's inside the box?

1. **Resin Core** - the core library. Resin has 3 high level classes that act as API level components:
    * **ChatEngine** - is a complete RAG unit [TBD]
    * **ContextEngine** - is a proxy between your application and Pinecone. It will handle the R in the RAG pipeline and will return the snippet of context along with the respected source. 
    * **KnowledgeBase** - is the data managment interface, handles the processing, chunking and encoding (embedding) of the data, along with Upsert/Query and Delete operations

2. **Resin Service** - a service that wraps the **Resin Core** and exposes it as a REST API. The service is built on top of FastAPI and Uvicorn and can be easily deployed in production. 

3. **Resin CLI** - [TBD]


## How to install

1. Set up the environment variables

```bash
export PINECONE_API_KEY="<PINECONE_API_KEY>"
export PINECONE_ENVIRONMENT="<PINECONE_ENVIRONMENT>"
export OPENAI_API_KEY="<OPENAI_API_KEY>"
export INDEX_NAME="test-index-1"
```

2. install the package
```bash
pip install pinecone-resin
```

3. you are good to go! see the quickstart guide on how to run basic demo

## Quickstart

In this quickstart, we will show you how to use the **Resin** to build a simple question answering system using RAG (retrival augmented generation).

### 0. Before we start

Before we start, run the `resin` command alone to verify the connection to services in healthy:
    
```bash
resin
```

output should be similar to this:

```bash
Resin: Ready

Usage: resin [OPTIONS] COMMAND [ARGS]...
# rest of the help message
```


### 1. Create a new **Resin** Index

**Resin** will create and configure a new Pinecone index on your behalf. Just run:

```bash
resin new
```

And follow the CLI instructions. The index that will be created will have a prefix `resin--<INDEX_NAME>`.

> Note, this will have to be done only once per index.

![](https://github.com/pinecone-io/context-engine/blob/change-readme-cli-names/.readme-content/resin-new.gif)

### 2. Uploading data

You can load data into your **Resin** Index by simply using the CLI:

```bash
resin upsert <PATH_TO_DATA>
```

The data should be in a parquet format where each row is a document. The documents should have the following schema:

```
+----------+--------------+--------------+---------------+
| id(str)  | text(str)    | source(str)  | metadata(dict)|
|----------+--------------+--------------+---------------|
| "1"      | "some text"  | "some source"| {"key": "val"}|
+----------+--------------+--------------+---------------+
```

Follow the instructions in the CLI to upload your data.

![](https://github.com/pinecone-io/context-engine/blob/change-readme-cli-names/.readme-content/resin-upsert.gif)

### 3. Start the **Resin** service

**Resin** service serve as a proxy between your application and Pinecone. It will also handle the RAG part of the application. To start the service, run:

```bash
resin start
```

Now, you should be prompted with standard Uvicorn logs:

```
Starting Resin service on 0.0.0.0:8000
INFO:     Started server process [24431]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

![](https://github.com/pinecone-io/context-engine/blob/change-readme-cli-names/.readme-content/resin-start.gif)


### 4. Chat with your data

Now that you have data in your index, you can chat with it using the CLI:

```bash
resin chat
```

This will open a chat interface in your terminal. You can ask questions and the **Resin** will try to answer them using the data you uploaded.

![](https://github.com/pinecone-io/context-engine/blob/change-readme-cli-names/.readme-content/resin-chat.gif)

To compare the chat response with and without RAG use the `--no-rag` flag

```bash
resin chat --no-rag
```

This will open a similar chat interface window, but will send your question directly to the LLM without the RAG pipeline.

![](https://github.com/pinecone-io/context-engine/blob/change-readme-cli-names/.readme-content/resin-chat-no-rag.gif)


### 5. Stop the **Resin** service

To stop the service, simply press `CTRL+C` in the terminal where you started it.

If you have started the service in the background, you can stop it by running:

```bash
resin stop
```

## Advanced usage

### 1. Migrating existing OpenAI application to **Resin**

If you already have an application that uses the OpenAI API, you can migrate it to **Resin** by simply changing the API endpoint to `http://host:port/context` as follows:

```python
import openai

openai.api_base = "http://host:port/context"

# now you can use the OpenAI API as usual
```

or without global state change:

```python
import openai

openai_response = openai.Completion.create(..., api_base="http://host:port/context")
```
