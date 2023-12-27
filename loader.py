from llama_index import download_loader


def __get_pages(file_path):
    """
    Reads the (web/link) pages from the given file path
    :param file_path: The path to the file containing the pages
    :return: List of pages
    """

    with open(file_path, "r") as f:
        links = f.readlines()
    return links


def load_wiki(wiki_file):
    """
    Loads the wikipedia pages from the given wikipedia file path
    :param wiki_file: The path to the file containing the wikipedia pages
    :return: List of llama-index documents
    """

    WikipediaReader = download_loader("WikipediaReader")
    loader = WikipediaReader()

    wiki_pages = __get_pages(wiki_file)
    documents = loader.load_data(pages=wiki_pages)

    return documents
