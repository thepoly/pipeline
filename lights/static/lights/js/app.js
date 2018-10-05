function populatePicker() {
    $(".cpicker").empty();

    for (var i = 0; i < 360; i += 40) {
        $(".cpicker").append("<div class='color' id=" + i + " style='background-color:hsl(" + i + ",100%,50%);display: table-cell;float:inherit;'></div>");
    }
}

function updatePageColor() {
    $.get("LEDP.txt", function (data) {
        data = data.split("\n");
        $(".header").css("background-color", "rgb(" + data[0] + "," + data[1] + "," + data[2] + ")");
    });
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        let csrftoken = getCookie('csrftoken');
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

var colorPicker = Vue.component('color-picker', {
    template: `
      <div>
        <div v-on:click='updateColor' class="cpicker" style="cursor: pointer;display: table;top: -20px;table-layout:fixed;position:relative;padding-left:0;height:200px;width:100%;border-radius:5px; border-color:black; border-style: solid;"></div>
      </div>`,
    methods: {
        colorChange: function (e) {
            this.populate(e)
        },
        updateBg: function () {
            updatePageColor();
        },
        updateColor: function (e) {
            var newColor = ($(e.target).css("background-color").substring(4));
            newColor = newColor.substring(0, newColor.length - 1);
            newColor = newColor.replace(/ /g, '');
            var comp = this;
            var res = newColor.split(",");
            var pkg = {
                R: res[0],
                G: res[1],
                B: res[2]
            }
            $.post("submit", pkg, function (data) {});

        }
    },
    mounted() {
        populatePicker();
        updatePageColor();

        setInterval(function () {
            updatePageColor();
        }, 1000);
    }

})

$(window).resize(function () {
    populatePicker();
});

Vue.component('app-body', {
    template: `
    <div>
      <div class="header"><img class="title-logo" src="/static/lights/images/logo_m.png"/></div>
      <div class ="project-title"><p class="main-header">PolyLights</p></div>
      <div style="margin: 0 auto; width:75%;top:50px;position:relative;"><color-picker/></div>
      <br><br><br>
      <div class="apiHolder" style="display:none;">
      <div class="api"><div class="post">POST</div> https://poly.rpi.edu/lights/submit/R=0&G=255&B=0</div>
      <div class="api"><div class="get">GET</div> https://poly.rpi.edu/lights/color</div>
      <div class="api"><div class="get">GET</div> https://poly.rpi.edu/lights/stats</div>
      </div>
      <div class="sub-text">Change the color of <a class="link" href="https://poly.rpi.edu">The Rensselaer Polytechnic's</a> Lights in the Rensselaer Student Union.<br><br>
      View the <a style="font-size20px;" class="link" href="#" onclick="$('.apiHolder').toggle();">API</a> | <a style="font-size20px;" class="link" href="https://github.com/thepoly/lights">Github</a>
      </div>
    </div>
  `
})


var app = new Vue({
    el: '#app',
    data: {

    },

    methods: {}
});