import pymysql
import sys
import os

conn  = pymysql.connect(host='localhost', user='host', password='paaaword',db='project',charset='UTF8')
select_curs = conn.cursor()

while(1):
    print('\n\n-------------------------------------------------------------------')
    print('\t\t\tCREATE ACCOUNT')
    print('-------------------------------------------------------------------')

    user_name = input('Please input User name: ')
    user_id   = input('Please input user ID: ')
    user_pw   = input('Please input password: ')
    
    print('-------------------------------------------------------------------\n')
    print('User Name: '+user_name)
    print('User ID: '+user_id)
    print('User Password: '+user_pw)
    
    print('\n-------------------------------------------------------------------')
    print('if you want exit insert q')
    option = input("If above info is Coorect insert 'Y' else insert 'N': ")
    
    if option is 'Y' or option is 'y':
        selectQuery = 'SELECT * FROM users WHERE ID = %s'
        select_curs.execute(selectQuery, user_id)
        check_id = select_curs.fetchone()
        if check_id is None:
            break
        else:
            os.system('clear')
            print('This ID is already used Please try again')
            pass
    
    elif option is 'q' or option is 'Q':
        print('Bye!')
        sys.exit()

    elif option is 'N' or option is 'n':
        os.system('clear')
        print('Insert Info again!!')
        pass

    else:
        print("Insert only 'y' or 'n'")
        sys.exit()

print('Creating Account with under Info')
print('User Name: '+user_name)
print('User ID: '+user_id)
print('User Password: '+user_pw)

insertQuery = 'INSERT INTO users VALUES(%s, %s, %s)'
insert_curs  = conn.cursor()

insert_curs.execute(insertQuery, (user_id, user_name, user_pw))

insert_curs.close()
select_curs.close()
conn.commit()
conn.close()

