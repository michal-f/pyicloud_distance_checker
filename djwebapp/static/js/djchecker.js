
$(document).ready(function () {

    var loadanimation = $("#loadanimaion");
    var out = $("#output");
    loadanimation.hide();

    $("#btn-check").click(function (e) {
        $("#loadanimaion").show();
        out.text(out.text().replace("current:","loading.."));
        //e.preventDefault();
        ajaxPoster("TESTER POST");
    });


    $("#btn-animation").click(function (e) {
        if (loadanimation.is(":visible")) {
            loadanimation.hide();
        } else {
            loadanimation.show();
        }
    });

    /* VERIFY POST DATA AND MAKE REQUEST */
    function ajaxPoster(input) {


        function do_post() {
            $.ajax({
                "type": "POST",
                "dataType": "json",
                "url": "ajax/",
                "data": input,

                "success": function (result) {
                    var distance=result['data']['distance'];
                    var adres=result['data']['adres'];
                    var location="[D:"+distance+"m],[A:"+adres+"]";
                    out.text(" current:" + location);
                     $('#resultArea').append('<p class="resulat-arena">' + location + '</p>');
                },
                "complete": function () {
                    loadanimation.hide();
                },
                "error": function (xhr, textStatus, thrownError) {
                    loadanimation.hide();
                    alert("ERROR::");
                    //popup("error", gettext("post Error:") + thrownError + " txtStatus:" + textStatus + " xhr:" + xhr, gettext("ajax post handler"));
                },
                "async": true
            });
        }
        do_post();
    }


    /*SECURITY TOKEN HANDLING*/
    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');
});