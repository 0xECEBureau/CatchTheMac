import random as rd

FLAG = "MAC{c0eur_d3_p1eRr3!}"

charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_-!"

def f(a,b,n,x):
	return (a*x+b)%n

def encrypt(message,a,b,n):
	encrypted = ""
	for char in message:
		x = charset.index(char)
		x = f(a,b,n,x)
		encrypted += charset[x]

	return encrypted

n = len(charset)
a = rd.randint(2,n-1)
b = rd.randint(1,n-1)

print(encrypt(FLAG,a,b,n))

# ENCRYPTED FLAG : d8rxOL_3tV0gV{X_}tgeJ