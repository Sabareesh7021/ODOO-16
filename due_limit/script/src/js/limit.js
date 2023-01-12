odoo.define('due_limit.limit ', function(require) {
    'use strict';
//                console.log('-----234567--drftg--------sdfghjkl');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');
//            console.log('-------drftg--------sdfghjkl');

    const pay = ProductScreen => class extends ProductScreen {
          setup() {
       super.setup();

   }
    _onClickPay() {
        console.log('---------------sdfghjkl');
                if(this.currentOrder.partner){
                var am=this.currentOrder.get_total_with_tax() + this.currentOrder.get_rounding_applied()
                console.log(am)
                var limit=this.currentOrder.partner.limit
                console.log(this.currentOrder.get_orderlines())
                if(this.currentOrder.partner.limit<=am){
                 const{ confirmed }= this.showPopup('ConfirmPopup',{
                    title:('Your purchase limit amount is '),
                    body:(limit),
                    });
                else
                 return super._onClickPay();
                }
                }
//                 super._onClickPay();
            }
        };
    Registries.Component.extend(ProductScreen, pay);
    return pay;
});