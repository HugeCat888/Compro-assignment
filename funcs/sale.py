import struct as st
import os
from funcs.fix_str import fix_str, decode_str

product_path = os.path.abspath("products.bin")

def sale_handler(path, fmt, size):
    import datetime
    while True:
        try:
            print("\nPlease choose from list:")
            print("\n| 1. Read sale details")
            print("|-- 1.1 Read all fields")
            print("|-- 1.2 Read by Id")
            print("| 2. Update sale details by Id")
            print("| 3. Delete sale details")
            print("|-- 3.1 Delete specific sale")
            print("|-- 3.2 Delete all sales")
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
                            print("="*94)
                            print("| Sale ID  | " + "Product ID  | " + "Quantity  | " + "Total Amount        | " + "Created At     | " + "Updated At     |")
                            print("="*94)
                            while chuck := file.read(size):
                                saleId, productId, quantity, totalAmount, created_at, updated_at = st.unpack(fmt, chuck)
                                created_dt = datetime.datetime.fromtimestamp(created_at)
                                created_at = created_dt.strftime("%d/%m %H:%M")
                                updated_dt = datetime.datetime.fromtimestamp(updated_at)
                                updated_at = updated_dt.strftime("%d/%m %H:%M")
                                print(f"| {decode_str(saleId):<8} | {decode_str(productId):<11} | {quantity:<9} | {totalAmount:<19} | {created_at:<14} | {updated_at:<14} |")
                            print("="*94)
                    elif read_opt == 2:
                        sale_id = input("\nEnter Sale ID: ")
                        if "0" not in sale_id or len(sale_id) < 6:
                            sale_id = "0" * (5 - len(sale_id)) + sale_id
                            if not sale_id.startswith("S"):
                                sale_id = "S" + sale_id
                        with open(path, "rb") as file:
                            while chuck := file.read(size):
                                sales = st.unpack(fmt, chuck)
                                if decode_str(sales[0]) == sale_id:
                                    created_dt = datetime.datetime.fromtimestamp(sales[4])
                                    created_at = created_dt.strftime("%d/%m %H:%M")
                                    updated_dt = datetime.datetime.fromtimestamp(sales[5])
                                    updated_at = updated_dt.strftime("%d/%m %H:%M")
                                    print(f"Sale details for ID {sale_id}: ")
                                    print("="*60)
                                    print(f"| Sale ID      : {decode_str(sales[0])}")
                                    print(f"| Product ID   : {decode_str(sales[1])}")
                                    print(f"| Quantity     : {sales[2]}")
                                    print(f"| Total Amount : {sales[3]}")
                                    print(f"| Created At   : {created_at}")
                                    print(f"| Updated At   : {updated_at}")
                                    print("="*60)
                except Exception as e:
                    print(f"Error reading sale details: {e}")
            case 2:
                sale_id = input("Enter Sale ID to update: ").strip()
                if "0" not in sale_id or len(sale_id) < 6:
                    sale_id = "0" * (5 - len(sale_id)) + sale_id
                    if not sale_id.startswith("S"):
                        sale_id = "S" + sale_id
                temp_path = ".tmp"
                found = False
                with open(path, "rb") as file, open(temp_path, "wb") as tmp:
                    while chunk := file.read(size):
                        record = st.unpack(fmt, chunk)
                        if decode_str(record[0]) == sale_id:
                            found = True
                            created_dt = datetime.datetime.fromtimestamp(record[4])
                            created_at = created_dt.strftime("%d/%m %H:%M")
                            updated_dt = datetime.datetime.fromtimestamp(record[5])
                            updated_at = updated_dt.strftime("%d/%m %H:%M")
                            print("Current values:")
                            print(f"| Sale ID      : {decode_str(record[0])}")
                            print(f"| Product ID   : {decode_str(record[1])}")
                            print(f"| Quantity     : {record[2]}")
                            print(f"| Total Amount : {record[3]}")
                            print(f"| Created At   : {created_at}")
                            print(f"| Updated At   : {updated_at}")
                            new_quantity = int(input("Enter new quantity (or -1 to keep): "))
                            if new_quantity == -1:
                                new_quantity = record[2]
                            new_total = float(input("Enter new total amount (or -1 to keep): "))
                            if new_total == -1:
                                new_total = record[3]
                            updated_at = datetime.datetime.now().timestamp()
                            new_record = st.pack(fmt, record[0], record[1], new_quantity, new_total, record[4], updated_at)
                            tmp.write(new_record)
                        else:
                            tmp.write(chunk)
                if found:
                    os.replace(temp_path, path)
                    print("Sale record updated.")
                else:
                    os.remove(temp_path)
                    print("Sale ID not found.")
            case 3:
                print("Delete Options:")
                print("1. Delete specific sale")
                print("2. Delete all sales")
                print("0. Cancel")
                opt = int(input("Your input: "))
                if opt == 0:
                    print("Cancel delete.")
                elif opt == 1:
                    sale_id = input("Enter Sale ID to delete: ").strip()
                    if "0" not in sale_id or len(sale_id) < 6:
                        sale_id = "0" * (5 - len(sale_id)) + sale_id
                        if not sale_id.startswith("S"):
                            sale_id = "S" + sale_id
                    temp_path = ".tmp"
                    found = False
                    with open(path, "rb") as file, open(temp_path, "wb") as tmp:
                        while chunk := file.read(size):
                            record = st.unpack(fmt, chunk)
                            if decode_str(record[0]) == sale_id:
                                found = True
                                continue
                            tmp.write(chunk)
                    if found:
                        os.replace(temp_path, path)
                        print("Sale record deleted.")
                    else:
                        os.remove(temp_path)
                        print("Sale ID not found.")
                elif opt == 2:
                    confirm = input("Are you sure you want to delete all sales? (y/n): ")
                    if confirm.lower() == "y":
                        open(path, "wb").close()
                        print("All sale records deleted.")
                    else:
                        print("Cancelled.")
            case 0:
                break
            case _:
                print("Invalid option")
        
        options = int(input("\nDo you want to continue? (0 for no, other for yes): "))
        
        if options == 0:
            break