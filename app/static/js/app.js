/* Add your Application JavaScript */
window.onload = function(){
    const email = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    const name = /^[a-zA-Z ]{2,30}$/;
    $("form.kabian").submit(function(event){
        {
            if (name.test($("#f_names_co").val().toLowerCase()) == false || $("#f_names_co").val().trim().length != $("#f_names_co").val().length){
                alert("You have entered invalid text for your first name!");
                event.preventDefault();
            } 
            if (name.test($("#l_names_co").val().toLowerCase()) == false || $("#l_names_co").val().trim().length != $("#l_names_co").val().length){
                alert("You have entered invalid text for your last name!");
                event.preventDefault();
            } 
            if (email.test($("#email-regex").val().toLowerCase()) == false || $("#email-regex").val().trim().length != $("#email-regex").val().length){
                alert("You have entered an invalid email address!");
                event.preventDefault();
            }  
        }
    });
}