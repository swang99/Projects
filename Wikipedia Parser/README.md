# Wikipedia Article Parser

<p align="left">
  <img width="200" height="150" src="https://i.insider.com/5fbd515550e71a001155724f?width=600&format=jpeg&auto=webp">
</p>

### About
A simple question answering system that retrives information from a corpus of text files.
When presented with a query (a user-inputted question in English), document retrieval will first identify which files are most relevant to the query. Once the top documents are found, it will be divided into sentences so that the most relevant one to the question can be determined.

The statistical measure I used to determine relevant matches is called tf-idf. It ranks documents based on the term frequency for words in the query and the inverse document frequency of the word, which measures its rarity inside the corpus. After finding the most relevant documents, I used a combination of inverse document frequency and query term density to score the sentences. Query term density is the proportion of words in the sentence that are also words in the query.

### Files
- corpus - folder of Wikipedia articles for the AI to parse
- questions.py - where the user inputs their questions and gets the best answer based on 

### Sample Questions and Inputs
- Who developed probability?
- How are the methods of machine learning and statistics related?
- When was Python released?
- How do neurons connect in a neural network?
- What are the types of supervised learning?
- What is this the can? → invalid question
- x / exit → exits the program  
  
Note: the wording of the question matters a lot, so look inside the corpus documents to strategically phrase them.

### System Requirements  
#### nltk
You might also need to use the following prompts in the terminal:  
`python -m nltk.downloader stopwords`  
`python -m nltk.downloader 'punkt'`
