var initialize = function () {
    console.log("Initialize called")
    $('input[name="text"]').on('keypress', function () {
        console.log("In keypress handler")
        $('.has-error').hide();
    });

}
console.log("list.js loaded")