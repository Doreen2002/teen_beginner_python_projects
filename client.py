def add_group_order_no(customer,doc):
    def get_customer_group(customer):
        customers = []
        is_group_customer = frappe.db.get_value("Customer", customer, "is_group_customer")
        if is_group_customer == 1:
            customers.append(customer)
            customers.append(frappe.db.get_all("Group Customers", filters={'parent':customer}, pluck="customer_in_group"))
        elif is_group_customer == 0:
            exists_ingroup = frappe.db.get_all("Group Customers", filters={'customer_in_group':customer}, fields=['*'])
            if exists_ingroup != []:
                customers.append(exists_ingroup[0].parent)
                customers.append(frappe.db.get_all("Group Customers", filters={'parent':exists_ingroup[0].parent}, pluck="customer_in_group"))
        return customers
                   
    def generate_group_order_no(customer):
        next_number = 1
        last_doc = frappe.db.get_value(
                "Sales Order", 
                filters={"group_order_no":["is", "set"]}, 
                fieldname="group_order_no", 
                order_by="creation desc"
            )
        if last_doc:
            next_number = int(last_doc) + 1
        else:
            next_number = 1
        return f"{next_number:04d}"
    customers = get_customer_group(customer)
    existing_group_order_no = frappe.db.get_all("Sales Order", filters={"delivery_date":doc.delivery_date,"customer":["in", customers]}, fields=["group_order_no"])
    if existing_group_order_no:
        doc.group_order_no = existing_group_order_no[0].group_order_no
    else:
        next_number = generate_group_order_no(customer)
        doc.group_order_no = next_number
        
add_group_order_no(doc.customer, doc)
