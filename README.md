Automatic summarization is a technique used to extract useful data about an article, and the data extracted have benefits to a multitude of areas.
AutoSum is our personal automatic summarization, based on extractive summarization technique that includes the following capacities:
- Extract up to 6 most central sentences of an article
- Compare the similarity between two articles and their shared keywords
- Construct a cluster tree that describe the closeness between multiple articles

User interacts with AutoSum by providing the urls of the article(s). The content of the article is extracted through the Goose API, and is analyzed by our very own summarization library.

The service is built on Djangos framework, and the front-end is designed with Zurb Foundation.


