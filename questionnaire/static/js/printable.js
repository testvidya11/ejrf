$(document).ready(function() {
    $(this).find('.form-content input[type="radio"]:checked').each(function() {
        $(this).after('<span><img class="checked-box" src="/static/img/checked.jpeg"></span>');
    });
});