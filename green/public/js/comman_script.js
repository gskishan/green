$(document).ready(function() {
	setTimeout(function(){
	 $('.search-bar').before('<div class="hello-text"><strong>' + frappe.defaults.get_user_default("Company") + '</strong></div>');
 
	
	}, 1000);
	
 });
 

function report_view() {
    frappe.views.ReportView.prototype.get_count_element = function(df, data) {
		let $count =0
        return $count;
    };
}

$(document).ready(function() {
    report_view();

    window.onpopstate = function() {
        report_view();
    };

    $('.navbar').on('click', function(event) {
        report_view();
    });


    $(document).on('click', function(event) {
        report_view();
    });

})
