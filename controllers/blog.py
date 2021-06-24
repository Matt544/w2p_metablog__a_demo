import blog_helpers

def archive():
    """Sends blog articles to the blog archive page. Only articles 
    authored by Admin or the logged in user will display.
    """   
    articles = blog_helpers.return_articles() 
    return dict(articles=articles, tag_link_list=blog_helpers.tag_link_list)


def tag():
    """Sends articles with the requested tag for display."""
    tag_record = db.tag(slug=request.args(0)) 
    # tagged_articles = db(db.article.tags.contains(tag_record.id)).select()  (: would be a simpler way of defining tagged_articles, in a simpler context ;)

    if auth.is_logged_in():
        tagged_articles = db(
            (db.article.tags.contains(tag_record.id)) 
            & ((db.article.account_user==1) | (db.article.account_user==auth.user.id))
            ).select()
    else:
        tagged_articles = db(
            (db.article.tags.contains(tag_record.id)) 
            & (db.article.account_user==1)).select()
    
    return dict(tag_record=tag_record, tagged_articles=tagged_articles, 
                tag_link_list=blog_helpers.tag_link_list)


def category():
    """Sends articles with the requested category for display."""
    category_record = db.category(slug=request.args(0))
    # category_articles = db(db.article.categories.contains(category_record.id)).select() (: would be a simpler way of defining category_articles, in a simpler context ;)

    if auth.is_logged_in():
        category_articles = db(
            (db.article.categories.contains(category_record.id))
            & ((db.article.account_user==1) | (db.article.account_user==auth.user.id))
            ).select()
    else:
        category_articles = db(
            (db.article.categories.contains(category_record.id))
            & (db.article.account_user==1)).select()
    
    return dict(category_record=category_record, 
                category_articles=category_articles, 
                tag_link_list=blog_helpers.tag_link_list)


def download():
    """Used display the image associated with a blog article."""
    return response.download(request, db)
