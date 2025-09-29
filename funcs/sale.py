import struct as st
import os
import datetime
from funcs.fix_str import fix_str, decode_str

product_path = os.path.abspath("products.bin")

def sale_handler(path, fmt, size):
    while True:
        try:
            print("\nPlease choose from list:")
            print("\n| 1. Read sale details")
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
                                saleId, productId, quantity, totalAmount, created_at, updated_at = st.unpack(fmt, chuck)
                                print(f"\n| Sale ID: {decode_str(saleId)}")
                                print(f"| Product ID: {decode_str(productId)}")
                                print(f"| Quantity: {quantity}")
                                print(f"| Total Amount: {totalAmount}")
                                print(f"| Created At: {created_at}")
                                print(f"| Updated At: {updated_at}")
                    elif read_opt == 2:
                        sale_id = input("\nEnter Sale ID: ")
                        if "0" not in sale_id or len(sale_id) < 6:
                            sale_id = "0" * (5 - len(sale_id)) + sale_id
                            if not sale_id.startswith("S"):
                                sale_id = "S" + sale_id
                        with open(path, "rb") as file:
                            print(f"Sale details for ID {sale_id}: ")
                            while chuck := file.read(size):
                                saleId, productId, quantity, totalAmount, created_at, updated_at = st.unpack(fmt, chuck)
                                if decode_str(saleId) == sale_id:
                                    print(f"\n| Sale ID: {decode_str(saleId)}")
                                    print(f"| Product ID: {decode_str(productId)}")
                                    print(f"| Quantity: {quantity}")
                                    print(f"| Total Amount: {totalAmount}")
                                    print(f"| Created At: {created_at}")
                                    print(f"| Updated At: {updated_at}")
                except Exception as e:
                    print(f"Error reading sale details: {e}")
            case 0:
                break
            case _:
                print("Invalid option")
        
        options = int(input("\nDo you want to continue? (0 for no, other for yes): "))
        
        if options == 0:
            break