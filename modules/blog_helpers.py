from gluon import * 

def return_articles():
    """Returns to the calling function (in either blog.py or home.py) all 
    articles authored by Admin or a logged in user (if any)
    """
    db = current.db
    auth = current.auth

    if auth.is_logged_in():
        articles = db(
            ((db.article.account_user==1) | (db.article.account_user==auth.user.id))
            ).select(orderby=~db.article.id)
    else:
        articles = db(db.article.account_user==1).select(orderby=~db.article.id)
        
    return articles 


def tag_link_list(article_tags):
    """Creates links for the list of tags applicable to a posted article"""
    tag_list = []
    for tag in article_tags:
        link = str(A(tag.name, _href=URL(c='blog', f='tag', args=tag.slug)))
        tag_list.append(link)
    tag_links = XML(', '.join(tag_list))
    return tag_links
