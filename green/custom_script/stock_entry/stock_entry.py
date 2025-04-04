import frappe

@frappe.whitelist()
def get_work_order_items(work_order):
    if not work_order:
        return []

    work_order_items = frappe.get_all(
        "Work Order Item",
        filters={"parent": work_order},
        fields=["item_code", "source_warehouse", "required_qty","item_name","description"]
    )

    for item in work_order_items:
        # Get actual stock quantity from Bin
        bin_qty = frappe.get_value("Bin", {"item_code": item["item_code"], "warehouse": item["source_warehouse"]}, "actual_qty") or 0
        item["actual_qty"] = bin_qty

        # Get Stock UOM from Item Doctype
        stock_uom = frappe.get_value("Item", item["item_code"], "stock_uom")

        # Get matching UOM and Conversion Factor from Item UOM table
        uom_data = frappe.get_all(
            "UOM Conversion Detail",
            filters={"parent": item["item_code"], "uom": stock_uom},
            fields=["uom", "conversion_factor"]
        )

        if uom_data:
            item["uom"] = uom_data[0]["uom"]
            item["conversion_factor"] = uom_data[0]["conversion_factor"]
        else:
            item["uom"] = stock_uom
            item["conversion_factor"] = 1  # Default Conversion Factor

    return work_order_items



# @frappe.whitelist()
# def get_work_order_items(work_order_ids):
#     import json
#     work_order_ids = json.loads(work_order_ids)
#     items = []

#     for work_order_id in work_order_ids:
#         work_order = frappe.get_doc("Work Order", work_order_id)
#         for item in work_order.required_items:
#             items.append({
#                 "item_code": item.item_code,
#                 "item_name": item.item_name,
#                 "description": item.description,
#                 "qty": item.required_qty,
#                 "uom": item.stock_uom,
#                 "warehouse": work_order.wip_warehouse  # Fetch warehouse from Work Order
#             })

    # return items

@frappe.whitelist()
def get_work_order_item(work_order_ids):
    import json
    work_order_ids = json.loads(work_order_ids)
    all_items = []

    for work_order in work_order_ids:
        if not work_order:
            continue

        work_order_items = frappe.get_all(
            "Work Order Item",
            filters={"parent": work_order},
            fields=["item_code", "source_warehouse", "required_qty", "item_name", "description","stock_uom"]
        )

        for item in work_order_items:
            bin_qty = frappe.get_value("Bin", {"item_code": item["item_code"], "warehouse": item["source_warehouse"]}, "actual_qty") or 0
            item["actual_qty"] = bin_qty

            # **Filter items: Add only if required_qty > actual_qty**
            if item["required_qty"] > item["actual_qty"]:
                stock_uom = frappe.get_value("Item", item["item_code"], "stock_uom")

                uom_data = frappe.get_all(
                    "UOM Conversion Detail",
                    filters={"parent": item["item_code"], "uom": stock_uom},
                    fields=["uom", "conversion_factor"]
                )

                if uom_data:
                    item["uom"] = uom_data[0]["uom"]
                    item["conversion_factor"] = uom_data[0]["conversion_factor"]
                else:
                    item["uom"] = stock_uom
                    item["conversion_factor"] = 1  

                item["qty"] = item["required_qty"] 
                all_items.append(item)

    return all_items
