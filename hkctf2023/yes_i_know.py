from base64 import b64decode, b32decode


class RC4:
    def __init__(self, key=None):
        self.state = list(range(256))  # initialisation de la table de permutation
        self.x = self.y = 0  # les index x et y, au lieu de i et j

        if key is not None:
            self.key = key
            self.init(key)

    # Key schedule
    def init(self, key):
        for i in range(256):
            self.x = (ord(key[i % len(key)]) + self.state[i] + self.x) & 0xFF
            self.state[i], self.state[self.x] = self.state[self.x], self.state[i]
        self.x = 0

    # Decrypt binary input data
    def binaryDecrypt(self, data):
        output = [None] * len(data)
        for i in range(len(data)):
            self.x = (self.x + 1) & 0xFF
            self.y = (self.state[self.x] + self.y) & 0xFF
            self.state[self.x], self.state[self.y] = (
                self.state[self.y],
                self.state[self.x],
            )
            output[i] = (
                data[i] ^ self.state[(self.state[self.x] + self.state[self.y]) & 0xFF]
            )
        return bytearray(output)


def fromBase64URL(msg):
    msg = msg.replace("_", "/").replace("-", "+")
    if len(msg) % 4 == 3:
        return b64decode(msg + "=")
    elif len(msg) % 4 == 2:
        return b64decode(msg + "==")
    else:
        return b64decode(msg)


RC4_PASSWORD = "K#2dF!8t@1qZ"
first = "0.EO6ylFlsUc_7u_QD8gBDp8L8iFiGZGkhptC_QwnSem_ivrO3zFUgj-nfi9hMhgL.khV2U6tVzJq5EWnz-yXZhBWFmKMaKaM65qclb77kF5MWxV6mdVGDyj9BdDJS6uC.49h41eLONT5V_UHgksMdORol-2cYgWkzWj6H6ae8uRzgRMJjDmYss8XBOekyibe.tQVMNb2669ZzoRFkDZWIylBaJ5C"
last = "1.Lp8co2gYHOgdIDqj7CIEWkM"


msgs = [first, last]

fileData = ""
for msg in msgs:
    chunkNumber, rawData = msg.split(".", 1)
    fileData += rawData.replace(".", "")

rc4Decryptor = RC4(RC4_PASSWORD)
outputFileName = "iknowsecret" + ".zip"

with open(outputFileName, "wb+") as fileHandle:
    fileHandle.write(rc4Decryptor.binaryDecrypt(bytearray(fromBase64URL(fileData))))
    fileHandle.close()
