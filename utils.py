import random
from llama_index.core import StorageContext, load_index_from_storage

from llama_index.core import VectorStoreIndex, SummaryIndex, Document
from llama_index.core.storage import StorageContext
from llama_index.core.vector_stores import SimpleVectorStore
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.storage.index_store import SimpleIndexStore
from llama_index.core import Settings, load_index_from_storage

VECTOR_INDEX_PATH="data/vector_index"
SUMMARY_INDEX_PATH="data/summary_index"

def dict_to_document(article):
    return Document(
        text=article['Text'],
        metadata={
            'url': article['URL'],
            'published_at': article['PublishedAt']
        }
    )

def setup_indexes(dir_suffix=""):
    storage_context_v = StorageContext.from_defaults(
        vector_store=SimpleVectorStore(),
        docstore=SimpleDocumentStore(),
        index_store=SimpleIndexStore())
    storage_context_s = StorageContext.from_defaults(
        docstore=SimpleDocumentStore(),
        index_store=SimpleIndexStore())
    # Create empty indexes
    vector_index = VectorStoreIndex([], storage_context=storage_context_v)
    summary_index = SummaryIndex([], storage_context=storage_context_s)
    save_indexes(vector_index, summary_index, dir_suffix=dir_suffix)
    return vector_index, summary_index


def read_indexes(dir_suffix=""):
    
    # Load the vector index
    vector_storage_context = StorageContext.from_defaults(
        persist_dir=f"{VECTOR_INDEX_PATH}{dir_suffix}"
    )
    vector_index = load_index_from_storage(storage_context=vector_storage_context)
    summary_storage_context = StorageContext.from_defaults(
        persist_dir=f"{SUMMARY_INDEX_PATH}{dir_suffix}"
    )
    summary_index = load_index_from_storage(storage_context=summary_storage_context)
    
    return vector_index, summary_index

def save_indexes(vector_index, summary_index, dir_suffix=""):
    vector_index.storage_context.persist(persist_dir=f"{VECTOR_INDEX_PATH}{dir_suffix}")
    summary_index.storage_context.persist(persist_dir=f"{SUMMARY_INDEX_PATH}{dir_suffix}")

def add_to_indexes(articles, vector_index, summary_index):
    for article in articles:
        doc = dict_to_document(article)
    
        # Add to vector index
        vector_index.insert(doc)
    
        # Add to summary index
        summary_index.insert(doc)
 

def print_sample_node(vector_index_path):
    # Load the vector index
    storage_context = StorageContext.from_defaults(persist_dir=vector_index_path)
    vector_index = load_index_from_storage(storage_context=storage_context)

    # Access the docstore
    docstore = vector_index.storage_context.docstore

    # Get all document IDs
    doc_ids = list(docstore.docs.keys())

    if not doc_ids:
        print("No documents found in the index.")
        return

    # Select a random document ID
    random_doc_id = random.choice(doc_ids)

    # Retrieve the node
    node = docstore.get_node(random_doc_id)

    # Print node information
    print("Sample Node:")
    print(f"Node ID: {node.node_id}")
    print(f"Node Type: {type(node).__name__}")
    print("Node Content:")
    print(node.get_content())

    # If you want to print additional metadata
    print("\nMetadata:")
    for key, value in node.metadata.items():
        print(f"{key}: {value}")

