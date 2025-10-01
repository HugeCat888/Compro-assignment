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
# [2] quantity: i
# [3] total_amount: f
# [4] created_at: d
# [5] updated_at: d

# purchases.bin
# [0] purchase_id: 6s
# [1] product_id: 6s
# [2] quantity: i
# [3] total: f
# [4] note: 255s
# [5] created_at: d
# [6] updated_at: d

product_fmt = "<6s200s50si50sf15s"
product_size = st.calcsize(product_fmt)

sale_fmt = "<6s6sifdd"
sale_size = st.calcsize(sale_fmt)

purchase_fmt = "<6s6sif255sdd"
purchase_size = st.calcsize(purchase_fmt)

def print_report():
    # --- HEADER AND FORMAT LINE (match report.txt) ---
    header = (
        "+--------+------------------------------+-------------+----------+------------+-------------+---------------+---------------+-----------+\n"
    )
    header_titles = (
        "| SellId | Name                         | Category    | Price    | Sell Amount| Prod Remain | Last Sell     | Last Purchase | Status    |"
    )
    def format_line(cols):
        return (
            f"| {str(cols[0]).ljust(6)} "
            f"| {str(cols[1]).ljust(30)} "
            f"| {str(cols[2]).ljust(12)} "
            f"| {str(cols[3]).rjust(8)} "
            f"| {str(cols[4]).rjust(10)} "
            f"| {str(cols[5]).rjust(11)} "
            f"| {str(cols[6]).rjust(13)} "
            f"| {str(cols[7]).rjust(13)} "
            f"| {str(cols[8]).ljust(9)}|"
        )
    # --- END HEADER AND FORMAT LINE ---

    # Read products
    products = []
    if os.path.exists("products.bin"):
        with open("products.bin", "rb") as f:
            while chunk := f.read(product_size):
                products.append(st.unpack(product_fmt, chunk))

    # Read sales
    sales = []
    if os.path.exists("sales.bin"):
        with open("sales.bin", "rb") as f:
            while chunk := f.read(sale_size):
                sales.append(st.unpack(sale_fmt, chunk))

    # Read purchases
    purchases = []
    if os.path.exists("purchases.bin"):
        with open("purchases.bin", "rb") as f:
            while chunk := f.read(purchase_size):
                purchases.append(st.unpack(purchase_fmt, chunk))

    # Prepare product summary rows
    product_rows = []
    # Build a mapping from product_id to latest purchase date
    last_purchase_map = {}
    for p in purchases:
        prod_id = decode_str(p[1])
        purchase_date = datetime.datetime.fromtimestamp(p[5]).strftime("%d/%m")
        if prod_id not in last_purchase_map or p[6] > last_purchase_map[prod_id][0]:
            last_purchase_map[prod_id] = (p[6], purchase_date)
    # Build a mapping from product_id to latest sale datetime
    last_sale_map = {}
    for s in sales:
        prod_id = decode_str(s[1])
        sale_time = s[4]
        sale_dt = datetime.datetime.fromtimestamp(sale_time)
        sale_str = sale_dt.strftime("%d/%m %H:%M")
        if prod_id not in last_sale_map or sale_time > last_sale_map[prod_id][0]:
            last_sale_map[prod_id] = (sale_time, sale_str)
    # For each sale, show the row as in report_backup.txt
    for s in sales:
        sale_id = decode_str(s[0])
        prod_id = decode_str(s[1])
        sell_amount = s[2]
        # Find product info
        prod_info = next((prod for prod in products if decode_str(prod[0]) == prod_id), None)
        if prod_info:
            pId, name, category, quantity, unit, price, status = prod_info
            name = decode_str(name)
            category = decode_str(category)
            status = decode_str(status)
            # Last sale date/time for this product
            last_sell = last_sale_map.get(prod_id, (None, "--/-- --:--"))[1]
            # Last purchase date for this product
            last_purchase = last_purchase_map.get(prod_id, (None, "--/--"))[1]
            product_rows.append([
                sale_id,
                name,
                category,
                f"{price:8.2f}",
                f"{sell_amount:10}",
                f"{quantity:10}",
                last_sell,
                last_purchase,
                status
            ])

    # --- SUMMARY AND STATISTICS ---
    summary_stats = {
        "total": 0, "active": 0, "restock": 0, "deactive": 0,
        "min_price": float("inf"), "max_price": 0,
        "categories": {}
    }
    sales_by_category = {}
    purchases_by_product = {}
    total_sales = 0.0
    total_purchases = 0.0
    best_seller = {"name": "", "amount": 0}
    min_seller = {"name": "", "amount": float("inf")}
    sales_transactions = 0
    purchase_transactions = 0
    # Calculate stats from products
    for prod in products:
        pId, name, category, quantity, unit, price, status = prod
        pId = decode_str(pId)
        name = decode_str(name)
        category = decode_str(category)
        status = decode_str(status)
        summary_stats["total"] += 1
        if status == "Active":
            summary_stats["active"] += 1
            summary_stats["min_price"] = min(summary_stats["min_price"], price)
            summary_stats["max_price"] = max(summary_stats["max_price"], price)
            summary_stats["categories"][category] = summary_stats["categories"].get(category, 0) + 1
        elif status == "Restock":
            summary_stats["restock"] += 1
        else:
            summary_stats["deactive"] += 1
    # Calculate sales and purchases stats
    for s in sales:
        prod_id = decode_str(s[1])
        category = next((decode_str(prod[2]) for prod in products if decode_str(prod[0]) == prod_id), "")
        sales_transactions += 1
        sales_by_category[category] = sales_by_category.get(category, 0) + s[3]
        total_sales += s[3]
        name = next((decode_str(prod[1]) for prod in products if decode_str(prod[0]) == prod_id), "")
        if s[2] > best_seller["amount"]:
            best_seller = {"name": name, "amount": s[2]}
        if s[2] < min_seller["amount"]:
            min_seller = {"name": name, "amount": s[2]}
    for p in purchases:
        prod_id = decode_str(p[1])
        name = next((decode_str(prod[1]) for prod in products if decode_str(prod[0]) == prod_id), "")
        purchase_transactions += 1
        purchases_by_product[name] = purchases_by_product.get(name, 0) + p[3]
        total_purchases += p[3]
    # --- END SUMMARY AND STATISTICS ---

    # Write report
    with open("report.txt", "w", encoding="utf-8") as f:
        f.write("                                          ===================================                                           \n")
        f.write("                                                STOCK MANAGEMENT REPORT                                                 \n")
        f.write("                                          ===================================                                           \n\n")
        now = datetime.datetime.now()
        tz = now.astimezone().strftime('%z')
        f.write(f"Generated At : {now.strftime('%Y-%m-%d %H:%M:%S')} ({tz[:3]}:{tz[3:]})\n")
        f.write("App Version : 1.0\n")
        f.write("Endianness : Little-Endian\n")
        f.write("Encoding : UTF-8 (fixed-length)\n\n")

        # Product summary table
        f.write("[1] PRODUCT SUMMARY\n")
        f.write(header)
        f.write(header_titles + "\n")
        f.write(header)
        for row in product_rows:
            f.write(format_line(row) + "\n")
        f.write(header + "\n\n")

        # Summary stats
        f.write("Summary (Active only)\n")
        f.write(f"- Total Products (records) : {summary_stats['total']}\n")
        f.write(f"- Active Products : {summary_stats['active']}\n")
        f.write(f"- Restock Products: {summary_stats['restock']}\n")
        f.write(f"- Deactivate Products : {summary_stats['deactive']}\n\n")
        f.write("Price Statistics (THB, Active only)\n")
        f.write(f"- Min Price : {summary_stats['min_price']:.2f}\n")
        f.write(f"- Max Price : {summary_stats['max_price']:.2f}\n\n")
        f.write("Products by Category (Active only)\n")
        for cat, count in summary_stats['categories'].items():
            f.write(f"- {cat} : {count}\n")

        # Sales summary
        f.write("\n[2] SALES SUMMARY\n")
        f.write(f"- Total Sales      : {total_sales:.2f} บาท\n")
        f.write(f"- Transactions     : {sales_transactions}\n")
        if best_seller["name"]:
            f.write(f"- Best Seller      : {best_seller['name']} ({best_seller['amount']} units)\n")
        if min_seller["name"]:
            f.write(f"- Min Seller       : {min_seller['name']}\n")
        f.write("- Sales by Category:\n")
        for cat, amount in sales_by_category.items():
            f.write(f"  * {cat:<10} : {amount:.2f} บาท\n")

        # Purchases summary
        f.write("\n[3] PURCHASES SUMMARY\n")
        f.write(f"- Total Purchases  : {total_purchases:.2f} บาท\n")
        f.write(f"- Transactions     : {purchase_transactions}\n")
        f.write("- Purchases by Product:\n")
        for prod, amount in purchases_by_product.items():
            f.write(f"  * {prod} : {amount:.2f} บาท\n")