$(document).ready(function() {
	setTimeout(function(){
	 $('.search-bar').before('<div class="hello-text"><strong>' + frappe.defaults.get_user_default("Company") + '</strong></div>');
 
	
	}, 1000);
	
 });
 
