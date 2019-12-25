var vm = avalon.define({
    $id: 'fuyuko',
    show_image_url: '',
    middle_image_name: '',
    middle_image_desc: '',
    start_date: '',
    load_image: false,
    image_json: {},
    web_title: '',
    sub_title: '',
    page_title: '2019年度影集',
    days_back: '',
    imageLayout: function () {
        vm.back_imgs = image_json.back;
        vm.start_date = image_json.days;
        vm.days_back = image_json.days_back;
        vm.web_title = image_json.title;
        vm.sub_title = image_json.sub_title;
        vm.image_json = image_json.photos;
        vm.page_title = image_json.page_title;
    },

    //单击展示大图
    show_middle_image: function (img) {
        console.log($(window).width());
        if ($(window).width() > 720) {
            vm.show_image_url = "";
            var win_height;
            if (vm.start_date && vm.start_date !== "") {
                win_height = $(window).scrollTop() - $(window).height() - 450;
            } else {
                win_height = $(window).scrollTop() - $(window).height() + 50;
            }
            vm.show_image_url = img.middle;
            vm.middle_image_desc = img.desc;
            vm.middle_image_name = img.name;
            var pic = $('#middle_picture');
            //console.log("win:", win_height);
            pic.fadeIn({
                duration: 500
            });
            vm.load_image = true;
            pic.css('top', win_height + 50 + 'px');
            var img_dom = $('#middle_image');
            vm.load_image = false;
            if (img.small_height > img.small_width) {
                img_dom.css('margin-left', $(window).width() / 6 + 'px');
                var new_height = $(window).height() * 0.85;
                img_dom.animate({height: new_height + 'px'}, 200);
                img_dom.animate({width: img.middle_width * new_height / img.middle_height + 'px'}, 200);
            } else {
                img_dom.css('margin-left', '0');
                var new_width = $(window).width() * 0.65;
                img_dom.animate({width: new_width}, 200);
                img_dom.animate({height: img.middle_height * new_width / img.middle_width + 'px'}, 200);
            }
            $('#middle_desc_text')[0].focus();
        }
    },
    show_photo_desc: function (img) {
        img.show_desc = true;
        $('.photo_desc').css("margin-top", '0px');
        $('.photo_desc').animate({marginTop: '-50px'});
    },

    hide_photo_desc: function (img) {
        img.show_desc = false;
        $('.photo_desc').css("margin-top", '0px');
    }

});

$(document).ready(function () {
    $('#middle_picture').fadeOut({
        duration: 10
    });

    vm.imageLayout();
    init_background(0);
    init_days_background();
    var index = 1;
    setInterval(function () {
        init_background(index);
        index += 1;
        if (index >= vm.back_imgs.length) {
            index = 0;
        }
    }, 60000);
    if (vm.start_date && vm.start_date !== "") {
        init_start_date();
        setInterval(function () {
            init_start_date();
        }, 60000);
    }
    $(document).dblclick(function () {
        var pic = $('#middle_picture');
        pic.fadeOut({
            duration: 500
        })
    });
    document.getElementById('middle_image').onload = function (e) {
        vm.load_image = false;
    }

});

function init_background(index) {
    var attr = "url('" + vm.back_imgs[index] + "')";
    $('.banner').css("backgroundImage", attr);
}

function init_days_background() {
    var attr = "url('" + vm.days_back + "')";
    $('.days-coming').css("backgroundImage", attr);
}

function hide_image() {
    var pic = $('#middle_picture');
    pic.fadeOut({
        duration: 500
    })
}

function get_days() {
    var begin = new Date(vm.start_date);
    var s2 = new Date();
    return ((s2.getTime() - begin.getTime()) / (1000 * 60 * 60 * 24)).toFixed(0);
}

function init_start_date() {
    var days = get_days();
    console.log(days);
    $('#count_day').html(days + '<p class="days">days</p>');
}




