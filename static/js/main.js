$(document).ready(function() {

    // validate signup form on keyup and submit
    $("#signup-form").validate({
        rules: {
            name: {
                required: true,
                minlength: 6
            },
            email: {
                required: true,
                email: true
            },
            password: {
                required: true,
                minlength: 5
            },
            phone:{
                required:true,
                minlength:10,
                maxlength:10,
                number: true
            },
        },
        messages: {
            name: {
                required: "Please enter a Full Name.",
                minlength: "Your Full Name must consist of at least 6 characters long."
            },
            email: "Please enter a valid email address.",
            password: {
                required: "Please provide a password.",
                minlength: "Your password must be at least 5 characters long."
            },
            phone: {
                required: "Please provide a phone number.",
                minlength: "Phone number is invalid."
            },
        }
    });


    // validate login form on keyup and submit
    $("#login-form").validate({
        rules: {
            username: {
                required: true,
                minlength: 6
            },
            password: {
                required: true,
                minlength: 5
            },
        },
        messages: {
            username: {
                required: "Please enter a User Name.",
                minlength: "Your Full Name must consist of at least 6 characters long."
            },
            password: {
                required: "Please provide a password.",
                minlength: "Your password must be at least 5 characters long."
            },
        }
    });
});