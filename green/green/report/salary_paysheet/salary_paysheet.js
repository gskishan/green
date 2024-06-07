// Copyright (c) 2024, kushdhallod@gmail.com and contributors
// For license information, please see license.txt

frappe.query_reports["Salary Paysheet"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Company",
			"reqd": 1,
			"default": frappe.defaults.get_default("company")
		},
		{
			"fieldname": "currency",
			"label": __("Currency"),
			"fieldtype": "Link",
			"options": "Currency",
			"reqd": 1,
			"default": "INR"
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			on_change: function() {
				if (frappe.query_report.filters[1].value ){

					frappe.query_report.set_filter_value('to_date', get_month_end(frappe.query_report.filters[2].value ));
				}
			}
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			

		},

	]
};
function get_month_end(date) {
    var d = new Date(date);
    return new Date(d.getFullYear(), d.getMonth() + 1, 0);
}
function getTodayDate() {
    var d = new Date();
    var f = n => ('0' + n).slice(-2);
    return f(d.getDate()) + '-' + f(d.getMonth() + 1) + '-' + d.getFullYear();
}
function formatDate(inputDate) {
    var d = new Date(inputDate);
    var f = n => ('0' + n).slice(-2);
    return f(d.getDate()) + '.' + f(d.getMonth() + 1) + '.' + d.getFullYear();
}

function convertMoneyToWords(amt, cur) {
    frappe.call({
        method: 'green.green.report.salary_paysheet.salary_paysheet.get_money_in_words',
        args: {
            amount: amt,
            currency: cur
        },
        callback: function(response) {
            if (response.message) {
                console.log("Money in words: ", response.message);
				document.getElementById("money-in-words").innerText = response.message

			return response.message
            }
			
        }
    });
}
