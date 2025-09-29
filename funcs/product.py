import struct as st
import os
import datetime
from funcs.fix_str import fix_str, decode_str

sale_path = "sales.bin"
sale_fmt = "<6s6sifdd"
sale_size = st.calcsize(sale_fmt)

purchase_path = "purchases.bin"
purchase_fmt = "<6s6sif255sdd"
purchase_size = st.calcsize(purchase_fmt)

def product_handler(path, fmt, size):
    while True:
        try:
            print("\nPlease choose from list:")
            print("\n| 1. Add product")
            print("| 2. Read product")
            print("|-- 2.1 Read all products")
            print("|-- 2.2 Read by Id")
            print("| 3. Update product")
            print("| 4. Delete product")
            print("| 5. Sell product")
            print("| 6. Purchase product")
            print("| 0. Exit")
            options = int(input("\nyour input: "))
        except:
            print("Invalid option")
            continue
        
        match options:
            case 1:
                try:
                    # Get and validate product ID
                    while True:
                        product_id = input("Enter product ID (start with P): ").strip()
                        if not product_id:
                            print("Error: Product ID cannot be empty")
                            continue
                        if len(product_id) > 6:
                            print("Error: Product ID cannot be longer than 6 characters")
                            continue
                        # Format product ID
                        product_id = "0" * (5 - len(product_id)) + product_id
                        if not product_id.startswith("P"):
                            product_id = "P" + product_id
                        break
                    
                    # Check if product ID already exists
                    if os.path.exists(path):
                        with open(path, "rb") as check_file:
                            while chuck := check_file.read(size):
                                pId, *_ = st.unpack(fmt, chuck)
                                if decode_str(pId) == product_id:
                                    print(f"Error: Product ID {product_id} already exists!")
                                    return
                    
                    # Get and validate product name
                    while True:
                        name = input("Enter product name: ").strip()
                        if not name:
                            print("Error: Product name cannot be empty")
                            continue
                        if len(name) > 255:
                            print("Error: Product name is too long (max 255 characters)")
                            continue
                        break
                    
                    # Get and validate category
                    print("\nPlease choose category from list: ")
                    print("\n1. เครื่องดื่ม\n2. ขนม\n3. อาหารแห้ง\n4. ของสด\n5. เครื่องปรุง")
                    while True:
                        try:
                            cat_choice = int(input("\nEnter Category (1-5): "))
                            if 1 <= cat_choice <= 5:
                                category = category_list(cat_choice)
                                if category:
                                    break
                            print("Error: Please select a valid category (1-5)")
                        except ValueError:
                            print("Error: Please enter a valid number")
                    
                    # Get and validate quantity
                    while True:
                        try:
                            quantity = int(input("Enter quantity: "))
                            if quantity < 0:
                                print("Error: Quantity cannot be negative")
                                continue
                            break
                        except ValueError:
                            print("Error: Please enter a valid number")
                    
                    # Get and validate unit
                    print("\nPlease choose unit from list: ")
                    print("\n1. ชิ้น\n2. ขวด\n3. แพ็ค\n4. กล่อง\n5. ห่อ")
                    while True:
                        try:
                            unit_choice = int(input("\nEnter Unit (1-5): "))
                            if 1 <= unit_choice <= 5:
                                unit = unit_list(unit_choice)
                                if unit:
                                    break
                            print("Error: Please select a valid unit (1-5)")
                        except ValueError:
                            print("Error: Please enter a valid number")
                    
                    # Get and validate selling price
                    while True:
                        try:
                            sell_price = float(input("Enter sell price: "))
                            if sell_price < 0:
                                print("Error: Price cannot be negative")
                                continue
                            break
                        except ValueError:
                            print("Error: Please enter a valid price")
                    
                    # Determine status based on quantity
                    status = "Active" if quantity >= 50 else "Restock" if quantity >= 20 else "Deactive"
                    
                    # Create the product record
                    record = st.pack(
                        fmt,
                        fix_str(product_id),
                        fix_str(name),
                        fix_str(category),
                        quantity,
                        fix_str(unit),
                        sell_price,
                        fix_str(status)
                    )
                    
                    # Write to file
                    try:
                        with open(path, "ab") as file:
                            file.write(record)
                        print(f"\nProduct added successfully:")
                        print(f"ID: {product_id}")
                        print(f"Name: {name}")
                        print(f"Category: {category}")
                        print(f"Quantity: {quantity}")
                        print(f"Unit: {unit}")
                        print(f"Price: {sell_price:.2f}")
                        print(f"Status: {status}")
                    except IOError as e:
                        print(f"Error writing to file: {e}")
                        return
                        
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    return
            case 2:
                def print_product_details(product_data):
                    """Helper function to print product details in a formatted way"""
                    pId, name, category, quantity, unit, sell_price, status = product_data
                    print("\n+" + "-" * 50 + "+")
                    print(f"| Product ID    : {decode_str(pId):<39} |")
                    print(f"| Name         : {decode_str(name):<39} |")
                    print(f"| Category     : {decode_str(category):<39} |")
                    print(f"| Quantity     : {quantity:<39} |")
                    print(f"| Unit         : {decode_str(unit):<39} |")
                    print(f"| Price        : {sell_price:<39.2f} |")
                    print(f"| Status       : {decode_str(status):<39} |")
                    print("+" + "-" * 50 + "+")

                try:
                    if not os.path.exists(path):
                        print("No product database found.")
                        return

                    print("\nRead Options:")
                    print("1. Read all products")
                    print("2. Read specific product by ID")
                    
                    while True:
                        try:
                            read_opt = int(input("\nEnter option (1-2): "))
                            if read_opt in [1, 2]:
                                break
                            print("Error: Please select a valid option (1 or 2)")
                        except ValueError:
                            print("Error: Please enter a valid number")
                    
                    if read_opt == 1:
                        # Read all products
                        products_found = False
                        print("\nProduct List:")
                        with open(path, "rb") as file:
                            while chuck := file.read(size):
                                products_found = True
                                print_product_details(st.unpack(fmt, chuck))
                                
                        if not products_found:
                            print("No products found in database.")
                            
                    elif read_opt == 2:
                        # Read specific product
                        while True:
                            productId = input("Enter product ID (start with P): ").strip()
                            if not productId:
                                print("Error: Product ID cannot be empty")
                                continue
                            if len(productId) > 6:
                                print("Error: Product ID cannot be longer than 6 characters")
                                continue
                            productId = "0" * (5 - len(productId)) + productId
                            if not productId.startswith("P"):
                                productId = "P" + productId
                            break
                        
                        product_found = False
                        with open(path, "rb") as file:
                            while chuck := file.read(size):
                                unpacked_data = st.unpack(fmt, chuck)
                                if decode_str(unpacked_data[0]) == productId:
                                    print(f"\nProduct {productId} found:")
                                    print_product_details(unpacked_data)
                                    product_found = True
                                    break
                                    
                        if not product_found:
                            print(f"\nProduct {productId} not found in database.")
                
                except IOError as e:
                    print(f"Error reading file: {e}")
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    return
            case 3:
                def print_current_values(product_data):
                    """Helper function to print current product values"""
                    pId, name, category, quantity, unit, sell_price, status = product_data
                    print("\nCurrent Product Values:")
                    print("+" + "-" * 50 + "+")
                    print(f"| 1. Name     : {decode_str(name):<39} |")
                    print(f"| 2. Category : {decode_str(category):<39} |")
                    print(f"| 3. Quantity : {quantity:<39} |")
                    print(f"| 4. Unit     : {decode_str(unit):<39} |")
                    print(f"| 5. Price    : {sell_price:<39.2f} |")
                    print("+" + "-" * 50 + "+")

                try:
                    if not os.path.exists(path):
                        print("No product database found.")
                        return

                    # Get and validate product ID
                    while True:
                        productId = input("Enter product ID (start with P): ").strip()
                        if not productId:
                            print("Error: Product ID cannot be empty")
                            continue
                        if len(productId) > 6:
                            print("Error: Product ID cannot be longer than 6 characters")
                            continue
                        productId = "0" * (5 - len(productId)) + productId
                        if not productId.startswith("P"):
                            productId = "P" + productId
                        break

                    # Find the product
                    temp_path = ".tmp"
                    product_found = False
                    
                    with open(path, "rb") as file:
                        product_data = None
                        product_index = 0
                        while chuck := file.read(size):
                            current_data = st.unpack(fmt, chuck)
                            if decode_str(current_data[0]) == productId:
                                product_found = True
                                product_data = current_data
                                break
                            product_index += 1

                    if not product_found:
                        print(f"\nProduct {productId} not found in database.")
                        return

                    # Show current values and update options
                    print_current_values(product_data)
                    print("\nUpdate Options:")
                    print("1. Name")
                    print("2. Category")
                    print("3. Quantity")
                    print("4. Unit")
                    print("5. Sell Price")
                    print("6. Update all fields")
                    print("0. Cancel update")

                    # Get valid update choice
                    while True:
                        try:
                            update_choice = int(input("\nEnter field number to update (0-6): "))
                            if 0 <= update_choice <= 6:
                                break
                            print("Error: Please enter a valid option (0-6)")
                        except ValueError:
                            print("Error: Please enter a valid number")

                    if update_choice == 0:
                        print("Update cancelled.")
                        return

                    # Initialize with current values
                    pId, name, category, quantity, unit, sell_price, status = product_data
                    new_name = decode_str(name)
                    new_category = decode_str(category)
                    new_quantity = quantity
                    new_unit = decode_str(unit)
                    new_sell_price = sell_price

                    # Update selected fields
                    if update_choice == 1 or update_choice == 6:
                        while True:
                            new_name = input("Enter new name: ").strip()
                            if not new_name:
                                print("Error: Name cannot be empty")
                                continue
                            if len(new_name) > 255:
                                print("Error: Name is too long (max 255 characters)")
                                continue
                            break

                    if update_choice == 2 or update_choice == 6:
                        print("\nPlease choose category from list:")
                        print("1. เครื่องดื่ม\n2. ขนม\n3. อาหารแห้ง\n4. ของสด\n5. เครื่องปรุง")
                        while True:
                            try:
                                cat_choice = int(input("\nEnter Category (1-5): "))
                                if 1 <= cat_choice <= 5:
                                    new_category = category_list(cat_choice)
                                    if new_category:
                                        break
                                print("Error: Please select a valid category (1-5)")
                            except ValueError:
                                print("Error: Please enter a valid number")

                    if update_choice == 3 or update_choice == 6:
                        while True:
                            try:
                                new_quantity = int(input("Enter new quantity: "))
                                if new_quantity < 0:
                                    print("Error: Quantity cannot be negative")
                                    continue
                                break
                            except ValueError:
                                print("Error: Please enter a valid number")

                    if update_choice == 4 or update_choice == 6:
                        print("\nPlease choose unit from list:")
                        print("1. ชิ้น\n2. ขวด\n3. แพ็ค\n4. กล่อง\n5. ห่อ")
                        while True:
                            try:
                                unit_choice = int(input("\nEnter Unit (1-5): "))
                                if 1 <= unit_choice <= 5:
                                    new_unit = unit_list(unit_choice)
                                    if new_unit:
                                        break
                                print("Error: Please select a valid unit (1-5)")
                            except ValueError:
                                print("Error: Please enter a valid number")

                    if update_choice == 5 or update_choice == 6:
                        while True:
                            try:
                                new_sell_price = float(input("Enter new sell price: "))
                                if new_sell_price < 0:
                                    print("Error: Price cannot be negative")
                                    continue
                                break
                            except ValueError:
                                print("Error: Please enter a valid price")

                    # Update status based on new quantity
                    new_status = "Active" if new_quantity >= 50 else "Restock" if new_quantity >= 20 else "Deactive"

                    # Prepare new record
                    new_record = st.pack(
                        fmt,
                        pId,  # Keep original product ID bytes
                        fix_str(new_name),
                        fix_str(new_category),
                        new_quantity,
                        fix_str(new_unit),
                        new_sell_price,
                        fix_str(new_status)
                    )

                    # Update file using temporary file for safety
                    try:
                        with open(path, "r+b") as file:
                            file.seek(product_index * size)
                            file.write(new_record)

                        print(f"\nProduct {productId} updated successfully:")
                        print(f"Name: {new_name}")
                        print(f"Category: {new_category}")
                        print(f"Quantity: {new_quantity}")
                        print(f"Unit: {new_unit}")
                        print(f"Price: {new_sell_price:.2f}")
                        print(f"Status: {new_status}")

                    except IOError as e:
                        print(f"Error updating file: {e}")
                        return

                except Exception as e:
                    print(f"Unexpected error: {e}")
                    return
            case 4:
                def confirm_delete(message):
                    """Helper function to confirm deletion"""
                    while True:
                        confirm = input(f"{message} (yes/no): ").lower().strip()
                        if confirm in ['yes', 'y']:
                            return True
                        if confirm in ['no', 'n']:
                            return False
                        print("Please answer 'yes' or 'no'")

                try:
                    if not os.path.exists(path):
                        print("No product database found.")
                        return

                    print("\nDelete Options:")
                    print("1. Delete specific product")
                    print("2. Delete all products")
                    print("0. Cancel")

                    # Get valid delete option
                    while True:
                        try:
                            opt = int(input("\nEnter option (0-2): "))
                            if 0 <= opt <= 2:
                                break
                            print("Error: Please enter a valid option (0-2)")
                        except ValueError:
                            print("Error: Please enter a valid number")

                    if opt == 0:
                        print("Delete operation cancelled.")
                        return

                    elif opt == 1:
                        # Delete specific product
                        while True:
                            productId = input("Enter product ID (start with P): ").strip()
                            if not productId:
                                print("Error: Product ID cannot be empty")
                                continue
                            if len(productId) > 6:
                                print("Error: Product ID cannot be longer than 6 characters")
                                continue
                            productId = "0" * (5 - len(productId)) + productId
                            if not productId.startswith("P"):
                                productId = "P" + productId
                            break

                        # First check if product exists and show its details
                        product_found = False
                        product_details = None
                        with open(path, "rb") as file:
                            while chuck := file.read(size):
                                data = st.unpack(fmt, chuck)
                                if decode_str(data[0]) == productId:
                                    product_found = True
                                    product_details = data
                                    break

                        if not product_found:
                            print(f"\nProduct {productId} not found in database.")
                            return

                        # Show product details before deletion
                        pId, name, category, quantity, unit, sell_price, status = product_details
                        print(f"\nProduct to delete:")
                        print("+" + "-" * 50 + "+")
                        print(f"| Product ID : {decode_str(pId):<39} |")
                        print(f"| Name       : {decode_str(name):<39} |")
                        print(f"| Category   : {decode_str(category):<39} |")
                        print(f"| Quantity   : {quantity:<39} |")
                        print(f"| Unit       : {decode_str(unit):<39} |")
                        print(f"| Price      : {sell_price:<39.2f} |")
                        print(f"| Status     : {decode_str(status):<39} |")
                        print("+" + "-" * 50 + "+")

                        if not confirm_delete(f"\nAre you sure you want to delete product {productId}?"):
                            print("Delete operation cancelled.")
                            return

                        # Proceed with deletion
                        temp_path = ".tmp"
                        try:
                            with open(path, "rb") as file, open(temp_path, "wb") as temp:
                                while chuck := file.read(size):
                                    current_id = decode_str(st.unpack(fmt, chuck)[0])
                                    if current_id != productId:
                                        temp.write(chuck)
                            os.replace(temp_path, path)
                            print(f"\nProduct {productId} has been deleted successfully.")
                        except Exception as e:
                            if os.path.exists(temp_path):
                                os.remove(temp_path)
                            raise e

                    elif opt == 2:
                        # Delete all products
                        if not confirm_delete("\nAre you sure you want to delete ALL products? This action cannot be undone!"):
                            print("Delete operation cancelled.")
                            return

                        try:
                            os.remove(path)
                            print("\nAll products have been deleted successfully.")
                        except FileNotFoundError:
                            print("No product database found.")
                        except PermissionError:
                            print("Error: Permission denied. Please check file permissions.")

                except IOError as e:
                    print(f"Error accessing file: {e}")
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    return
            case 5:
                product_id = input("Enter product ID (start with P): ")
                if "0" not in product_id or len(product_id) < 6:
                    product_id = "0" * (5 - len(product_id)) + product_id
                    if not product_id.startswith("P"):
                        product_id = "P" + product_id
                try:
                    index = 0
                    found_product = None
                    with open(path, "rb") as file:
                        while chuck := file.read(size):
                            current_product = st.unpack(fmt, chuck)
                            if decode_str(current_product[0]) == product_id:
                                found_product = current_product
                                break
                            index += 1
                            
                    if not found_product:
                        print(f"Error: Product ID {product_id} not found!")
                        continue
                    
                    pId, name, category, quantity, unit, sell_price, status = found_product
                    
                    print(f"\n| productId: {decode_str(pId)}")
                    print(f"| Name: {decode_str(name)}")
                    print(f"| Category: {decode_str(category)}")
                    print(f"| Quantity: {quantity}")
                    print(f"| Unit: {decode_str(unit)}")  
                    print(f"| Sell_price: {sell_price}")
                    print(f"| Status: {decode_str(status)}")
                    
                    sell = int(input("\nEnter quantity to sell: "))
                    if sell > quantity:
                        print("Error: Not enough stock to sell.")
                        continue
                    
                    # Auto-generate Sale ID
                    next_sale_num = 1
                    if os.path.exists(sale_path):
                        with open(sale_path, "rb") as sale_file:
                            while chuck := sale_file.read(sale_size):
                                sId, *_ = st.unpack(sale_fmt, chuck)
                                sId_decoded = decode_str(sId)
                                if sId_decoded.startswith("S") and sId_decoded[1:].isdigit():
                                    num = int(sId_decoded[1:])
                                    if num >= next_sale_num:
                                        next_sale_num = num + 1
                    sale_id = f"S{next_sale_num:05d}"
                    current_time = datetime.datetime.now().timestamp()
                    total = (sell * sell_price) + 5
                    sale_record = st.pack(
                        sale_fmt,
                        fix_str(sale_id),
                        pId,
                        sell,
                        total,
                        current_time,
                        current_time
                    )
                    
                    if os.path.exists(sale_path):
                        temp_path = ".tmp"
                        sale_found = False
                        
                        with open(sale_path, "rb") as sale_file, open(temp_path, "wb") as temp:
                            while chuck := sale_file.read(sale_size):
                                sId, spId, squantity, stotal, screated, supdated = st.unpack(sale_fmt, chuck)
                                if decode_str(sId) == sale_id:  # Check by sale_id instead of product_id
                                    sale_found = True
                                    new_qty = squantity + sell
                                    new_total = (new_qty * sell_price) + 5
                                    new_sale_record = st.pack(
                                        sale_fmt,
                                        sId,
                                        spId,
                                        new_qty,
                                        new_total,
                                        screated,  # Keep original creation time
                                        current_time  # Update the update time
                                    )
                                    temp.write(new_sale_record)
                                else:
                                    temp.write(chuck)
                            if not sale_found:
                                temp.write(sale_record)
                        os.replace(temp_path, sale_path)
                    else:
                        with open(sale_path, "wb") as sale_file:
                            sale_file.write(sale_record)
                    
                    new_quantity = quantity - sell
                    new_status = "Active" if new_quantity >= 50 else "Restock" if new_quantity >= 20 else "Deactive"
                    
                    new_record = st.pack(
                        fmt,
                        pId,
                        name,
                        category,
                        new_quantity,
                        unit,
                        sell_price,
                        fix_str(new_status),
                    )
                    
                    with open(path, "r+b") as file:
                        file.seek(index * size)
                        file.write(new_record)
                    
                    print(f"Sold {sell} of product {product_id}.")
                except Exception as e:
                    print("Error: ", e)
            case 6:
                product_id = input("Enter product ID (start with P): ")
                if "0" not in product_id or len(product_id) < 6:
                    product_id = "0" * (5 - len(product_id)) + product_id
                    if not product_id.startswith("P"):
                        product_id = "P" + product_id
                try:
                    index = 0
                    found_product = None
                    with open(path, "rb") as file:
                        while chuck := file.read(size):
                            current_product = st.unpack(fmt, chuck)
                            if decode_str(current_product[0]) == product_id:
                                found_product = current_product
                                break
                            index += 1
                            
                    if not found_product:
                        print(f"Error: Product ID {product_id} not found!")
                        continue
                    
                    pId, name, category, quantity, unit, sell_price, status = found_product
                    print(f"\n| Name: {decode_str(name)}")
                    print(f"| Category: {decode_str(category)}")
                    print(f"| Quantity: {quantity}")
                    print(f"| Unit: {decode_str(unit)}")  
                    print(f"| Sell_price: {sell_price}")
                    print(f"| Status: {decode_str(status)}")
                    
                    # Auto-generate Purchase ID
                    next_purchase_num = 1
                    if os.path.exists(purchase_path):
                        with open(purchase_path, "rb") as purchase_file:
                            while chunk := purchase_file.read(purchase_size):
                                purId, *_ = st.unpack(purchase_fmt, chunk)
                                purId_decoded = decode_str(purId)
                                if purId_decoded.startswith("I") and purId_decoded[1:].isdigit():
                                    num = int(purId_decoded[1:])
                                    if num >= next_purchase_num:
                                        next_purchase_num = num + 1
                    purchase_id = f"I{next_purchase_num:05d}"
                    
                    purchase_qty = int(input("Enter quantity to purchase: "))
                    if purchase_qty <= 0:
                        print("Error: Quantity must be greater than 0")
                        return
                        
                    purchase_desc = input("Enter purchase description: ")
                    current_time = datetime.datetime.now().timestamp()
                    total = purchase_qty * sell_price
                    
                    new_purchase = st.pack(
                        purchase_fmt,
                        fix_str(purchase_id),  
                        pId,                                  
                        purchase_qty,          
                        total,                 
                        fix_str(purchase_desc), 
                        current_time,          
                        current_time           
                    )
                    
                    temp_path = ".tmp"
                    purchase_found = False
                    
                    if os.path.exists(purchase_path):
                        try:
                            with open(purchase_path, "rb") as pur_file, open(temp_path, "wb") as temp:
                                while chunk := pur_file.read(purchase_size):
                                    purId, ppId, pquantity, ptotal, pdesc, pcreated, pupdated = st.unpack(purchase_fmt, chunk)
                                    if decode_str(purId) == purchase_id:
                                        
                                        purchase_found = True
                                        new_qty = pquantity + purchase_qty
                                        new_total = new_qty * sell_price
                                        temp.write(st.pack(
                                            purchase_fmt,
                                            purId,            
                                            ppId,                    
                                            new_qty,
                                            new_total,
                                            pdesc,          
                                            pcreated,       
                                            current_time     
                                        ))
                                    else:
                                        temp.write(chunk)
                                
                                if not purchase_found:
                                    temp.write(new_purchase)
                            
                            os.replace(temp_path, purchase_path)
                        except Exception as e:
                            if os.path.exists(temp_path):
                                os.remove(temp_path)
                            raise e
                    else:
                        
                        with open(purchase_path, "wb") as pur_file:
                            pur_file.write(new_purchase)
                            
                    
                    new_quantity = quantity + purchase_qty
                    new_status = "Active" if new_quantity >= 50 else "Restock" if new_quantity >= 20 else "Deactive"
                    
                    
                    new_record = st.pack(
                        fmt,
                        pId,
                        name,
                        category,
                        new_quantity,
                        unit,
                        sell_price,
                        fix_str(new_status),
                    )
                    
                    
                    try:
                        with open(path, "r+b") as file:
                            file.seek(index * size)
                            file.write(new_record)
                        
                        if purchase_found:
                            print(f"Updated existing purchase {purchase_id}. Total quantity: {new_qty}")
                        else:
                            print(f"Created new purchase {purchase_id}")
                        print(f"Product {product_id} quantity updated to: {new_quantity}")
                    except Exception as e:
                        print(f"Error updating product quantity: {e}")
                except Exception as e:
                    print("Error: ", e)
            case 0:
                break
            case _:
                print("Invalid option")
        options = int(input("\nDo you want to continue? (0 for no, other for yes): "))
        
        if options == 0:
            break

def category_list(index):
    cat_list = {
        1: "เครื่องดื่ม",
        2: "ขนม",
        3: "อาหารแห้ง",
        4: "ของสด",
        5: "เครื่องปรุง"
    }
    for i, v in cat_list.items():
        if i == index:
            return v
        
def unit_list(index):
    unit_list = {
        1: "ชิ้น",
        2: "ขวด",
        3: "แพ็ค",
        4: "กล่อง",
        5: "ห่อ"
    }
    for i, v in unit_list.items():
        if i == index:
            return v