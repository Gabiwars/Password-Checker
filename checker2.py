import requests
import hashlib # Module to hash our password (sha1)

# Accessing the webiste
def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the API')
    return res

# Counting how many times the password has been leaked
def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

# Hashing the password, getting the first and last 5 char from the password
def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)

# Printing out the results
def main(args):
    count = pwned_api_check(args)
    if count:
        print(f'{args} was found {count} times')
    else:
        print(f'{args} was not found')

# Only execute if it is the main program.
# Asking the user for the password or break to exit out.
if __name__ == '__main__':
    while True:
        password = input('type "break" to exit\npassword: ')
        if password == 'break':
            break
        main(password)
