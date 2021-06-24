from gluon.tools import Mail
from gluon.tools import Recaptcha2

mail = Mail()
mail.settings.server = 'logging' # To make this actually work, I used 'smtp.gmail.com:587'
mail.settings.sender = 'YOUR_ADDRESS@gmail.com'
mail.settings.login = 'YOUR_ADDRESS@gmail.com:YOUR_PASSWORD_OR_APP_PASSWORD'


def contact_form():
    """"Creates the contact form for contact_form.load"""
    form = SQLFORM.factory(
        Field('name', requires=IS_NOT_EMPTY()),
        Field('email', requires =[
            IS_EMAIL(error_message='invalid email!'), 
            IS_NOT_EMPTY()]
            ),
        Field('subject', requires=IS_NOT_EMPTY()),
        Field('message', requires=IS_NOT_EMPTY(), type='text'))
    form[0][4].insert(0, DIV(Recaptcha2(
        public_key='6Lesek4bAAAAAIgfe_l5XlVdn3eXsEyiVMb54SgJ', 
        private_key='6Lesek4bAAAAAGKGXoTYHBX8g5bEsL6Gozk2eAF2', 
        error_message='invalid captcha'), _class="mb-3"))
    
    if form.process().accepted:
        session.name = form.vars.name
        session.email = form.vars.email
        session.subject = form.vars.subject
        session.message = form.vars.message
    
        if mail:
            if mail.send(
                to=[form.vars.email, mail.settings.sender],
                subject=form.vars.subject,
                message= "Thanks for your email. The following message was sent:\n\n" + \
                         ">> " + form.vars.message
                ):
                response.flash = 'email sent sucessfully (read: logged to console only:)'
            else:
                response.flash = form.vars.name + ' fail to send email sorry! ' + \
                form.vars.email + form.vars.message
        else:
            response.flash = 'Unable to send the email : email parameters not defined'
    elif form.errors:
        response.flash='Email form has errors.'
            
    return dict(form=form)
