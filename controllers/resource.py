from gluon.contrib.markmin.markmin2html import markmin2html
from gluon.tools import Recaptcha2

# The variable "extra" (below) is required for syntax highlighting in articles, 
# replies, nested replies, and previews

extra = {
    'code_cpp':lambda text: CODE(text,language='cpp').xml(),
    'code_java':lambda text: CODE(text,language='java').xml(),
    'code_python':lambda text: CODE(text,language='python').xml(),
    'code_html':lambda text: CODE(text,language='html').xml()
    }


def article():
    """
    Sends the article clicked in a connecting link (e.g. from the blog page) to 
    its display page. Also returns replies that were authored by Admin or by the 
    logged in user. 
    """
    article = db.article(slug=request.args(0))
    session.article_id = article.id
    
    if auth.is_logged_in(): 
        replies = db(
            (db.reply.article_id==article.id) 
            & ((db.reply.account_user==1) | (db.reply.account_user==auth.user.id))
            ).select(orderby=~db.reply.id) 
    else:
        replies = db(
            (db.reply.article_id==article.id) 
            & (db.reply.account_user==1)).select(orderby=~db.reply.id)

    return dict(article=article, article_id=session.article_id, 
                replies=replies, extra=extra)


def reply_form():
    """
    A LOAD component that (1) displays the reply form, and (2) displays the
    reply submitted in the form. 
    
    Upon submission of a reply, the variable "last_reply" is changed from None 
    to the db row of the last-submitted reply for its display. 
    """
    form = SQLFORM(db.reply)
    last_reply = None
    logged_in = None
    slug = request.args(0)

    if auth.is_logged_in():
        logged_in = True
        form.append(Recaptcha2(
            public_key='6Lesek4bAAAAAIgfe_l5XlVdn3eXsEyiVMb54SgJ', 
            private_key='6Lesek4bAAAAAGKGXoTYHBX8g5bEsL6Gozk2eAF2', 
            label='Verify captcha:',
            error_message='invalid captcha'))
        db.reply.article_id.default = session.article_id
        db.reply.account_user.default = auth.user.id
        
        if form.process().accepted:
            response.flash = 'Your reply was accepted.'
            last_reply = db().select(db.reply.ALL).last()
        elif form.errors:
            response.flash = 'There was an error.'
    
    return dict(form=form, last_reply=last_reply, extra=extra,
                logged_in=logged_in, slug=slug)


def nested_reply_form():
    """
    A LOAD component that (1) displays the nested_reply form, and (2) displays 
    the nested_reply submitted in the form. 

    The variable "last_nested_reply" changes from None to the db row of 
    the last-submitted nested_reply for its display.
    """
    form = SQLFORM(db.nested_reply, formstyle='bootstrap4_stacked')
    last_nested_reply = None
    logged_in = None
    slug = request.args(0) # This is needed to redirect the user to 
                           # the page they were on before logging in.
    reply_author = None
    reply_id = request.vars.reply_id # This is needed to assign the nested 
                                     # reply a reply id, so that it will desplay 
                                     # under relevant.Also used for the form name.
    reply_container_id = request.vars.reply_container_id 
        # This is used as an anchor to take the user back to the part of the page 
        # with the commment they wanted to reply to, after they register or sign in. 

    if auth.is_logged_in():
        logged_in = True
        db.nested_reply.reply_id.default = reply_id 
        db.nested_reply.article_id.default = session.article_id 
        db.nested_reply.account_user.default = auth.user.id
        reply_author = request.vars.reply_author

        if form.process(formname=reply_id).accepted:
            response.flash = 'Your reply was accepted.'
            last_nested_reply = db().select(db.nested_reply.ALL).last()
        elif form.errors:
            response.flash = 'There was an error.'

    return dict(form=form, reply_author=reply_author, 
                last_nested_reply=last_nested_reply, logged_in=logged_in, 
                slug=slug, reply_id=reply_id,
                reply_container_id=reply_container_id, extra=extra)


def echo():
    """This powers the preview of replies."""
    x = request.vars.body
    y = ''.join(x)
    return XML(markmin2html(y, extra=extra), sanitize=True, 
               allowed_attributes={'a':['href', 'title'], 'img':['src', 'alt'], 
               'blockquote':['type'], 'span':['style']})


def download():
    """Used to display the image associated with a blog article."""
    return response.download(request, db)
