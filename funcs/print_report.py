import struct as st
import datetime
import os
from funcs.fix_str import fix_str, decode_str

# products.bin
# [0] product_id: 6s
# [1] name: 200s
# [2] category: 50s
# [3] quantity: i
# [4] unit: 50s
# [5] sell_price: f
# [6] status: 15s

# sales.bin
# [0] sale_id: 6s
# [1] product_id: 6s
# [2] product_name: 200s
# [3] quantity: i
# [4] price: f
# [5] total_amount: f
# [6] created_at: d
# [7] updated_at: d

# purchases.bin
# [0] purchase_id: 6s
# [1] product_id: 6s
# [2] product_name: 200s
# [3] quantity: i
# [4] total: f
# [5] note: 255s
# [6] created_at: d
# [7] updated_at: d

product_fmt = "<6s200s50si50sf15s"
product_size = st.calcsize(product_fmt)

sale_fmt = "<6s6s200siffdd"
sale_size = st.calcsize(sale_fmt)

purchase_fmt = "<6s6s200sif255sdd"
purchase_size = st.calcsize(purchase_fmt)

def center_text(text, width, fill_char=" "):
    text_length = len(text)
    padding = (width - text_length) // 2
    return fill_char * padding + text + fill_char * (width - text_length - padding)

def format_number(num):
    return "{:.2f}".format(num)

def format_cell(text, width, align="left"):
    if align == "right":
        return " " * (width - len(text)) + text
    else:
        return text + " " * (width - len(text))

