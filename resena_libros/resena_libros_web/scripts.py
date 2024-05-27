from django.contrib.auth.hashers import check_password

# Esto se utilizó para trabajar JSON y loaddata

def imprimir():
    hashed_password = 'pbkdf2_sha256$216000$Hq9lL8dcZ8lO$eJbDjH2Dz/4lU/fL+zfF6N4UGJtEpB3SptCW30PybSo='
    password_to_check = 'Abc123#'

    is_correct = check_password(password_to_check, hashed_password)
    print(is_correct)
