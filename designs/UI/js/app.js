$(".form").find("input, textarea").on("keyup blur focus", function (e) {
    var $this = $(this)
        , label = $this.prev("label");
    if (e.type === "keyup") {
        if ($this.val() === "") {
            label.removeClass("active highlight");
        }
        else {
            label.addClass("active highlight");
        }
    }
    else if (e.type === "blur") {
        if ($this.val() === "") {
            label.removeClass("active highlight");
        }
        else {
            label.removeClass("highlight");
        }
    }
    else if (e.type === "focus") {
        if ($this.val() === "") {
            label.removeClass("highlight");
        }
        else if ($this.val() !== "") {
            label.addClass("highlight");
        }
    }
});
$(".tab a").on("click", function (e) {
    e.preventDefault();
    $(this).parent().addClass("active");
    $(this).parent().siblings().removeClass("active");
    target = $(this).attr("href");
    $(".tab-content > div").not(target).hide();
    $(target).fadeIn(600);
});
$(document).ready(function () {
    loadfunctionAjax();
});
var loadfunctionAjax = function () {
    $.ajax({
        type: 'GET'
        , url: 'https://eventsbright.herokuapp.com/api/events'
        , contentType: "application/json; charset=utf-8"
        , dataType: "json"
        , success: function (data) {
            console.log(data)
            var trHTML = '';
            $.each(data, function (i, item) {
                console.log(data[i].event.name)
                console.log(data[i].url)
                trHTML += '<div class ="column" >'+
                            '<div class ="callout" >'+
                                '<img class = "thumbnail" src = "http://lorempixel.com/400/200/nightlife" alt="image-one">'+
                                    '<h5>'+data[i].event.name+'</h5>' +
                                    '<i class="fa fa-calendar fa-2x fa-fw" aria-hidden="true"></i>'+
                                    '<p class="small">'+data[i].event.date+'</p>'+
                                '<br>'+
                                '<i class="fa fa-map-marker fa-2x fa-fw" aria-hidden="true"></i>'+
                            '<p class = "small" >'+data[i].event.location+'</p>'+
                        '<a href = "'+data[i].url+'" class = "button small expanded hollow" > View more details </a>' + 
                    '</div >'+
                '</div>'
            });
            $('#eventCard').append(trHTML);
        }
    });
}