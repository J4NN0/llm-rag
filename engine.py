def run_chat_engine(index):
    # Create chat engine that can be used to query the index
    chat_engine = index.as_chat_engine(similarity_top_k=3, chat_mode="context")
    while True:
        query_str = input("\nQ: ")
        if query_str == "exit":
            print("Cya!")
            break
        if query_str.strip() == "":
            continue

        streaming_response = chat_engine.stream_chat(query_str)
        for token in streaming_response.response_gen:
            print(token, end="")


def run_query_engine(index):
    # Create query engine that can be used to query the index
    query_engine = index.as_query_engine(similarity_top_k=3, streaming=True)
    while True:
        query_str = input("\nQ&A: ")
        if query_str == "exit":
            print("Cya!")
            break
        if query_str.strip() == "":
            continue

        streaming_response = query_engine.query(query_str)
        streaming_response.print_response_stream()
