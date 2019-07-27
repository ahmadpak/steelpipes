# frappe-app
Custom app built with Frappe Framework

## Currently working on
app: steelpipes  
discription: This is app is intended to add additional functionality to ERPNEXT for Steel Pipe Manufacturers and Traders  

## Purpose of the app:
Adds transperancy to the purchase cycle, manufactuing and sales cycle for pipes.
### What this app does:
Calculates Mild steel pipe weight automatically based on its attribute values. It also allows users to input scale weight during Delivery Note and Purchase Receipts and validates if the scale weight of the pipe is with in the set range. If allowed range is false the delivery note/ purchase receipt will show error message and will not submit until the matter is resolved or over ruled by the Manager. For now the threshold of the pipe weight is set at +-3%. In future user will be allowed to define its own threshold value. This will add more control over the inventory by insuring wrong items are not delivered. 

In the manfacturing module of this app. User will be able to make workorders as for Pipe production and the app will calculate in realtime that how many pipes will be produced from each strip or coil. As the standard BOM is not applicable in case of pipe manufacturing 


## Installation:
In your frappe-bench folder create a new site:  
  a-  bench new-site site-name  
  b-  bench --site new-site install-app erpnext  
  c-  bench get-app --branch master steelpipes https://github.com/MohammadAhmad1990/steelpipes.git  
  d-  bench include-app steelpipes # To get updates when running bench update  
  e-  bench --site new-site install-app steelpipes  

Login as administrator

Make item named "Pipe" with following variants:
1. Material Type
2. Pipe Size
3. Pipe Thickness
4. Pipe Length
5. Pipe Outer Din
6. Strip.Width 

goto data import tool and import the following files in order for pre made items:
1. item_attributes.xlsx
2. item_group.xlsx
3. Item.xlsx

### Task Completed:
#### 1. Add required custom fields in the following doctypes:
#####  A. Sales Cycle
  1. Sales Order
  2. Sales Order Item
  3. Delivery Note 
  4. Delivery Note Item
  5. Sales Invoice
  6. Sales Invoice Item

#####  B. Purchase Cycle
  1. Purchase Order 
  2. Purchase Order Item
  3. Purchase Receipt
  4. Purchase Receipt Item
  5. Purchase Invoice
  6. Purchase Invoice Item

#####  C. Stock
  1. Stock Entry 
  2. Stock Entry Item

#### 2. Def Modules for each doctype containing custom fields
#### 3. Create .py and .js files for required operations and validations.

### Todo
1. Pipe manufacturing module
2. Pipe manufacturing doctype
3. Code for pipe manufacturing 