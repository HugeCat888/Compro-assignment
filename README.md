# Stock Management System

A command-line inventory management system built in Python that handles product management, sales, and purchases using binary file storage.

## Project Structure
```
Assignment_2/
├── main.py              # Main program entry point
├── products.bin         # Binary file storing product data
├── sales.bin           # Binary file storing sales records
├── purchases.bin       # Binary file storing purchase records
└── funcs/
    ├── __init__.py
    ├── fix_str.py      # String encoding/decoding utilities
    ├── print_report.py # Report generation functionality
    ├── product.py      # Product management functions
    ├── purchase.py     # Purchase handling functions
    └── sale.py         # Sales handling functions
```

## Features

### 1. Product Management
- Add new products with:
  - Product ID (P00001 format)
  - Product name
  - Category (เครื่องดื่ม, ขนม, อาหารแห้ง, ของสด, เครื่องปรุง)
  - Quantity
  - Unit (ชิ้น, ขวด, แพ็ค, กล่อง, ห่อ)
  - Selling price
  - Status (automatically set based on quantity)
    * Active: quantity ≥ 10
    * Restock: 5 ≤ quantity < 10
    * Deactive: quantity < 5

- Read product information:
  - View all products
  - Search by Product ID
- Update product details
- Delete products (single or all)

### 2. Sales Management
- Record product sales
- Generate unique sale IDs (S00001 format)
- Track:
  - Product details
  - Quantity sold
  - Sale price
  - Total amount
  - Creation and update timestamps
- Automatically update product quantities and status
- Handle multiple sales of the same product

### 3. Purchase Management
- Record product purchases
- Generate unique purchase IDs (I00001 format)
- Track:
  - Product details
  - Quantity purchased
  - Total cost
  - Purchase description/notes
  - Creation and update timestamps
- Automatically update product quantities and status

### 4. Data Storage
- Uses binary files for persistent storage
- Maintains data integrity with proper file handling
- Implements backup through temporary files during updates

## How to Use

1. Run the program:
   ```bash
   python main.py
   ```

2. Choose from the available options:
   - 1: Add product
   - 2: Read product
     * 2.1: Read all products
     * 2.2: Read by ID
   - 3: Update product
   - 4: Delete product
   - 5: Sell product
   - 6: Purchase product
   - 0: Exit

## Data Formats

### Products (products.bin)
- Format: `<6s255s50si50sf15s`
  * Product ID (6 chars)
  * Name (255 chars)
  * Category (50 chars)
  * Quantity (integer)
  * Unit (50 chars)
  * Price (float)
  * Status (15 chars)

### Sales (sales.bin)
- Format: `<6s6s50siffdd`
  * Sale ID (6 chars)
  * Product ID (6 chars)
  * Product Name (50 chars)
  * Quantity (integer)
  * Price (float)
  * Total (float)
  * Created timestamp (double)
  * Updated timestamp (double)

### Purchases (purchases.bin)
- Format: `<6s6s50sif255sdd`
  * Purchase ID (6 chars)
  * Product ID (6 chars)
  * Product Name (50 chars)
  * Quantity (integer)
  * Total (float)
  * Description (255 chars)
  * Created timestamp (double)
  * Updated timestamp (double)
