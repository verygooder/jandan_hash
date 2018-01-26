import base64
import hashlib


def b64decode(string):
    string += '=='
    string = bytes(string, encoding='utf-8')
    result = base64.decodebytes(string)
    return result


def md5(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()


def turn(m, r, d):
    d = 0
    q = 4
    r = md5(r)
    o = md5(r[:16])
    n = md5(r[16:])
    l = m[:q]
    c = o + md5(o + l)
    m = m[q:]
    k = b64decode(m)
    h = list(range(256))
    b = [ord(c[g % len(c)]) for g in range(256)]
    f = 0
    for g in range(256):
        f = (f + h[g] + b[g]) % 256
        tmp = h[g]
        h[g] = h[f]
        h[f] = tmp
    t = ''
    k = list(k)
    p = 0
    f = 0
    for g in range(len(k)):
        p = (p + 1) % 256
        f = (f + h[p]) % 256
        tmp = h[p]
        h[p] = h[f]
        h[f] = tmp
        t += chr(k[g] ^ (h[(h[p] + h[f]) % 256]))
    return t

