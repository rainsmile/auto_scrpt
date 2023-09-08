with open('email.txt', 'r') as f:
    goole = f.readlines()
    for g in goole:
        email_ = g.split('----')[0]
        pwd_ = g.split('----')[1]
        f_email_ = g.split('----')[2]
        print(email_, pwd_, f_email_)