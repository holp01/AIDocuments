from flask import Flask, request, jsonify
from cache import cache_manager
from indexing import indexer
from pdf_extraction import extractor
from database import database_helper
import openai
import pdb; 

app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask():
    query = request.json.get('query')
    
    # Step 1: Search for relevant document identifiers based on user's query
    matching_ids = indexer.search_index(query)
    
    if not matching_ids:
        return jsonify({"error": "No relevant context found"}), 400

    # Fetch and combine content of all matched documents as context
    context = ""
    for doc_id in matching_ids:
        doc_content = cache_manager.get_cached_content(doc_id)
        context += doc_content + "\n\n"

    # Step 2: Send the combined context and the query to your AI model
    response = ai_response(query, context)
    
    return jsonify({"response": response})

# @app.route('/update', methods=['POST'])
# def update():
#     post_id = request.json.get('post_id')

#     # Step 1: Fetch the new post from the database
#     # post = database_helper.fetch_post_by_id(post_id)
#     # if not post:
#     #     return jsonify({"error": "Post not found"}), 400

#     # Step 2: Download and extract content
#     content = cache_manager.get_cached_content(post_id)
#     if not content:
#         content = download_and_extract_content(post)  # This function combines downloading and extraction logic
#         cache_manager.cache_content(content, post_id)  # Cache the content for future use

#     # Step 3: Update the index
#     indexer.update_index(content, post_id)

#     return jsonify({"status": "Updated successfully"})

@app.route('/update', methods=['POST'])
def update():
    topic = request.json.get('topic')

    # Step 2: Download and extract content
    content = cache_manager.get_cached_content(topic)
    if not content:
        content = download_and_extract_content(topic)  # Extract from txt
        cache_manager.cache_content(content, topic)  # Cache the content

    # Step 3: Update the index
    indexer.update_index(content, topic)

    return jsonify({"status": "Updated successfully"})

# Set up your API key (better to use environment variables in production)
openai.api_key = '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'

def ai_response(query, context):
    """
    Uses OpenAI's GPT-3 model to generate a response based on the provided query and context.
    """
    try:
        response = openai.Completion.create(
            engine="davinci",  # Use "davinci" or another suitable engine
            prompt=f"{context}\n\nQuestion: {query}\nAnswer:",
            max_tokens=150,  # Adjust this value based on your needs
            n=1,
            stop=["\n"],  # This makes sure the model stops generating after the first newline after "Answer:"
            temperature=0.7  # Adjust this value for randomness. Lower values make output more deterministic.
        )

        # Extracting the response text
        answer = response.choices[0].text.strip()

        return answer
    except Exception as e:
        # Handle exceptions and potentially log them
        return f"Error: {str(e)}"


def download_and_extract_content(topic):
    file_path = f"data/{topic}.txt"
    return extractor.extract_from_txt(file_path)

def initialize():
    topics = ["1", "2", "3"]
    for topic in topics:
        content = download_and_extract_content(topic)
        cache_manager.cache_content(content, topic)
        indexer.update_index(content, topic)

if __name__ == '__main__':
    initialize()  # Initialize and index at startup
    app.run(debug=True)

