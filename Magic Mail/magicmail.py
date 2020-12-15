import smtplib, ssl
from flask import Flask, render_template, request
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)

PEOPLE_FOLDER = os.path.join('static', 'people_photo')
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

data = []

def login_check(email_id, password):
    data.append(email_id)
    data.append(password)
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login(email_id, password)

def sandEmail(body, subject, reciever, attachment):
    sender = data[0]
    password = data[1]

    
    # get the password in the gmail (manage your google account, click on the avatar on the right)
    # then go to security (right) and app password (center)
    # insert the password and then choose mail and this computer and then generate
    # copy the password generated here
    # put the email of the receiver here
    
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = reciever
    message['Subject'] = subject
    
    message.attach(MIMEText(body, 'plain'))

    if attachment:
        pdfname = attachment
        # open the file in binary
        binary_pdf = open(pdfname, 'rb')
        
        payload = MIMEBase('application', 'octate-stream', Name=pdfname)
        # payload = MIMEBase('application', 'pdf', Name=pdfname)
        payload.set_payload((binary_pdf).read())
        
        # encoding the binary into base64
        encoders.encode_base64(payload)
        
        # add header with pdf name
        payload.add_header('Content-Decomposition', 'attachment', filename=pdfname)
        message.attach(payload)

        session = smtplib.SMTP('smtp.gmail.com', 587)
    
        #enable security
        session.starttls()
        
        #login with mail_id and password
        session.login(sender, password)
        
        text = message.as_string()
        session.sendmail(sender, reciever, text)
        session.quit()
    else:
        #use gmail with port
        session = smtplib.SMTP('smtp.gmail.com', 587)
        
        #enable security
        session.starttls()
        
        #login with mail_id and password
        session.login(sender, password)
        
        text = message.as_string()
        session.sendmail(sender, reciever, text)
        session.quit()

@app.route('/', methods = ['GET', 'POST'])
def login_page():
    if request.method == "POST":
        myMail = request.form
        email_id = str(myMail['email'])
        password = str(myMail['password'])
        try:
            login_check(email_id, password)
            return render_template('message.html')
        except Exception as error:
            return render_template('error.html', error_detect = error)
    return render_template('login.html')
    
@app.route('/mail', methods = ['GET', 'POST'])
def main_fuction():
    if request.method == "POST":
        myDict = request.form
        reciever = str(myDict['reciever'])
        subject = str(myDict['subject'])
        body = str(myDict['body'])
        attachment = str(myDict['attachment'])
        try: 
            sandEmail(body, subject, reciever, attachment)
            return render_template('submit.html', mailid = reciever)
        except Exception as e:
            return render_template("error.html", error_detect = e)
    return render_template("message.html")

@app.route('/contact', methods = ['GET', 'POST'])
def contact():
	if request.method == 'POST':
		mycontact = request.form
		firstname = str(mycontact['firstname'])
		lastname = str(mycontact['lastname'])
		country = str(mycontact['country'])
		subject = str(mycontact['subject'])
		return render_template('contact_save.html', firstname = firstname, lastname = lastname, country = country, message = subject)
	full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'img.png')
	return render_template('contact.html', user_image = full_filename)

@app.route('/about', methods = ['GET', 'POST'])
def about():
	team1 = os.path.join(app.config['UPLOAD_FOLDER'], 'team1.png')
	team2 = os.path.join(app.config['UPLOAD_FOLDER'], 'team2.png')
	team3 = os.path.join(app.config['UPLOAD_FOLDER'], 'team3.png')
	return render_template('about.html', team1 = team1, team2 = team2, team3 = team3)

@app.route('/team-contact', methods = ['GET', 'POST'])
def team_contact():
	full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'img.png')
	return render_template('contact.html', user_image = full_filename)


if __name__ == "__main__":
    app.run(debug=True)
