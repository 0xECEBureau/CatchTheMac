# La base de la base

Ce challenge est une simple répétition de base64 sur le flag. Il faut donc le décoder pour obtenir le flag.

```python
import base64

def decode_50_times(encoded_string):
    decoded = encoded_string.encode()
    for _ in range(50):
        decoded = base64.b64decode(decoded)
    return decoded.decode()

if __name__ == "__main__":
    with open("challenge.txt", "r") as f:
        data = f.read()
    flag = decode_50_times(data)
    print("[+] Flag:", flag)
```