def print_report():
    # Initialize data storage
    product_data = []
    sales_data = []
    purchase_data = []
    
    # Get current timezone offset
    utc_offset = datetime.datetime.now().astimezone().strftime('%z')
    utc_offset = f"{utc_offset[:3]}:{utc_offset[3:]}"
    
    with open("report.txt", "w", encoding="utf-8") as f:
        # Header
        header_width = 120
        f.write(center_text("=".center(35, "="), header_width) + "\n")
        f.write(center_text(" STOCK MANAGEMENT REPORT ", header_width) + "\n")
        f.write(center_text("=".center(35, "="), header_width) + "\n\n")
        
        # System Info
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write("Generated At : " + current_time + " (" + utc_offset + ")\n")
        f.write("App Version : 1.0\n")
        f.write("Endianness : Little-Endian\n")
        f.write("Encoding : UTF-8 (fixed-length)\n\n")
        
        # [1] Product Summary
        f.write("[1] PRODUCT SUMMARY\n")
        header = "+" + "-"*8 + "+" + "-"*29 + "+" + "-"*11 + "+" + "-"*10 + "+" + "-"*6 + "+" + "-"*11 + "+" + "-"*9 + "+\n"
        f.write(header)
        header_cells = [
            format_cell("ProdID", 6),
            format_cell("Name", 27),
            format_cell("Category", 9),
            format_cell("Quantity", 8),
            format_cell("Unit", 4),
            format_cell("SellPrice", 9),
            format_cell("Status", 7)
        ]
        f.write("| " + " | ".join(header_cells) + " |\n")
        f.write(header)
        
        active_count = 0
        restock_count = 0
        deactive_count = 0
        prices = []
        categories = {}
        
        try:
            with open("products.bin", "rb") as pf:
                while chunk := pf.read(product_size):
                    # [0] product_id, [1] name, [2] category, [3] quantity
                    # [4] unit, [5] sell_price, [6] status
                    data = st.unpack(product_fmt, chunk)
                    
                    # Extract and decode data
                    prod_id = decode_str(data[0])
                    name = decode_str(data[1])
                    category = decode_str(data[2])
                    quantity = data[3]
                    unit = decode_str(data[4])
                    sell_price = data[5]
                    status = decode_str(data[6])
                    
                    # Update counters and statistics
                    if status == "Active":
                        active_count += 1
                        prices.append(sell_price)
                        categories[category] = categories.get(category, 0) + 1
                    elif status == "Restock":
                        restock_count += 1
                    else:  # Deactive
                        deactive_count += 1
                    
                    # Calculate proper padding for Thai characters
                    def thai_len(s):
                        return len(s) + sum(1 for c in s if ord(c) > 0x0E00)
                    
                    name_padding = 27 - (thai_len(name) - len(name))
                    category_padding = 9 - (thai_len(category) - len(category))
                    unit_padding = 4 - (thai_len(unit) - len(unit))
                    
                    # Write product line
                    def adjust_width(text, width):
                        thai_chars = sum(1 for c in text if ord(c) > 0x0E00)
                        return width - thai_chars

                    name_width = adjust_width(name, 27)
                    cat_width = adjust_width(category, 9)
                    unit_width = adjust_width(unit, 4)

                    cells = [
                        format_cell(prod_id, 6),
                        format_cell(name, name_width),
                        format_cell(category, cat_width),
                        format_cell(str(quantity), 8, "right"),
                        format_cell(unit, unit_width),
                        format_cell(format_number(sell_price), 9, "right"),
                        format_cell(status, 7)
                    ]
                    f.write("| " + " | ".join(cells) + " |\n")
                
                f.write(header)
                
                # Write summary section
                total_products = active_count + restock_count + deactive_count
                f.write("\nSummary (Active only)\n")
                f.write("- Total Products (records) : " + str(total_products) + "\n")
                f.write("- Active Products : " + str(active_count) + "\n")
                f.write("- Restock Products: " + str(restock_count) + "\n")
                f.write("- Deactivate Products : " + str(deactive_count) + "\n\n")
                
                # Write price statistics
                f.write("Price Statistics (THB, Active only)\n")
                if prices:
                    f.write("- Min Price : " + format_number(min(prices)) + "\n")
                    f.write("- Max Price : " + format_number(max(prices)) + "\n")
                else:
                    f.write("- No active products for price statistics\n")
                f.write("\n")
                
                # Write category summary
                f.write("Products by Category (Active only)\n")
                for cat, count in categories.items():
                    f.write("- " + cat + " : " + str(count) + "\n")
                
        except FileNotFoundError:
            f.write("No product data available.\n")
        
        # [2] Sales Summary
        f.write("\n[2] SALES SUMMARY\n")
        total_sales = 0
        sales_by_category = {}
        product_sales = {}
        product_names = {}  # Store product names for reference
        
        try:
            with open("sales.bin", "rb") as sf:
                transactions = 0
                while chunk := sf.read(sale_size):
                    # [0] sale_id, [1] product_id, [2] product_name, [3] quantity
                    # [4] price, [5] total_amount, [6] created_at, [7] updated_at
                    data = st.unpack(sale_fmt, chunk)
                    transactions += 1
                    
                    prod_id = decode_str(data[1])
                    prod_name = decode_str(data[2])
                    quantity = data[3]
                    total_amount = data[5]
                    
                    total_sales += total_amount
                    product_names[prod_id] = prod_name
                    product_sales[prod_id] = product_sales.get(prod_id, 0) + quantity
                    
                    # Get category from products data
                    try:
                        with open("products.bin", "rb") as pf:
                            while p_chunk := pf.read(product_size):
                                p_data = st.unpack(product_fmt, p_chunk)
                                if decode_str(p_data[0]) == prod_id:
                                    category = decode_str(p_data[2])
                                    sales_by_category[category] = sales_by_category.get(category, 0) + total_amount
                                    break
                    except FileNotFoundError:
                        pass
                
                f.write("- Total Sales      : " + format_number(total_sales) + " บาท\n")
                f.write("- Transactions     : " + str(transactions) + "\n")
                
                if product_sales:
                    best_seller = max(product_sales.items(), key=lambda x: x[1])
                    min_seller = min(product_sales.items(), key=lambda x: x[1])
                    best_name = product_names.get(best_seller[0], best_seller[0])
                    min_name = product_names.get(min_seller[0], min_seller[0])
                    f.write("- Best Seller      : " + best_name + " (" + str(best_seller[1]) + " units)\n")
                    f.write("- Min Seller       : " + min_name + "\n")
                
                f.write("- Sales by Category:\n")
                for cat, amount in sales_by_category.items():
                    cat_padded = format_cell(cat, 10)
                    f.write("  * " + cat_padded + " : " + format_number(amount) + " บาท\n")
        
        except FileNotFoundError:
            f.write("No sales data available.\n")
        
        # [3] Purchases Summary
        f.write("\n[3] PURCHASES SUMMARY\n")
        total_purchases = 0
        purchases_by_product = {}
        
        try:
            with open("purchases.bin", "rb") as pf:
                transactions = 0
                while chunk := pf.read(purchase_size):
                    # [0] purchase_id, [1] product_id, [2] product_name, [3] quantity
                    # [4] total, [5] note, [6] created_at, [7] updated_at
                    data = st.unpack(purchase_fmt, chunk)
                    transactions += 1
                    
                    prod_name = decode_str(data[2])
                    total = data[4]
                    
                    total_purchases += total
                    purchases_by_product[prod_name] = purchases_by_product.get(prod_name, 0) + total
                
                f.write("- Total Purchases  : " + format_number(total_purchases) + " บาท\n")
                f.write("- Transactions     : " + str(transactions) + "\n")
                f.write("- Purchases by Product:\n")
                for prod, amount in purchases_by_product.items():
                    prod_padded = format_cell(prod, 10)
                    f.write("  * " + prod_padded + " : " + format_number(amount) + " บาท\n")
        
        except FileNotFoundError:
            f.write("No purchase data available.\n")
        
        # [4] Profit & Loss Summary
        f.write("\n[4] PROFIT & LOSS SUMMARY\n")
        f.write("- Total Revenue    : " + format_number(total_sales) + " บาท\n")
        f.write("- Total Cost       : " + format_number(total_purchases) + " บาท\n")
        f.write("- Gross Profit     : " + format_number(total_sales - total_purchases) + " บาท\n")