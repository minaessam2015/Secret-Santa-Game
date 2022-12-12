
class User(object):
    def __init__(self,name=None,mail=None,wishes=None):
        self.name = name
        self.mail = mail
        if wishes is not None:
            self.wishes = [v.strip() for v in wishes]
        else:
            self.wishes = wishes
    def __repr__(self):
        return "Name: {0}\nMail: {1}\nWishes: {2}".format(\
            self.name,self.mail,self.wishes)
    
    def __str__(self):
        return self.__repr__()
    
def get_users(filename: str):
    """
    Return a ditc of the information from users file
    """
    users = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for i,a_contact in enumerate(contacts_file):
            if i == 0 or (a_contact.strip() == ''):
                # skip the first line
                continue
            #Name,UserName,Mail,Password,OldPassword
            fields = a_contact.split(',')
            user = User(name=fields[0],mail=fields[1].strip(),wishes=fields[2:])
            users.append(user)
            
    return users

def save_users(filename: str,users: list):
    """
    Save the users into a csv format
    """

    with open(filename,mode='w+') as f:
        f.write('Name,Mail,Wishes\n')
        for u in users: 
            message = ""
            for v in u.wishes:
                message += v+','
            f.write(f'{u.name},{u.mail},{message[:-1]}'+'\n')