$(document).ready(function(){
    let tempArray=[]
    $('.btn').click(function(addCart){
        let name=addCart.currentTarget.closest('tr').cells[1].innerHTML
        let price = addCart.currentTarget.closest('tr').cells[2].innerHTML
        let img=addCart.currentTarget.closest('tr').cells[0].innerHTML
        let iprice = Number(price);
        var qt = 1
        var totalPrice = qt*iprice
        console.log(totalPrice)
        if(tempArray.includes(name)){
            alert("already exists in cart")
        }else{
            
            var cart_row = "<tr class='remov'><td>"+ img + "</td><td class='cname'>" + name + "</td><td><input type='number' value='1' min='1' class='qty'></td><td class='unitp'>" + price + "</td><td class='total'>"+totalPrice+"</td><td><button class='btn btn-danger rbutton'>REMOVE</button></td></tr>";
            $('#ctable').append(cart_row);
        
            tempArray.push(name);
            alert("Item Added To Cart");
        }
        var sum=0;
        $('.total').each(function(){
            sum+= parseFloat($(this).text())

        })
        $('.total_Amount').empty()
        $('.total_Amount').append(sum);
        

        
        
    
                $(document).on('click','.qty',function(ev){
                    var x=$(this).closest('tr');
                    var unit_total=0
                    var qt= Number(x.context.value)
                    var unit_Price =  Number(addCart.currentTarget.closest('tr').cells[2].innerHTML)
                    var unit_total=qt*unit_Price
                    x[0].cells[4].innerHTML = unit_total
    
                    var sum=0;
                    $('.total').each(function(){
                        sum+= parseFloat($(this).text())
    
                    })
                    $('.total_Amount').empty()
                    $('.total_Amount').append(sum);
                })
                
                $('#ctable').on('click','.rbutton',function(ev){
                    var name=ev.currentTarget.closest('tr').cells[1].innerHTML
                    tempArray= tempArray.filter(function(element){
                        return element!=name;
                    });
                    $(this).closest('tr').remove()
                });
                $('.clear_cart').click(function(ev){
                    $('.remov').remove()
                    tempArray= []
                    $('.total_Amount').empty()

                })
                
                
    
            
    })
    $('.shop').click(function(){
        $("#ctable").hide()
        $(".product").hide()
        $(".tprice").hide()
        $(".chead").hide()
        $('#bill_body').toggle()
        
        let r=$(".total_Amount").text()
        console.log(r)
        $("#am").val(r)

    })
   
    $('.cart_button').click(function(){
        $(".cart").toggle()
        $("#bill_body").hide()
    })
    $('.home').click(function(){
        $('.product').show()
        $(".tprice").show()
        $(".chead").show()
        $(".cart").show()
        $("#ctable").show()
        $("#bill_body").hide()

    })
    
    function checkDate(){
        rel=/^(0[1-9]|1[0-2])\/?([0-9]{2})$/;
        var date= $("#expr").val();
        if (date.match(rel)){
            $("#espan").text("");
            }
        else{
             $("#espan").text("should be in MM/YY formate");
        }
    }

    $(document).ready(function(){
        $("#phno").focusout(function(){
            var num = $("#phno").val();
            var numbers = /[0-9]/+$g;
            if(num.match(numbers)){
                 $("#pspan").text('');
            }
            else{
                    $("#pspan").text("Number should contain digits ");
            }
            if(( num.length >11) || (num.length< 10)){
                $("#pspan").text("should be 10 digits");
            }
            else{
                   $("#pspan").text('');
            }

        });
    });

    $(function(){
        $("#cvv").focusout(function(){
            var cvv = $("#cvv").val();
            var numbers = /[0-9]/+$g;
            if(cvv.match(numbers)){
                 $("#cvspan").text('');
            }
            else{
                $("#cvspan").text("CVV should contain digits only ");
                return false;
            }
            if (cvv.length < 3){
                $("#cvspan").text("should be 3-4 digits");
            }
            else{
                   $("#cvspan").text('');
            }

        });
    })

    $(function(){
        $("#cnumb").focusout(function(){
            var cno = $("#cnumb").val();
            var numbers = /[0-9]/+$g;
            if(cno.match(numbers)){
                 $("#cspan").text('');
            }
            else{
                $("#cspan").text("Card number should contain digits only ");
                return false;
            }
            if (cno.length < 14){
                $("#cspan").text("should be 14-16 digits");
            }
            else{
                   $("#cspan").text('');
            }

        });
       });

    function hasnum(){
        var name = $("#name").val();
        if(name.length<=3){
             $("#nspan").text("Name should contain minimum 3 characters");
            }
            else{
                    $("#nspan").text('');
            }
        if(/\d/.test(name)){
             $("#nspan").text("Name does not contain numbers ");
            return false;
            }
            else{
                $("#nspan").text('');
            }

     }


});    
