import urllib.request
import json
import textwrap

#From <script src="https://gist.github.com/AO8/faa3f52d3d5eac63820cfa7ec2b24aa7.js"></script>
#Goal is to convert into 
# Input ISBN from main
# Save Title, Summary, Author, Count, Language

def getBookInfo(ISBN): 

    base_api_link = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
    user_input = ISBN

    with urllib.request.urlopen(base_api_link + user_input) as f:
        text = f.read()

    decoded_text = text.decode("utf-8")
    obj = json.loads(decoded_text) # deserializes decoded_text to a Python object
    volume_info = obj["items"][0] 
    authors = obj["items"][0]["volumeInfo"]["authors"]
    title = volume_info["volumeInfo"]["title"]
    summary = textwrap.fill(volume_info["searchInfo"]["textSnippet"], width=65)
    pages = volume_info["volumeInfo"]["pageCount"]

    return title,authors,pages,summary

    # displays title, summary, author, domain, page count and language
    #print("\nTitle:", volume_info["volumeInfo"]["title"])
    #print("\nSummary:\n")
    #print(textwrap.fill(volume_info["searchInfo"]["textSnippet"], width=65))
    #print("\nAuthor(s):", ",".join(authors))
    #print("\nPublic Domain:", volume_info["accessInfo"]["publicDomain"])
    #print("\nPage count:", volume_info["volumeInfo"]["pageCount"])
    #print("\nLanguage:", volume_info["volumeInfo"]["language"])
    #print("\n***")

