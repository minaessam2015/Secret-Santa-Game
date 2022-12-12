
import os
from User import User,get_users
import numpy as np

def generate_santa_file(input_file: str,output_file='./santa.txt'):

    users = get_users(input_file)
    if len(users)%2 != 0:
        # Circular matching
        randomized = np.arange(len(users)+1)
        randomized[-1] = randomized[0]
    else:
        randomized = np.arange(len(users))
    np.random.shuffle(randomized)
    print(randomized)

    with open(output_file,'w+') as f:
        f.write('Name,Mail,Target,Target_wishes\n')
        for index in range(len(randomized)-1):
            user = users[randomized[index]]
            message = ""
            for v in users[randomized[index+1]].wishes:
                message += v+','
            f.write("{0},{1},{2},{3}\n".\
                format(user.name,user.mail,users[randomized[index+1]].name,message[:-1]))



if __name__ == '__main__':
    import sys
    assert len(sys.argv) >= 2, "Expected to have a path for the users file"
    file = sys.argv[1]
    if len(sys.argv) == 3:
        out_file = sys.argv[2]

    generate_santa_file(file)
