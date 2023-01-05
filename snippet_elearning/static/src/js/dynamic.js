odoo.define('snippet_elearning.dynamic', function (require) {
var core = require('web.core');
var publicWidget = require('web.public.widget');
var QWeb = core.qweb;
var rpc = require('web.rpc');

var CourseCarousel = publicWidget.Widget.extend({
        selector: '.js_dynamic_snippet',
        willStart: async function(){
            await rpc.query({
                route: '/elearning_snippet',
            }).then((data) =>{
                this.data = data;
                console.log('data',data);
            })
        },
        start: function(){
            var chunks = _.chunk(this.data,3)
            chunks[0].is_active = true
            this.$el.find('#elearning').html(
            QWeb.render('snippet_elearning.course_carousel',{
                chunks
            })
            )
            },
        })
        publicWidget.registry.snippet_elearning_DynamicSnippet = CourseCarousel;
        return CourseCarousel
})


