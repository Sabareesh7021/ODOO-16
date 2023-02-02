$(document).ready(function(){
    let temparray=[]
    $("#add").click(function(){
        var name=$("#name").val().trim()
        var number=$("#phone").val().trim()
        var n=Number(number)
        console.log(name)
        console.log(number)
        if(temparray.includes(n)){
            alert("same numer is saved")

            
        }
        else{
            var contact = "<tr><td>" + name + "</td><td>" + n + "</td><td><button id='edit' class='btn btn-outline-secondary' >Edit</button><button id='delete' class='btn btn-outline-danger'>Delete</button></td></tr>";
            if(name != "" && n != ""){
                temparray.push(n)
                $("#save").append(contact);
                $("#name").val("");
                $("#phone").val("");
            }    
            
        }
        

         
    
    })
    $(document).on("click", "#delete", function(){
        $(this).closest("tr").remove();
    });    

    $(document).on("click", "#edit", function(){
    var currentTD = $(this).parents('tr').find('td');
    if ($(this).html() == 'Edit') {                  
        $.each(currentTD, function () {
            $(this).prop('contenteditable', true)
        });
    } else {
       $.each(currentTD, function () {
            $(this).prop('contenteditable', false)
        });
    }
    $(this).html($(this).html() == 'Edit' ? 'Save' : 'Edit')
    });
    

})    