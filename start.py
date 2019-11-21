import sys
import subprocess



print('-------------------------------------------------------------------')
print('\t\t\t WELLCOME TO FACE RECOGNIZER')
print('-------------------------------------------------------------------')
print('------------------------OPTION LIST--------------------------------')
print('1. Create Account     2. Face Collecting      3.Face Recognizing')

try:
    option_num = int(input('\nSelect Option (Only use number): '))
    if option_num > 0 and option_num < 4:
    
        if option_num is 1:
            subprocess.call(['python','create_account.py'])
    
        elif option_num is 2:
            subprocess.call(['python','face_collect.py'])
    
        elif option_num is 3:
            subprocess.call(['python','face_recognize.py'])
    else:
        print('Please only input number (1, 2, 3)')
        sys.exit()

except ValueError:
    print('Only insert number!!')
    sys.exit()
