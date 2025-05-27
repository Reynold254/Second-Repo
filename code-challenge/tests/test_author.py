from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def test_create_author():
    author = Author.create("Test Author")
    assert author.name == "Test Author"
    assert isinstance(author.id, int)

def test_find_author_by_id():
    author = Author.create("Another Author")
    found = Author.find_by_id(author.id)
    assert found.name == "Another Author"

def test_add_article_and_articles_method():
    author = Author.create("Article Author")
    magazine = Magazine.create("Tech Monthly", "Technology")
    author.add_article(magazine, "The Future of AI")
    
    articles = author.articles()
    assert len(articles) >= 1
    assert any(article.title == "The Future of AI" for article in articles)

def test_magazines_method():
    author = Author.create("Multi Magazine Author")
    mag1 = Magazine.create("Nature Weekly", "Science")
    mag2 = Magazine.create("Health Today", "Health")
    
    author.add_article(mag1, "Climate Change")
    author.add_article(mag2, "Mental Health Awareness")

    magazines = author.magazines()
    mag_names = [mag.name for mag in magazines]
    assert "Nature Weekly" in mag_names
    assert "Health Today" in mag_names

def test_topic_areas():
    author = Author.create("Topic Tester")
    mag1 = Magazine.create("Physics World", "Science")
    mag2 = Magazine.create("Art Digest", "Art")
    
    author.add_article(mag1, "Quantum Mechanics")
    author.add_article(mag2, "Impressionist Art")

    topics = author.topic_areas()
    assert "Science" in topics
    assert "Art" in topics
