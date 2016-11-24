var ContactForm = function () {

    return {

        //Contact Form
        initContactForm: function () {
	        // Validation
	        $("#sky-form3").validate({
	            // Rules for form validation
	            rules:
	            {
	                name:
	                {
	                    required: true
	                },
	                email:
	                {
	                    required: true,
	                    email: true
	                },
	                message:
	                {
	                    required: true,
	                    minlength: 10
	                },
	                captcha:
	                {
	                    required: true,
	                    remote: 'assets/plugins/sky-forms/version-2.0.1/captcha/process.php'
	                }
	            },

	            // Messages for form validation
	            messages:
	            {
	                name:
	                {
	                    required: '请输入您的姓名',
	                },
	                email:
	                {
	                    required: '请输入您的邮箱地址',
	                    email: '请输入一个有效的邮箱地址以方便我们与您联系'
	                },
	                message:
	                {
	                    required: '请输入您的留言内容'
	                },
	                captcha:
	                {
	                    required: '请输入验证码',
	                    remote: '您输入的验证码不正确，请重新输入'
	                }
	            },

	            // Ajax form submition
	            submitHandler: function(form)
	            {
	                $(form).ajaxSubmit(
	                {
	                    beforeSend: function()
	                    {
	                        $('#sky-form3 button[type="submit"]').attr('disabled', true);
	                    },
	                    success: function()
	                    {
	                        $("#sky-form3").addClass('submited');
	                    }
	                });
	            },

	            // Do not change code below
	            errorPlacement: function(error, element)
	            {
	                error.insertAfter(element.parent());
	            }
	        });
        }

    };

}();
