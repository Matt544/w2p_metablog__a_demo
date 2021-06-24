no_permission = "Not authorized to do that"

def user():
    # This function (incl. docstring) is taken directly from the web2py default controller
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    form=auth()
    return dict(form=form) 


@auth.requires_login()
@auth.requires_signature()
def account():
    """Sends articles authored by the logged in user to their account page, where
    the user can view, update or delete them, or create a new article"""
    requested_user = request.args(0, cast=int)
    articles = None
    user_is_requested_user = False

    if auth.user.id == requested_user:
        user_is_requested_user = True
        articles = db(db.article.account_user == requested_user).select()
    
    return dict(articles=articles, no_permission=no_permission, 
                user_is_requested_user=user_is_requested_user)


@auth.requires_login()
def create_article():
    """Returns a form for the user to create an article"""
    form = SQLFORM(db.article)
    db.article.account_user.default = auth.user.id 
    form.vars.author = auth.user.first_name # Note: This is an alternative way of
                                            # prepopulating the form, vs. the above
    if form.process().accepted:
        session.flash = 'New record entered'
        redirect(URL('users', 'account', args=auth.user.id, user_signature=True))
        last_reply = db().select(db.reply.ALL).last()
    elif form.errors:
        response.flash = 'Oops, did not work'
        reply_form_error = True

    return dict(form=form)

@auth.requires_login()
@auth.requires_signature()
def update_article():
    """Returns a form for the user to update an article they authored"""  
    record = db.article(request.args(0))
    form = None
    user_is_author = None

    if auth.user.id == record.account_user:
        user_is_author = True
        form = SQLFORM(db.article, record)
        if form.process().accepted:
            session.flash = 'Record updated'
            redirect(URL('users', 'account', args=auth.user.id, user_signature=True))
        elif form.errors:
            response.flash = 'Oops, update did not work'

    return dict(form=form, no_permission=no_permission, 
                user_is_author=user_is_author)


@auth.requires_login()
@auth.requires_signature()
def confirm_delete_article():
    """Asks for confirmation before deleting an article. Deletions accomplished by
    clicking on the returned URL
    """
    record = db.article(request.args(0))
    article_id = record.id
    user_is_author = None

    if auth.user.id == record.account_user:
        user_is_author = True

    return dict(article_id=article_id, record=record,
                no_permission=no_permission, user_is_author=user_is_author,
                delete=URL('users', 'delete_article', 
                           args=[article_id, 'delete'], user_signature=True),
                not_delete=URL('users', 'delete_article', 
                               args=[article_id, 'not_delete'], user_signature=True))


@auth.requires_login()
@auth.requires_signature()
def delete_article():
    """Either deletes the article or doesn't delete (depending on user input) 
    and either way redirects to user account
    """
    record = db.article(request.args(0))
    article_id = record.id
    user_is_author = None
    action = request.args(1)

    if auth.user.id == record.account_user and action == 'delete':
        user_is_author = True
        db(db.article.id == article_id).delete()
        session.flash = f'Article "{record.title}" deleted'
        redirect(URL('users', 'account', args=auth.user.id, user_signature=True))
    elif auth.user.id == record.account_user and action == 'not_delete':
        session.flash = 'Article not deleted. Close call!'
        redirect(URL('users', 'account', args=auth.user.id, user_signature=True))
    else:
        redirect(URL('users', 'confirm_delete_article', args=article_id, user_signature=True))
