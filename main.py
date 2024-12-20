from pymem.process import *
from pymem.exception import *
from pymem import *
from time import sleep
from banner import *
import os
import json

with __builtins__.open("settings.json","r") as arquivo:
    data = json.load(arquivo)
    name = data["resolution"]["module"]

pm = Pymem("ShadowOfWar.exe")
module = module_from_name(pm.process_handle,name).lpBaseOfDll

def getPointer(base, offsets):
    # Lê o endereço base na memória do processo
    addr = pm.read_ulonglong(base)
    # Itera sobre os offsets fornecidos para calcular o endereço final
    for offset in offsets:
        if offset != offsets[-1]:  # Se não for o último offset, continua o cálculo
            addr = pm.read_ulonglong(addr + offset)
    # Adiciona o último offset para obter o endereço final
    addr += offsets[-1]
    return addr  # Retorna o endereço final calc

def targetResolution():
    enderecoR = int(data["resolution"]["endereco"],16)
    offsetsR = [int(f"0x{offset}",16) for offset in data["resolution"]["offsets"]]
    return pm.write_float(getPointer(module + enderecoR, offsetsR),500.0)

def targetLife():
    enderecoL = int(data["life"]["endereco"],16)
    offsetsL = [int(f"0x{offset}",16) for offset in data["life"]["offsets"]]
    return pm.write_float(getPointer(module + enderecoL, offsetsL), 500.0)

def main():
    banner = layout()
    print(banner)
    sleep(2)
    print("[*] Injetado!")
    while True:
        targetResolution()
        targetLife()


if __name__ == "__main__":
    main()