from flask import Flask, request, jsonify
from azurehelper import azure_manager
from indexing import indexer
from pdf_extraction import extractor
import openai
import os

app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask():
    query = request.json.get('query')
    
    # Step 1: Search for relevant document identifiers based on user's query
    matching_ids = indexer.search_index(query)
    if not matching_ids:
        return jsonify({"response": "I'm sorry, seems that the information you asked for is not present in ArquiTips! Try to rephrase please!"})

    # Deduplicate matching_ids
    matching_ids = list(set(matching_ids))
    # Fetch and combine content of all matched documents as context 
    context = ""
    for doc_id in matching_ids:
        doc_content = azure_manager.get_cached_content(doc_id)
        print(doc_content)
        context += doc_content + "\n\n"

    # Step 2: Send the combined context and the query to your AI model
    response = ai_response(query, context)
    
    return jsonify({"response": response})

@app.route('/update', methods=['POST'])
def update():
    arquiTip = request.json.get('arquiTip')

    # Step 1: Download and extract content
    content = azure_manager.get_cached_content(arquiTip)
    if not content:
        title, content = azure_manager.download_and_extract_content_from_azure(arquiTip)  # Extract from Azure Repos
        azure_manager.cache_content_in_azure(content, arquiTip)  # Cache the content in Azure Blob Storage

    # Step 2: Update the index
    indexer.update_index(title, content, arquiTip)

    return jsonify({"status": "Updated successfully"})

@app.route('/update_all', methods=['POST'])
def update_all():
    mdFiles = azure_manager.list_all_md_files()
    for mdFile in mdFiles:
        print(mdFile)
        # Directly download and extract content from Azure Repos
        title, content = azure_manager.download_and_extract_content_from_azure(mdFile)
        
        # Cache the content in Azure Blob Storage
        azure_manager.cache_content(content, mdFile)
        
        # Update the index
        indexer.update_index(title, content, mdFile)  # Assuming mdFile is the title here, modify if needed

    return jsonify({"status": "All files updated successfully"})


# Set up your API key (better to use environment variables in production)
openai_api_key = os.environ.get('OPENAI_API_KEY')  # Make sure to keep this confidential
openai.api_key = openai_api_key
def ai_response(query, context):
    """
    Uses OpenAI's ChatGPT Turbo model to generate a response based on the provided query and context.
    """
    print("Query: " + query)
    print("Context: " + context)
    textAssist = "This is the information provided on the a document or more than one!\n\n Normally the line with ArquiTips will be the title of the document(s), the author will be after By and the Date after Published.\n\n Make sure to say reference the title(s) as well who published it/them in the answer!\n\nCan you analyze it/them and make sure to answer accordingly please. Don't answer with anything else beside the information that matters!"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": textAssist},
                {"role": "user", "content": context},
                {"role": "user", "content": query}
            ]
        )
        answer = response.choices[0].message['content'].strip()
        return answer
    except Exception as e:
        return f"Error: {str(e)}"

def download_and_extract_content(topic):
    file_path = f"data/{topic}.md"
    content = extractor.extract_from_md(file_path)
    return content

def initialize():
    mdFiles = ["teste1", "teste2", "teste3"] ##,"124BCAnalyzegroup"
    for mdFile in mdFiles:
        title, content = download_and_extract_content(mdFile)
        azure_manager.cache_content(content, mdFile)
        indexer.update_index(title, content, mdFile)

initialize()

if __name__ == '__main__':
    initialize()  # Initialize and index at startup
    app.run(debug=True)