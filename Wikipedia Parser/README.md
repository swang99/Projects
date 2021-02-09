# Wikipedia Article Parser

<p align="left">
  <img width="200" height="150" src="https://i.insider.com/5fbd515550e71a001155724f?width=600&format=jpeg&auto=webp">
</p>

### About
A simple question answering system based on inverse document frequency (IDF), that retrives information from a corpus of .txt files.
When presented with a query (a user-inputted question in English), document retrieval will first identify which files are most relevant to the query. Once the top documents are found, it will be subdivided into sentences so that the most relevant one to the question can be determined.

The algorithm I used to determine the most relevant document and sentences is called tf-idf. It ranks documents based on the term frequency for words in the query and the inverse document frequency for words in the query. Once we’ve found the most relevant documents, there many possible metrics for scoring passages, but we’ll use a combination of inverse document frequency and a query term density measure (described in the Specification).

### Files
- corpus - folder of Wikipedia articles for the AI to parse  
- questions.py - takes a user-inputted question and gives the best answer based on info in the corpus.

### Sample Questions and Inputs
- Who developed probability?
- How are the methods of machine learning and statistics related?
- When was Python released?
- How do neurons connect in a neural network?
- What are the types of supervised learning?
- What is this the can? → invalid question
- x / exit → exits the program

### System Requirements  
#### nltk
You might also need to use the following download prompts in the terminal:  
`python -m nltk.downloader stopwords`  
`python -m nltk.downloader 'punkt'`
