# Creating tables for blog articles, tags, categories and comments

db.define_table('tag',
                Field('name'),
                Field('slug', type='string'),
                format='%(name)s')

db.tag.slug.requires = [IS_NOT_IN_DB(db, db.tag.slug), 
                        IS_NOT_EMPTY(), 
                        IS_SLUG(maxlen=80, 
                                check=False, 
                                error_message='must be slug')]


db.define_table('category',
                Field('name'),
                Field('slug', type='string'),
                format='%(name)s')

db.category.slug.requires = [IS_NOT_IN_DB(db, db.category.slug), 
                             IS_NOT_EMPTY(), 
                             IS_SLUG(maxlen=80, 
                                     check=False, 
                                     error_message='must be slug')]


db.define_table('article',
                Field('author', type='string'),
                Field('account_user', type='integer'),
                Field('title', type='string'),
                Field('subtitle', type='string'),
                Field('slug', type='string'),
                Field('image', 'upload'),
                Field('summary', type='text'),
                Field('body', type='text'),
                Field('categories', 'list:reference category'),
                Field('tags', 'list:reference tag'),
                Field('created_on', 'datetime', default=request.now, 
                      update=request.now),
               )

db.article.author.requires = IS_NOT_EMPTY()
db.article.title.requires = [IS_NOT_IN_DB(db, db.article.title), IS_NOT_EMPTY()]
db.article.slug.requires = [IS_NOT_IN_DB(db, db.article.slug), 
                            IS_NOT_EMPTY(), 
                            IS_SLUG(maxlen=80, 
                                    check=False, 
                                    error_message='must be slug')]
db.article.summary.requires = IS_LENGTH(1000)
db.article.body.requires = IS_LENGTH(4000)


db.article.id.readable = False
db.article.account_user.readable = db.article.account_user.writable = False
db.article.created_on.writable = False
db.article.author.writable = False
db.article.author.readable = True 


db.define_table('reply',
                Field('article_id', 'reference article'),
                Field('account_user', type='integer'),
                Field('author', type='string'),
                Field('email'),
                Field('body', type='text'),
                Field('created_on', 'datetime', default=request.now),
               )

db.reply.article_id.requires = IS_IN_DB(db, db.article.id)
db.reply.account_user.readable = db.reply.account_user.writable = False
db.reply.author.requires = IS_NOT_EMPTY()
db.reply.email.requires = IS_EMPTY_OR(IS_EMAIL())
db.reply.body.requires = [IS_NOT_EMPTY(), IS_LENGTH(1000)]

db.reply.article_id.writable = db.reply.article_id.readable = False
db.reply.created_on.writable = False


db.define_table('nested_reply',
                Field('reply_id', 'reference reply'),
                Field('account_user', type='integer'),
                Field('article_id', 'reference article'),
                Field('author', type='string'),
                Field('email'),
                Field('body', type='text'),
                Field('created_on', 'datetime', default=request.now),
               )

db.nested_reply.reply_id.requires = IS_IN_DB(db, db.reply.id)
db.nested_reply.account_user.readable \
    = db.nested_reply.account_user.writable = False
db.nested_reply.author.requires = IS_NOT_EMPTY()
db.nested_reply.email.requires = IS_EMPTY_OR(IS_EMAIL())
db.nested_reply.body.requires = [IS_NOT_EMPTY(), IS_LENGTH(1000)]

db.nested_reply.reply_id.writable = db.nested_reply.reply_id.readable = False
db.nested_reply.article_id.writable = db.reply.article_id.readable = False
db.nested_reply.created_on.writable = False
