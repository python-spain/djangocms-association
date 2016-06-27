/**
 * Created by nekmo on 27/06/16.
 */

(function ($) {

    var createTag = function (params) {
        return {
            id: params.term,
            text: params.term,
            newOption: true
        }
    };

    var templateResult = function (data) {
        var $result = $("<span></span>");

        $result.text(data.text);

        if (data.newOption) {
            $result.append(" <em>(new)</em>");
        }

        return $result;
    };

    var init = function ($element, options) {
        $element.select2(options);
    };

    var initHeavy = function ($element, options) {
        var settings = $.extend({
            ajax: {
                data: function (params) {
                    return {
                        term: params.term,
                        page: params.page,
                        field_id: $element.data('field_id')
                    };
                },
                processResults: function (data, page) {
                    return {
                        results: data.results,
                        pagination: {
                            more: data.more
                        }
                    };
                }
            }
        }, options);

        $element.select2(settings);
    };

    $.fn.djangoSelect2 = function (options) {
        var settings = $.extend({}, options);
        $.each(this, function (i, element) {
            var $element = $(element);
            if($element.hasClass('django-select2-create-tag')) {
                $.extend(settings, {createTag: createTag})
            }
            if($element.hasClass('django-select2-template-result')){
                $.extend(settings, {templateResult: templateResult})
            }
            if ($element.hasClass('django-select2-heavy')) {
                initHeavy($element, settings);
            } else {
                init($element, settings);
            }
        });
        return this;
    };

    $(function () {
        $('.django-select2').djangoSelect2();
    });

}(this.jQuery));