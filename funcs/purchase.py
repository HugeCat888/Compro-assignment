import struct as st
import os
from funcs.fix_str import fix_str, decode_str

def purchase_handler(path, fmt, size):
    while True:
        try:
            print("\nPlease choose from list:")
            print("\n| 1. Read purchase details")
            print("|-- 1.1 Read all fields")
            print("|-- 1.2 Read by Id")
            print("| 0. Exit")
            options = int(input("\nyour input: "))
        except:
            print("Invalid option")
            continue
        
        match options:
            case 1:
                read_opt = int(input("\n1: Read all fields\n2: Read by Id\nYour input: "))
                if not read_opt and read_opt not in [1, 2]:
                    print("Invalid option")
                    continue
                try:
                    if read_opt == 1:
                        with open(path, "rb") as file:
                            while chuck := file.read(size):
                                purchaseId, productId, productName, quantity, total, Note, created_at, updated_at = st.unpack(fmt, chuck)
                                print(f"\n| Purchase ID: {decode_str(purchaseId)}")
                                print(f"| Product ID: {decode_str(productId)}")
                                print(f"| Product Name: {decode_str(productName)}")
                                print(f"| Quantity: {quantity}")
                                print(f"| Total: {total}")
                                print(f"| Note: {decode_str(Note)}")
                                print(f"| Created At: {created_at}")
                                print(f"| Updated At: {updated_at}")
                    elif read_opt == 2:
                        purchase_id = input("\nEnter Purchase ID: ")
                        if "0" not in purchase_id or len(purchase_id) < 6:
                            purchase_id = "0" * (5 - len(purchase_id)) + purchase_id
                            if not purchase_id.startswith("P"):
                                purchase_id = "P" + purchase_id
                        with open(path, "rb") as file:
                            print(f"Purchase details for ID {purchase_id}: ")
                            while chuck := file.read(size):
                                purchaseId, productId, productName, quantity, total, Note, created_at, updated_at = st.unpack(fmt, chuck)
                                if decode_str(purchaseId) == purchase_id:
                                    print(f"\n| Purchase ID: {decode_str(purchaseId)}")
                                    print(f"| Product ID: {decode_str(productId)}")
                                    print(f"| Product Name: {decode_str(productName)}")
                                    print(f"| Quantity: {quantity}")
                                    print(f"| Total: {total}")
                                    print(f"| Note: {decode_str(Note)}")
                                    print(f"| Created At: {created_at}")
                                    print(f"| Updated At: {updated_at}")
                except Exception as e:
                    print(f"Error reading purchase details: {e}")
            case _:
                print("Invalid option")
        
        options = int(input("\nDo you want to continue? (0 for no, other for yes): "))
        
        if options == 0:
            break