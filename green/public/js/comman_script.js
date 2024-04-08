$(document).ready(function() {
   setTimeout(function(){
    $('.search-bar').before('<div class="hello-text"><strong>' + frappe.defaults.get_user_default("Company") + '</strong></div>');
   if (window.location.pathname === "/app/home") {
    frappe.ui.toolbar.setup_session_defaults();
  }  
   
   }, 1000);
   
});
