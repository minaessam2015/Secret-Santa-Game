import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from generator_config import config
from User import User, get_users
import socket
from generate_pairs import generate_santa_file

MY_ADDRESS = config['sender_mail']
PASSWORD = config['sender_pass']
INTIXEL_MAIL_SERVER = config['server']
INTIXEL_PORT = config['port']


def fill_mail_template(user: User):
    """
    Returns a the template for a mail after filling the data.
    """
    # print(user)
    if user.wishes == ["Nothing"]:
        wished_message = "has no specific wishes. They are open for anything!"
    else:
        wished_message = "prefers the following wishes\n"
        for wish in user.wishes:
            wished_message += wish+"\n"
    # msg = """Dear {0},\n\nOnce again, 2022 was an incredible year that must have impacted us in many ways. We would like to make this last week more fun!. We are going to play secret santa together!. You are given a friend that you need to buy a nice souvenir to be a nice memory at the end of the year. The only rule that the budget for the present is no more than 150 LE. Get creative! and do not tell anyone who your pair is.\n\nYou are paired with: {1}\n\nNote:\nYour partner {2}Regards,\nSecret Santa"""\
    #     .format(user.name,user.target,wished_message)
    # print(msg)
    msg = get_message_template().format(user.name,user.target,wished_message)
    return msg

def get_message_template(file_path: str="./template_message.txt")->str:

    if not os.path.exists(file_path):
        raise ValueError(f"Provided path does not exist for the message template {file_path}")
    with open(file_path,"r") as f:
        message = f.read(-1)
    return message

def get_data(file: str):
    users = []
    with open(file, mode='r', encoding='utf-8') as contacts_file:
        for i,a_contact in enumerate(contacts_file):
            if i == 0 or (a_contact.strip() == ''):
                # skip the first line
                continue
            #Name,UserName,Mail,Password,OldPassword
            fields = a_contact.strip().split(',')
            # print("fields",fields)
            user = User(name=fields[0],mail=fields[1])
            user.target = fields[2]
            user.wishes = fields[3:]
            users.append(user)
    return users

def send(file: str):
    users = get_data(file) # read contacts
    print("Users",users)
    # set up the SMTP server
    print(INTIXEL_MAIL_SERVER,INTIXEL_PORT)

    s = smtplib.SMTP(host=INTIXEL_MAIL_SERVER, port=INTIXEL_PORT)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    # For each contact, send the email:
    for user in users:
        print(user.name,user.target)
        msg = MIMEMultipart()       # create a message

        # add in the actual person name to the message template
        message = fill_mail_template(user)

        # Prints out the message body for our sake
        #print(message)

        # setup the parameters of the message
        msg['From']=MY_ADDRESS
        msg['To']=user.mail
        msg['Subject']="See your secret santa pair"
        
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        
        # send the message via the server set up earlier.
        # s.send_message(msg)
        del msg
        
    # Terminate the SMTP session and close the connection
    s.quit()

def send_gmail(file: str,debug_folder=None):
    users = get_data(file) # read contacts
    print("Users",users)
    # set up the SMTP server
    print(INTIXEL_MAIL_SERVER,INTIXEL_PORT)
    
    # s = smtplib.SMTP(host=INTIXEL_MAIL_SERVER, port=INTIXEL_PORT)
    # s.starttls()
    # s.login(MY_ADDRESS, PASSWORD)
    context = ssl.create_default_context()
    

    # For each contact, send the email:
    with smtplib.SMTP_SSL(INTIXEL_MAIL_SERVER, INTIXEL_PORT, context=context) as server:
        print(MY_ADDRESS, PASSWORD)
        server.login(MY_ADDRESS, PASSWORD)
        for user in users:
            
            
            print(user.name,user.target)

            # add in the actual person name to the message template
            message = fill_mail_template(user)

            # Prints out the message body for our sake
            #print(message)
            msg = MIMEMultipart()       # create a message

            # add in the actual person name to the message template
            message = fill_mail_template(user)

            # Prints out the message body for our sake
            #print(message)

            # setup the parameters of the message
            msg['From']=MY_ADDRESS
            msg['To']=user.mail
            msg['Subject']="See your secret santa pair"
            
            # add in the message body
            msg.attach(MIMEText(message, 'plain'))

            server.sendmail(MY_ADDRESS, user.mail, msg.as_string())
            if debug_folder is not None:
                with open(os.path.join(debug_folder,user.name+".txt"),'w+') as f:
                    f.write(message)

            del msg
            
        

     
if __name__ == '__main__':
    import sys
    import os
    from shutil import rmtree

    # file = sys.argv[1]
    debug_folder = "mails_txt"
    if  os.path.exists(debug_folder):
        rmtree(debug_folder)
    os.mkdir(debug_folder)
    output_file = "./santa_pairs.txt"
    generate_santa_file("./users",output_file=output_file)
    send_gmail(output_file,debug_folder)