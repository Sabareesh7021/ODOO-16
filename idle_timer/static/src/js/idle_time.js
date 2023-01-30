odoo.define('idle_timer.idle_time', (require) => {
    const SurveyFormWidget = require('survey.form');
    const ajax = require('web.ajax');
    SurveyFormWidget.include({
        _idle_timer: function(option, _submitForm) {
            var self = this;

            ajax.jsonRpc('/survey/idle/timer', 'call', {'token':this.options.surveyToken}).then(values => {
                let idleTime = 0;
                let idleTimer = values['idle_time']*60;
                if (values['idle']) {
                     const timeInterval = setInterval(() => {
                        $('*').bind('mousemove keydown scroll click', function() {
                            idleTime = 0;
                            idleTimer = values['idle_time']*60
                        })
                        idleTime += 1;
                        idleTimer -= 1;
                        console.log(idleTime)
                        $('.countdown').text(idleTimer + " Seconds");
                        console.log(values['idle_time']*60)
                        if (idleTime == values['idle_time']*60) {
                            self._submitForm(option)
                            clearInterval(timeInterval)
                        }
                    }, 1000)
                } else {
                    $('.countdown').hide();
                }
            });
        },
          _initBreadcrumb: function(_submitForm) {
        var option = this.options
        this._idle_timer(option, _submitForm)
        },

    });
});
