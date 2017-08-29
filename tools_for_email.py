import smtplib, os.path, traceback
import mimetypes

from email.mime.multipart import MIMEMultipart

from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

from email import encoders

# This function sends a gmail message with attachments, without needing to open gmail. Hence it is useful for setting up automated emails that run after a task is complete.
# Inputs: gmail address address, gmail password (either the actual password, OR a text file address where it is stored), array of recipient addresses, simple message string, array of attached file addresses
# Currently has minimal provision for body of the email: it just puts the message in the subject header
# Note that the gmail address needs to be enabled to send messages in this way, with "allowing access to less secure apps"
# If attempting to send from gmail without this setting altered, an error message will be returned
# Because security settings need to be altered within gmail, it is also advisable that this function be used for purpose-made email addresses, not everyday gmail addresses
# Returns True if successful in sending the email, False if not successful. 
# Example call: email_result = tools_for_email.send_gmail_withattachments('johnsmith@gmail.com', 'E:/secret.txt', ['myfriend@gmail.com', 'myotherfriend@gmail.com'], 'Hi guys', ['E:/file1.xls', 'F:/file2.jpg'])
def send_gmail_withattachments(fromaddr='', password_pointer='', toaddrs=[], plainmsg = '', files = []):
    result = False
    try:
        username = fromaddr
        print("\nSending email from %s..." %fromaddr)
        if(os.path.isfile(password_pointer) == True):
            password = open(password_pointer, 'r', encoding='utf8').readline()
        else:
            password = password_pointer

        COMMASPACE = ', '

        # Create the container (outer) email message.
        msg = MIMEMultipart()
        msg['Subject'] = plainmsg
        # me == the sender's email address
        # family = the list of all recipients' email addresses
        msg['From'] = fromaddr
        msg['To'] = COMMASPACE.join(toaddrs)
        msg.preamble = plainmsg

        for file in files:
            
            ctype, encoding = mimetypes.guess_type(file)
            if ctype is None or encoding is not None:
                ctype = "application/octet-stream"

            maintype, subtype = ctype.split("/", 1)

            print("Attaching file of type: ", maintype, ", subtype: ", subtype)

            if maintype == "text":
                fp = open(file)
                # Note: we should handle calculating the charset
                attachment = MIMEText(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == "image":
                fp = open(file, "rb")
                attachment = MIMEImage(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == "audio":
                fp = open(file, "rb")
                attachment = MIMEAudio(fp.read(), _subtype=subtype)
                fp.close()
            else:
                fp = open(file, "rb")
                attachment = MIMEBase(maintype, subtype)
                attachment.set_payload(fp.read())
                fp.close()
                encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", "attachment", filename=file)
            msg.attach(attachment)

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username,password)
        server.send_message(msg)
        server.quit()
        result = True
        print("Email sent successfully from %s" %(fromaddr))
        return(result)
    except:
        traceback.print_exc()
        print("Error encountered sending email from %s" %(fromaddr))
        return(result)
