from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def test_create_magazine():
    magazine = Magazine.create("Science Daily", "Science")
    assert magazine.name == "Science Daily"
    assert magazine.category == "Science"
    assert isinstance(magazine.id, int)

def test_find_magazine_by_id():
    magazine = Magazine.create("Tech Times", "Technology")
    found = Magazine.find_by_id(magazine.id)
    assert found.name == "Tech Times"
    assert found.category == "Technology"

def test_articles_method():
    author = Author.create("Tech Author")
    magazine = Magazine.create("Tech World", "Technology")
    author.add_article(magazine, "AI in 2025")
    author.add_article(magazine, "Blockchain Trends")

    articles = magazine.articles()
    assert len(articles) >= 2
    titles = [article.title for article in articles]
    assert "AI in 2025" in titles
    assert "Blockchain Trends" in titles

def test_contributors_method():
    mag = Magazine.create("Writers Weekly", "Writing")
    author1 = Author.create("Alice Writer")
    author2 = Author.create("Bob Scribe")

    author1.add_article(mag, "Writing Tips")
    author2.add_article(mag, "Editing 101")

    contributors = mag.contributors()
    names = [author.name for author in contributors]
    assert "Alice Writer" in names
    assert "Bob Scribe" in names

def test_article_titles_method():
    author = Author.create("Journalist Jane")
    mag = Magazine.create("Daily News", "News")
    author.add_article(mag, "Politics Today")
    author.add_article(mag, "World Events")

    titles = mag.article_titles()
    assert "Politics Today" in titles
    assert "World Events" in titles

def test_contributing_authors_method():
    mag = Magazine.create("Heavy Contributor Mag", "General")
    author = Author.create("Prolific Author")

    author.add_article(mag, "Article 1")
    author.add_article(mag, "Article 2")
    author.add_article(mag, "Article 3")

    heavy_contributors = mag.contributing_authors()
    names = [a.name for a in heavy_contributors]
    assert "Prolific Author" in names
