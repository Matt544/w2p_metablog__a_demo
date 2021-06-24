import os

def read():
    """opens and reads the content of most files used to create w2p_metablog and display
    them in read.html"""
    requested_files = request.vars
    requested_path = requested_files["file"][0]
    path = os.path.join(request.folder, requested_path)
    requested_language = requested_files["file"][1]
    
    no_permission = "Sorry, the requeseted file is Super Secret or doesn't exist"
    permission = None
    the_code = None
  
    permitted_paths = [
        'models/db.py',
        'models/tables.py',
        'views/base.html',
        'views/show_code/read.html',
        'views/show_code/read.html',
        'views/files_list/files_list.load',
        'views/home/index.html',
        'views/home/legalities.html',
        'views/contact_form/contact_form.load',
        'views/resource/article.html',
        'views/blog/archive.html',
        'views/article_card_short.html',
        'views/resource/reply_form.load',
        'views/reply.html',
        'views/resource/nested_reply_form.load',
        'views/nested_reply.html',
        'views/blog/category.html',
        'views/blog/tag.html',
        'views/users/account.html',
        'views/users/user.html',
        'views/users/create_article.html',
        'views/users/update_article.html',
        'views/users/confirm_delete_article.html',
        'controllers/show_code.py',
        'controllers/files_list.py',
        'controllers/home.py',
        'controllers/blog.py',
        'controllers/contact_form.py',
        'controllers/resource.py',
        'controllers/users.py',
        'modules/blog_helpers.py',
        'static/css/custom.css',
        ]
    
    if requested_path in permitted_paths:
        permission = True
        with open(path, "r", encoding='utf-8') as open_file:
            the_code = open_file.read()
  
    return dict(requested_path=requested_path, the_code=the_code, 
                requested_language=requested_language, no_permission=no_permission, 
                permission=permission)
