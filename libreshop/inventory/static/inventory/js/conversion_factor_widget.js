(function($) {
    $(document).ready(function() {

        $('#id_standard_unit_of_measure').change(function(event) {
            $('#id_purchasing_conversion_factor_3').val($('#id_standard_unit_of_measure').val());
        });

        $('#id_standard_unit_of_measure').change();

        $('form').submit(function(event) {
            $(this).find('select:disabled').removeAttr('disabled');
        });
    });
})(django.jQuery);
