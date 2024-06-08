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
function getAccountNo(company) {
    const accountNumbers = {
        "AKONI TECHNOLOGIES": "920030058398719",
        "Greentek India Limited": "917030022506397",
        "GTK Software Solutions LLP": "923020047728020"
    };

    return accountNumbers[company] || null;
}
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

function numberToWords(num) {
    const units = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine'];
    const teens = ['Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen'];
    const tens = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety'];

    function convertLessThanOneThousand(number) {
        let result = '';

        if (number >= 100) {
            result += units[Math.floor(number / 100)] + ' Hundred ';
            number %= 100;
        }

        if (number >= 20) {
            result += tens[Math.floor(number / 10)] + ' ';
            number %= 10;
        }

        if (number > 0) {
            if (number < 10) {
                result += units[number];
            } else {
                result += teens[number - 10];
            }
        }

        return result;
    }

    if (num === 0) return 'Zero';

    let result = '';

    if (num < 0) {
        result = 'Minus ';
        num = Math.abs(num);
    }

    const crore = Math.floor(num / 10000000);
    const lakh = Math.floor((num % 10000000) / 100000);
    const thousand = Math.floor((num % 100000) / 1000);
    const remainder = num % 1000;

    if (crore) {
        result += convertLessThanOneThousand(crore) + ' Crore ';
    }

    if (lakh) {
        result += convertLessThanOneThousand(lakh) + ' Lakh ';
    }

    if (thousand) {
        result += convertLessThanOneThousand(thousand) + ' Thousand ';
    }

    if (remainder) {
        result += convertLessThanOneThousand(remainder);
    }

    return result.trim();
}

function moneyInWords(number, mainCurrency = "INR", fractionCurrency = "Paise") {
    if (isNaN(number) || number < 0) {
        return "";
    }

    const [main, fraction] = number.toFixed(2).toString().split('.');

    let out;
    if (main === "0" && (fraction === "00" || fraction === "000")) {
        out = `Zero`;
    } else if (main === "0") {
        out = `${numberToWords(fraction)} ${fractionCurrency}`;
    } else {
        out = `${numberToWords(main)}`;
        if (parseInt(fraction, 10) > 0) {
            out += ` and ${numberToWords(fraction)} ${fractionCurrency}`;
        }
    }

    return `${out} only.`;
}
