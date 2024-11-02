import hashlib

ini_str = "Iheptar"
 
print("Initial string", ini_str)
 
result = []
 
def permute(data, i, length): 
    if i == length: 
        result.append(''.join(data) )
    else: 
        for j in range(i, length): 
            data[i], data[j] = data[j], data[i] 
            permute(data, i + 1, length) 
            data[i], data[j] = data[j], data[i]  
permute(list(ini_str), 0, len(ini_str))

for i in result:
    attempt = i + 'wnage'
    hashed_attempt = hashlib.sha256(attempt.encode()).hexdigest()
    print(f'password: {attempt} | hash: {hashed_attempt}')
