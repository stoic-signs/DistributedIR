from pymongo import MongoClient
import pymongo


a = [1, 2, 3, 4, 5, 6]
b = [1, 3, 5, 7]
d = [3, 8, 9]
c = list(set(a) & set(b) & set(d))
c
b
a
d

client = MongoClient()
db = client.so_docs
docs = db.docs
doc = {
    "ques": "Why is there no SortedList in Java? SortedList",
    "url": "https://stackoverflow.com/questions/8725387/why-is-there-no-sortedlist-in-java"
}

doc_id = docs.insert_one(doc).inserted_id
doc_id

doc = db.docs.find_one({"_id": "1"})
type(doc)
for num in a[1:]:
    print(num)

num1 = {"q1": "hello", "q2": "world"}
num2 = {"q2": "meow", "q4": "bye"}

for key in num1.keys():
    print(key)

string = "how's everyone today?"
string.split()
