import requests
import json

etherScanApiKey= "APAAAC91153QR2AKTUYP2F33TSTEN1MG7V"
infuraApiKey= "3c796ecbf3df47bd81d8e6025521050f"

myAddr="0x40dE8Fa4B917Ce19648CadC5E04E03d231dea63c"

response = requests.get("https://api.etherscan.io/api?"
                        "module=account"
                        "&action=balance"
                        "&address=" + myAddr +
                        "&tag=latest"
                        "&apikey=" + etherScanApiKey
                        )

jsonParser: int = json.loads(response.text)
value = jsonParser.get("result")
print (value + " wei")
print (int(value) / 1000000000000000000 , "ETH")


response_infura = requests.get("https://mainnet.infura.io/v3/3c796ecbf3df47bd81d8e6025521050f")




### token 전체 목록 읽어오기 ###
ITAMCUBE = "0xbbab3bdb291b0f22bc9881895ff488a5db67bec8"

tokenInfo = requests.get("https://api.etherscan.io/api?"
                        "module=token"
                        "&action=tokeninfo"
                        "&contractaddress=" + ITAMCUBE +
                        "&apikey=" + etherScanApiKey
                         )



response = requests.get("https://api.etherscan.io/api?"
                        "module=account"
                        "&action=tokenbalance"
                        "&contractaddress=" + ITAMCUBE +
                        "&address=" + myAddr +
                        "&tag=latest"
                        "&apikey=" + etherScanApiKey
                        )

jsonParser: int = json.loads(response.text)
value = jsonParser.get("result")
print (value + " wei")
print (int(value) / 1000000000000000000 , "CUBE")


