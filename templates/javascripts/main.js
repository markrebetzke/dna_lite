$(function (){

    $.ajax({
        type: 'GET',
        url: 'https://reqres.in/api/users',
        success: function(data){
            console.log('success', data);
        }
    });
});