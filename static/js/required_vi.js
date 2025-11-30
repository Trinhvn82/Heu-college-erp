document.addEventListener('DOMContentLoaded', function() {
    var requiredFields = document.querySelectorAll('input[required], select[required], textarea[required]');
    requiredFields.forEach(function(field) {
        field.oninvalid = function(e) {
            if (!field.value) {
                if (field.type === 'email') {
                    field.setCustomValidity('Vui lòng nhập email.');
                } else if (field.type === 'password') {
                    field.setCustomValidity('Vui lòng nhập mật khẩu.');
                } else if (field.tagName === 'SELECT') {
                    field.setCustomValidity('Vui lòng chọn thông tin này.');
                } else {
                    field.setCustomValidity('Vui lòng nhập thông tin này.');
                }
            }
        };
        field.oninput = function(e) {
            field.setCustomValidity('');
        };
    });
});
