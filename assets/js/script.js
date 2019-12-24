var vm = avalon.define({
    $id: 'fuyuko',
    img_list: [],
    img_1_list: [],
    img_2_list: [],
    img_3_list: [],
    img_4_list: [],
    show_image_url: '',
    middle_image_name: '',
    middle_image_desc: '',
    start_date: '',
    load_image: false,
    image_json: {},
    imageLayout: function () {
        vm.start_date = image_json.days;
        vm.web_title = image_json.title;
        vm.sub_title = image_json.sub_title;
        vm.image_json = image_json.photos;
        // vm.image_json['photos'].forEach(function (photo_list) {
        //     photo_list['photo_info'].forEach(function (photo) {
        //         photo['flex'] = photo.small_width * 200 / photo.small_height;
        //         photo['show_desc'] = false;
        //
        //     })
        // })
    },

    show_middle_image: function (img) {
        console.log($(window).width());
        if ($(window).width() > 720) {
            vm.show_image_url = "";

            var win_height = $(window).scrollTop() - $(window).height() - 450;
            vm.show_image_url = img.middle;
            vm.middle_image_desc = img.desc;
            vm.middle_image_name = img.name;
            var pic = $('#middle_picture');
            console.log("win:", win_height);
            pic.fadeIn({
                duration: 500
            });
            vm.load_image = true;
            pic.css('top', win_height + 50 + 'px');
            var img_dom = $('#middle_image');
            vm.load_image = false;
            if (img.small_height > img.small_width) {
                img_dom.css('margin-left',  $(window).width() / 6 + 'px');
                img_dom.animate({height: img.middle_height * 0.6 + 'px'});
                img_dom.animate({width: img.middle_width * 0.6 + 'px'});
            } else {
                img_dom.css('margin-left', '0');
                img_dom.css('height', 'auto');
                img_dom.css('width: 80%');
            }
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
    var index = 1;
    setInterval(function () {
        var attr = "url('http://www.xiaomaidong.com/fuyuko/images/back_" + index + ".png')";
        console.log(attr);
        $('.banner').css("backgroundImage", attr);
        index += 1;
        if (index > 4) {
            index = 1;
        }
    }, 60000);
    $('#count_day').html(get_days() + '<p class="days">days</p>');
    setInterval(function () {
        var days = get_days();
        console.log(days);
        $('#count_day').html(days + '<p class="days">days</p>')
    }, 60000);

    vm.imageLayout();

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





