#!usr/bin/python

   # Simple encode decode functions, I m not hiding anything top secret, If anyone has the patience to write code 
   # to find the key I would have told him what I am hiding myself :P 

def findhash(key):
    shift = 0
    for i in range(0, len(key)):
        shift += (i+1) * ord(key[i])
    return shift%26

def encode(key, string):
    shift = findhash('key')
    string = string.lower()
    encoded_chars = []
    for i in range(0, len(string)):
        c = chr((ord(string[i]) + shift) % 256) 
        if(ord(c) > 122):
            c = chr( ord(c)-25 )
        encoded_chars.append(c)
    encoded = ''.join(encoded_chars)
    return encoded

def decode(key, string):
    shift = findhash('key')
    encoded_chars = []
    for i in range(0, len(string)):
        c = chr((ord(string[i]) - shift) % 256)
        if(ord(c) < 97):
            c = chr( ord(c)+25 )
        encoded_chars.append(c)
    encoded = ''.join(encoded_chars)
    return encoded

def show_result(plaintext, key):
    """Generate a resulting cipher with elements shown"""
    encrypted = encode(key, plaintext)
    decrypted = decode(key, encrypted)

    print ('Key: %s' % key)
    print ('Plaintext: %s' % plaintext)
    print ('Encrytped: %s' % encrypted)
    print ('Decrytped: %s' % decrypted)

def main():
	show_result('family', 'boom')

if __name__ == "__main__": main()