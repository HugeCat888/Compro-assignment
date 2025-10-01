import struct as st
import os 
from funcs.product import product_handler
from funcs.sale import sale_handler
from funcs.purchase import purchase_handler
from funcs.print_report import print_report

product_fmt = "<6s200s50si50sf15s"
product_size = st.calcsize(product_fmt)

sale_fmt = "<6s6sifdd"
sale_size = st.calcsize(sale_fmt)

purchase_fmt = "<6s6sif255sdd"
purchase_size = st.calcsize(purchase_fmt)

def main():
    print("Welcome to Stock management system.", end="\n")
    list_path = {
        1: "products.bin",
        2: "sales.bin",
        3: "purchases.bin",
        4: "print_report.txt"
    }
    while True:
        print("\nEnter file name")
        print("\n1: products.bin")
        print("2: sales.bin")
        print("3: purchases.bin")
        print("4: print_report.txt")
        print("0: Exit")
        path = int(input("\nyour input: "))

        if path not in [1, 2, 3, 4, 0]:
            print("Invalid file selection")
            continue
        if path == 0:
            break
        # if "Compro-assignment-main" not in os.getcwd():
        #     abs_path = os.path.abspath(f"{os.getcwd()}/Compro-assignment-main/{list_path[path]}")
        else:
            abs_path = os.path.abspath(f"{list_path[path]}")
        
        match path:
            case 1:
                product_handler(abs_path, product_fmt, product_size)
            case 2:
                sale_handler(abs_path, sale_fmt, sale_size)
            case 3:
                purchase_handler(abs_path, purchase_fmt, purchase_size)
            case 4:
                print_report()
                print("Report generated: print_report.txt")
            case _:
                print("Invalid file selection")
    
if __name__ == "__main__":
    main()