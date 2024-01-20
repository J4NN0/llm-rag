def run_chat_engine(index):
    # Create chat engine that can be used to query the index
    chat_engine = index.as_chat_engine(streaming=True, similarity_top_k=5)
    while True:
        query_str = input("\nQ: ")
        if query_str == "exit":
            break
        if query_str.strip() == "":
            continue

        response = chat_engine.chat(query_str)
        response.print_response_stream()


def run_query_engine(index):
    # Create query engine that can be used to query the index
    query_engine = index.as_query_engine(streaming=True, similarity_top_k=5)
    while True:
        query_str = input("\nQ&A: ")
        if query_str == "exit":
            break
        if query_str.strip() == "":
            continue

        response = query_engine.query(query_str)
        response.print_response_stream()
