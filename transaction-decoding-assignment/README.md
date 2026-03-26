# Bitcoin Transaction Decoder

## Description
The **Bitcoin Transaction Decoder** is a Python-based tool designed to parse and decode raw Bitcoin transaction hex strings. It supports both **legacy and SegWit transactions** and provides a detailed breakdown of all transaction components including inputs, outputs, witness data, and locktime. This project is ideal for developers, blockchain enthusiasts, and students learning about Bitcoin transaction structures.

---

## Key Features
- Decode raw Bitcoin transaction hex strings
- Support for **SegWit (Segregated Witness)** transactions
- Detailed breakdown of transaction components:
  - Version
  - Inputs (txid, vout, scriptSig, sequence)
  - Outputs (amount in satoshis, scriptPubKey)
  - Witness data
  - Locktime
- Handles variable-length fields using **VarInt**
- Outputs structured JSON/dictionary format for easy programmatic use

---

## Technologies Used
- **Python 3.10+**
- Standard libraries:
  - `struct` (for little-endian parsing)
- Optional: Any Python IDE or terminal for execution

---

## Installation Requirements
- Python 3.10 or higher installed
- Optional: Virtual environment for isolation
- No external dependencies required

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/bitcoin-transaction-decoder.git