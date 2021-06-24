import blog_helpers

def index():
    """
    Sends the three most recent blog articles to the home page. Also returns a 
    function (tag_link_list) from the blog_helpers module that can be run from 
    the view to create a link list for the article's tags.
    """
    articles = blog_helpers.return_articles()
    return dict(articles=articles, tag_link_list=blog_helpers.tag_link_list)


def legalities():
    return dict()


def download():
    """
    Used to display the image associated with a blog article.
    """
    return response.download(request, db)
