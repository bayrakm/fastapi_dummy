from passlib.context import CryptContext # to hash the password

# this file is for keeping small functionalities

# here we set the crypto algorithm for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"]) # Setting up crypto methods

def hash(password: str):
    return pwd_context.hash(password)

# new functions to hash pasword to compare loging password
def verify(plain_password, hashed_password):

    return pwd_context.verify(plain_password, hashed_password)