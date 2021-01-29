def render_template(template, **kwargs):
    ''' renders a Jinja template into HTML '''
    # check if template exists
    if not os.path.exists(template):
        print('No template file present: %s' % template)
        sys.exit()

    import jinja2
    templateLoader = jinja2.FileSystemLoader(searchpath="/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    templ = templateEnv.get_template(template)
    return templ.render(**kwargs)
#------------------------------------------------------------------------------------------------
def send_email(to, sender='MyCompanyName<noreply@mycompany.com>', cc=None, bcc=None, subject=None, body=None):
    ''' sends email using a Jinja HTML template '''
    import smtplib
    # Import the email modules
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.header import Header
    from email.utils import formataddr

    # convert TO into list if string
    if type(to) is not list:
        to = to.split()

    to_list = to + [cc] + [bcc]
    to_list = filter(None, to_list) # remove null emails

    msg = MIMEMultipart('alternative')
    msg['From']    = sender
    msg['Subject'] = subject
    msg['To']      = ','.join(to)
    msg['Cc']      = cc
    msg['Bcc']     = bcc
    msg.attach(MIMEText(body, 'html'))
    server = smtplib.SMTP("127.0.0.1") # or your smtp server
    try:
        log.info('sending email xxx')
        server.sendmail(sender, to_list, msg.as_string())
    except Exception as e:
        log.error('Error sending email')
        log.exception(str(e))
    finally:
        server.quit()
#------------------------------------------------------------------------------------------------

# MAIN

item1 = 'kryptonite'
item2 = 'green clothing'

# generate HTML from template
html = render_template('default.j2', vars=locals())

to_list = ['spiderman@marvel.com', 'punisher@marvel.com']
sender = 'superman<superman@dc.com>'
cc = 'greenlantern@dc.com'
bcc = 'invisible_man@dc.com'
subject = 'Meet me for a beatdown'

# send email to a list of email addresses
send_email(to_list, sender, cc, bcc, subject, html.encode("utf8"))
