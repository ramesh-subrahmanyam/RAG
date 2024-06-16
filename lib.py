from bs4 import BeautifulSoup
import requests
from langchain.docstore.document import Document


def url_to_paragraphs(url):
  """
  Given a URL, returns a list of paragraphs extracted from the article.

  Args:
      url: A string containing the URL of the article.

  Returns:
      list: A list of strings, each string representing a paragraph in the article.
  """

  # Download the webpage
  response = requests.get(url)

  # Parse the HTML
  soup = BeautifulSoup(response.content, 'html.parser')

  # Extract the text from the article
  article_text = soup.find_all('p')

  # Create a list of paragraphs
  documents = []
  for paragraph in article_text:
    documents.append(Document(page_content=paragraph.get_text(), 
                              metadata=dict(url=url)))
  return documents

class id_maker:
  def __init__(self, start=0):
      self.i=start
  def f(self):
    self.i+=1
    return str(self.i)
  
    

def add_data_to_db(urls, vector_store, id):
    # Create or get an existing collection
  for url in urls:
      documents = url_to_paragraphs(url)
      vector_store.add_documents(documents) 
  vector_store.persist() 
          

