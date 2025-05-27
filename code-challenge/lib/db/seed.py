from lib.models.author import Author
from lib.models.magazine import Magazine

a1 = Author.create("Alice Walker")
a2 = Author.create("George Orwell")

m1 = Magazine.create("Tech Times", "Technology")
m2 = Magazine.create("Nature Weekly", "Science")

a1.add_article(m1, "The Future of AI")
a1.add_article(m2, "Eco Farming Tips")
a2.add_article(m1, "Machine Learning Basics")
