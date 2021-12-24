from urllib.request import urlopen
import json

class BookApi:
    def __init__(self, query_type, query):
        self.url = "https://www.googleapis.com/books/v1/volumes?q="
        self.query_type = query_type
        self.query = query

    def find(self):
        result = urlopen(self.url+self.query_type+":"+self.query)
        res = json.load(result)['items']
        final = []
        for item in res:
            temp_book = ""
            if("books" in item["kind"]):
                temp_book = Book(item["volumeInfo"]["title"], author=item["volumeInfo"]["authors"])
                final.append(temp_book)
        for book in final:
            print(book)

        return temp_book


class Book:
    def __init__(self, title, isbn="", author=""):
        self.title = title
        self.isbn = isbn
        self.author = author
        self.link = ""
        self.description = ""

    def __str__(self):
        return self.title

    def getTitle(self):
        return self.title

if __name__ == "__main__":
    api = BookApi("subject", "psychology")
    api.find()



