import struct as st
import os
from funcs.fix_str import fix_str, decode_str

product_path = os.path.abspath("products.bin")

def purchase_handler(path, fmt, size):
    import datetime
    while True:
        try:
            print("\nPlease choose from list:")
            print("\n| 1. Read purchase details")
            print("|-- 1.1 Read all fields")
            print("|-- 1.2 Read by Id")
            print("| 2. Update purchase details by Id")
            print("| 3. Delete purchase details")
            print("|-- 3.1 Delete specific purchase")
            print("|-- 3.2 Delete all purchases")
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
                            print("="*110)
                            print("| Purchase ID   | Product ID   | Quantity  | Total     | Note              | Created At     | Updated At     |")
                            print("="*110)
                            while chuck := file.read(size):
                                purchaseId, productId, quantity, total, Note, created_at, updated_at = st.unpack(fmt, chuck)
                                created_dt = datetime.datetime.fromtimestamp(created_at)
                                created_at = created_dt.strftime("%d/%m %H:%M")
                                updated_dt = datetime.datetime.fromtimestamp(updated_at)
                                updated_at = updated_dt.strftime("%d/%m %H:%M")
                                print(f"| {decode_str(purchaseId):<13} | {decode_str(productId):<12} | {quantity:<9} | {total:<9} | {decode_str(Note):<19} | {created_at:<14} | {updated_at:<14} |")
                            print("="*110)
                    elif read_opt == 2:
                        purchase_id = input("\nEnter Purchase ID: ")
                        if "0" not in purchase_id or len(purchase_id) < 6:
                            purchase_id = "0" * (5 - len(purchase_id)) + purchase_id
                            if not purchase_id.startswith("I"):
                                purchase_id = "I" + purchase_id
                        with open(path, "rb") as file:
                            while chuck := file.read(size):
                                purchases = st.unpack(fmt, chuck)
                                if decode_str(purchases[0]) == purchase_id:
                                    created_dt = datetime.datetime.fromtimestamp(purchases[5])
                                    created_at = created_dt.strftime("%d/%m %H:%M")
                                    updated_dt = datetime.datetime.fromtimestamp(purchases[6])
                                    updated_at = updated_dt.strftime("%d/%m %H:%M")
                                    print(f"Purchase details for ID {purchase_id}: ")
                                    print("="*60)
                                    print(f"| Purchase ID : {decode_str(purchases[0])}")
                                    print(f"| Product ID  : {decode_str(purchases[1])}")
                                    print(f"| Quantity    : {purchases[2]}")
                                    print(f"| Total       : {purchases[3]}")
                                    print(f"| Note        : {decode_str(purchases[4])}")
                                    print(f"| Created At  : {created_at}")
                                    print(f"| Updated At  : {updated_at}")
                                    print("="*60)
                except Exception as e:
                    print(f"Error reading purchase details: {e}")
            case 2:
                purchase_id = input("Enter Purchase ID to update: ").strip()
                if "0" not in purchase_id or len(purchase_id) < 6:
                    purchase_id = "0" * (5 - len(purchase_id)) + purchase_id
                    if not purchase_id.startswith("I"):
                        purchase_id = "I" + purchase_id
                temp_path = ".tmp"
                found = False
                with open(path, "rb") as file, open(temp_path, "wb") as tmp:
                    while chunk := file.read(size):
                        record = st.unpack(fmt, chunk)
                        if decode_str(record[0]) == purchase_id:
                            found = True
                            created_dt = datetime.datetime.fromtimestamp(record[5])
                            created_at = created_dt.strftime("%d/%m %H:%M")
                            updated_dt = datetime.datetime.fromtimestamp(record[6])
                            updated_at = updated_dt.strftime("%d/%m %H:%M")
                            print("Current values:")
                            print(f"| Purchase ID : {decode_str(record[0])}")
                            print(f"| Product ID  : {decode_str(record[1])}")
                            print(f"| Quantity    : {record[2]}")
                            print(f"| Total       : {record[3]}")
                            print(f"| Note        : {decode_str(record[4])}")
                            print(f"| Created At  : {created_at}")
                            print(f"| Updated At  : {updated_at}")
                            new_quantity = int(input("Enter new quantity (or -1 to keep): "))
                            if new_quantity == -1:
                                new_quantity = record[2]
                            new_total = float(input("Enter new total (or -1 to keep): "))
                            if new_total == -1:
                                new_total = record[3]
                            new_note = input("Enter new note (or leave blank to keep): ")
                            if not new_note:
                                new_note = decode_str(record[4])
                            updated_at = datetime.datetime.now().timestamp()
                            new_record = st.pack(fmt, record[0], record[1], new_quantity, new_total, fix_str(new_note), record[5], updated_at)
                            tmp.write(new_record)
                        else:
                            tmp.write(chunk)
                if found:
                    os.replace(temp_path, path)
                    print("Purchase record updated.")
                else:
                    os.remove(temp_path)
                    print("Purchase ID not found.")
            case 3:
                print("Delete Options:")
                print("1. Delete specific purchase")
                print("2. Delete all purchases")
                print("0. Cancel")
                opt = int(input("Your input: "))
                if opt == 0:
                    print("Cancel delete.")
                elif opt == 1:
                    purchase_id = input("Enter Purchase ID to delete: ").strip()
                    if "0" not in purchase_id or len(purchase_id) < 6:
                        purchase_id = "0" * (5 - len(purchase_id)) + purchase_id
                        if not purchase_id.startswith("I"):
                            purchase_id = "I" + purchase_id
                    temp_path = ".tmp"
                    found = False
                    with open(path, "rb") as file, open(temp_path, "wb") as tmp:
                        while chunk := file.read(size):
                            record = st.unpack(fmt, chunk)
                            if decode_str(record[0]) == purchase_id:
                                found = True
                                continue
                            tmp.write(chunk)
                    if found:
                        os.replace(temp_path, path)
                        print("Purchase record deleted.")
                    else:
                        os.remove(temp_path)
                        print("Purchase ID not found.")
                elif opt == 2:
                    confirm = input("Are you sure you want to delete all purchases? (y/n): ")
                    if confirm.lower() == "y":
                        open(path, "wb").close()
                        print("All purchase records deleted.")
                    else:
                        print("Cancelled.")
            case 0:
                break
            case _:
                print("Invalid option")
        
        options = int(input("\nDo you want to continue? (0 for no, other for yes): "))
        
        if options == 0:
            break