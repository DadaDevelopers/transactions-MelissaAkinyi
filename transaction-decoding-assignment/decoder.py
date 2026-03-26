import binascii

def decode_transaction(hex_string):
    """
    Decode a simple Bitcoin transaction (legacy and SegWit) from hex format.
    
    Args:
        hex_string (str): Raw transaction hex
        
    Returns:
        dict: Decoded transaction components
    """
    # Convert hex string to bytes
    tx_bytes = bytes.fromhex(hex_string)
    
    decoded = {}
    cursor = 0
    
    # Version (4 bytes, little endian)
    decoded['version'] = int.from_bytes(tx_bytes[cursor:cursor+4], 'little')
    cursor += 4

    # Check for SegWit marker (00 01)
    marker = tx_bytes[cursor]
    flag = tx_bytes[cursor + 1]
    if marker == 0 and flag == 1:
        decoded['marker'] = f"{marker:02x}"
        decoded['flag'] = f"{flag:02x}"
        cursor += 2
    else:
        decoded['marker'] = None
        decoded['flag'] = None

    # Input count (VarInt)
    input_count = tx_bytes[cursor]
    decoded['inputs'] = []
    cursor += 1

    for i in range(input_count):
        inp = {}
        # Previous tx hash (32 bytes, little endian)
        inp['txid'] = binascii.hexlify(tx_bytes[cursor:cursor+32][::-1]).decode()
        cursor += 32
        # Previous output index (4 bytes, little endian)
        inp['vout'] = int.from_bytes(tx_bytes[cursor:cursor+4], 'little')
        cursor += 4
        # Script length (VarInt, here assume < 0xfd)
        script_len = tx_bytes[cursor]
        inp['script_length'] = script_len
        cursor += 1
        # ScriptSig
        inp['scriptSig'] = binascii.hexlify(tx_bytes[cursor:cursor+script_len]).decode()
        cursor += script_len
        # Sequence (4 bytes)
        inp['sequence'] = tx_bytes[cursor:cursor+4].hex()
        cursor += 4
        decoded['inputs'].append(inp)

    # Output count (VarInt)
    output_count = tx_bytes[cursor]
    decoded['outputs'] = []
    cursor += 1

    for i in range(output_count):
        outp = {}
        # Amount (8 bytes, little endian)
        outp['amount'] = int.from_bytes(tx_bytes[cursor:cursor+8], 'little')
        cursor += 8
        # Script length (VarInt)
        script_len = tx_bytes[cursor]
        cursor += 1
        # ScriptPubKey
        outp['scriptPubKey'] = binascii.hexlify(tx_bytes[cursor:cursor+script_len]).decode()
        cursor += script_len
        decoded['outputs'].append(outp)

    # Witness data (if SegWit)
    if decoded['marker'] == '00' and decoded['flag'] == '01':
        decoded['witness'] = []
        for inp in decoded['inputs']:
            # Number of witness elements (VarInt)
            n_items = tx_bytes[cursor]
            cursor += 1
            items = []
            for _ in range(n_items):
                length = tx_bytes[cursor]
                cursor += 1
                item = binascii.hexlify(tx_bytes[cursor:cursor+length]).decode()
                cursor += length
                items.append(item)
            decoded['witness'].append(items)
    else:
        decoded['witness'] = None

    # Locktime (4 bytes, little endian)
    decoded['locktime'] = int.from_bytes(tx_bytes[cursor:cursor+4], 'little')

    return decoded

# ----------------- Test Section -----------------
if __name__ == "__main__":
    tx_hex = "0200000000010131811cd355c357e0e01437d9bcf690df824e9ff785012b6115dfae3d8e8b36c10100000000fdffffff0220a107000000000016001485d78eb795bd9c8a21afefc8b6fdaedf718368094c08100000000000160014840ab165c9c2555d4a31b9208ad806f89d2535e20247304402207bce86d430b58bb6b79e8c1bbecdf67a530eff3bc61581a1399e0b28a741c0ee0220303d5ce926c60bf15577f2e407f28a2ef8fe8453abd4048b716e97dbb1e3a85c01210260828bc77486a55e3bc6032ccbeda915d9494eda17b4a54dbe3b24506d40e4ff43030e00"
    decoded = decode_transaction(tx_hex)
    print(decoded)