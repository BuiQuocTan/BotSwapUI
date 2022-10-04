from web3 import Web3
w4 = Web3(Web3.HTTPProvider('https://data-seed-prebsc-1-s1.binance.org:8545/'))
import time
import math
import api

sl = 1-1/100
my_address = '0x1D92242fA9142b2b2A78Dd373514BECD2AdAe1c7'
pkeyyyy = '302ea136bc261ae85f8118c078014406277ad4c6952ff7056e518b5f5c103ff8'
contract_router = w4.eth.contract(address='0x9Ac64Cc6e4415144C455BD8E4837Fea55603e5c3',abi = api.api_router)



def check_path(token, side):
    if side =="0x78867BbEeF44f2326bF8DDd1941a4439382EF2A7":
        return [token,'0x78867BbEeF44f2326bF8DDd1941a4439382EF2A7'] #BUSD_ADDRESS
    elif side =="0x7ef95a0FEE0Dd31b22626fA2e10Ee6A223F8a684":
        return [token,'0x78867BbEeF44f2326bF8DDd1941a4439382EF2A7','0x7ef95a0FEE0Dd31b22626fA2e10Ee6A223F8a684']
    elif side =="0xae13d989daC2f0dEbFf460aC112a837C89BAa7cd":
        return [token,'0x78867BbEeF44f2326bF8DDd1941a4439382EF2A7','0xae13d989daC2f0dEbFf460aC112a837C89BAa7cd']

def check_vitri(side):
    if side =="0x78867BbEeF44f2326bF8DDd1941a4439382EF2A7":
        return 1
    else :
        return 2

def lamtron(number:float, decimals:int=2):
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.floor(number)
    factor = 10 ** decimals
    return math.floor(number * factor) / factor

def token_name(contract_token,address):
    symbol = contract_token.functions.symbol().call()
    decimal = contract_token.functions.decimals().call()
    return {'name':symbol,
            'decimal':decimal}

def checkSoLuongBan(token,soluong) : 
    contract_token = w4.eth.contract(address = w4.toChecksumAddress(token),abi = api.api_token )
    decimal = token_name(contract_token,token)['decimal']
    balance =lamtron( contract_token.functions.balanceOf(my_address).call()/10**decimal,5)
    print((soluong),'soluong')
    print((balance),'balance')
    if (soluong) > balance :
        return False
    return True

def qouter_token(tokenA, tokenB,soluong ) :
    path = check_path(tokenA,tokenB)
    vitri = check_vitri(tokenB)
    tienban =int(soluong*10**18)
    (print(type(tienban)))
    print((tienban))
    quoter =round(contract_router.functions.getAmountsOut(tienban,path).call()[vitri]/10**18,4)
    return quoter
# print(qouter_token('0x8BaBbB98678facC7342735486C851ABD7A0d17Ca','0x78867BbEeF44f2326bF8DDd1941a4439382EF2A7',1.0))
def sell_pancake(token_A, token_B,socanban):

    contract_token = w4.eth.contract(address = w4.toChecksumAddress(token_A),abi = api.api_token )
    name_token_A = token_name(contract_token,token_A)['name']
    name_token_B = token_name(contract_token,token_B)['name']
    decimal = token_name(contract_token,token_A)['decimal']
    balance =lamtron( contract_token.functions.balanceOf(my_address).call()/10**decimal,5)
    print('balance ',balance)

    aa =int(balance*10**decimal)
    tienban =int(socanban*10**decimal)

    print(aa)
    time.sleep(0.5)

    path = check_path(token_A,token_B)
    vitri = check_vitri(token_B)
    print(path)
    quoter =round( contract_router.functions.getAmountsOut(tienban,path).call()[vitri]/10**18,4)
    print(type(quoter))
    print((quoter))

    print('ban duocccccccccccccccccccccccccccc ', quoter)
    noncee = w4.eth.getTransactionCount(my_address)
    # print('nonceeeeee',noncee)
    deadline = int(time.time()) +1000
    fn = contract_router.functions.swapExactTokensForTokens(tienban, int(quoter*sl*10**18), path, my_address, deadline).buildTransaction(
        {"chainId":97,
    "from": my_address,
    "value": int(0 * 10 ** 18),
    'gasPrice': int(10*10**9),
    "gas": 400000,
    "nonce":noncee })

    signed_tx = w4.eth.account.sign_transaction(fn, private_key=pkeyyyy)
    tx_hash = w4.eth.sendRawTransaction(signed_tx.rawTransaction)
    hashhh = (w4.toHex(tx_hash))
    receipt = w4.eth.wait_for_transaction_receipt(tx_hash, timeout=1000)
    eee=receipt['status']
    return {'confirm':eee,
            'hash':hashhh}
