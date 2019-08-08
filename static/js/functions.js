function hideentry() {
    $("#handle_form").hide(400);
    $('body').css('background', ' #7FDBFF ');
}

function openModal() {
    document.getElementById('modal').style.display = 'block';
    document.getElementById('fade').style.display = 'block';
}

function closeModal() {
    document.getElementById('modal').style.display = 'none';
    document.getElementById('fade').style.display = 'none';
}

function build_main() {
    const char_dicts = {
        "hank": ['Hank Hill', "/static/images/big_hank.gif"],
        "peggy": ['Peggy Hill', "/static/images/big_peggy.png"],
        "dale": ['Dale Gribble', "/static/images/big_dale.gif"],
        "bobby": ['Bobby Hill', "/static/images/big_bobby.gif"],

    };
    const temp = getKeysWithHighestValue(character_values, 1)[0];

    const name = char_dicts[temp][0];
    const imgsrc = char_dicts[temp][1];
    $("#proclamation").text("You are " + name);
    $("#biggie_char").attr("src", imgsrc);

}

function getKeysWithHighestValue(o, n) {
    var keys = Object.keys(o);
    keys.sort(function (a, b) {
        return o[b] - o[a];
    })
    console.log(keys);
    return keys.slice(0, n);
}

var config = {};
var character_values = {};
var mostBobby ="";
var mostHank ="";
var mostDale="";
var mostPeggy ="";
var mostBobbyConf =0;
var mostHankConf  =0;
var mostDaleConf =0;
var mostPeggyConf  =0;
var leastBobby ="";
var leastHank ="";
var leastDale="";
var leastPeggy ="";
var leastBobbyConf =-99;
var leastHankConf  =-99;
var leastDaleConf =-99;
var leastPeggyConf  =-99;

var ctx = document.getElementById("myChart").getContext("2d");


var frm = $('#handle_form');

//$("body").addClass("loading");

frm.submit(function (e) {

    e.preventDefault();

    $.ajax({
        type: frm.attr('method'),
        url: frm.attr('action'),
        data: frm.serialize(),
        beforeSend: function () {
            openModal();
        },
        success: function (data) {
            console.log('Submission was successful.');
            console.log(data)
            data = JSON.parse(data);
            var i;
            var k;
            var l;
            character_values = {};
            for (i = 0; i < data.length; i++) {
                Object.keys(data[i]).forEach(function (key) {
                    console.log(key);
                    var tweets = (data[i][key]);

                    for (var k = 0; k < tweets.length; k++) {
                        var name = tweets[k][0];
                        var value = tweets[k][1];
                        character_values[name] = (character_values[name] || 0) + 1;
                        character_values[name] += parseFloat(value);
                        console.log(tweets[k][0], tweets[k][1]);
                        //Do something
                    }
                });

            }
            config = {
                type: 'pie',
                data: {
                    datasets: [{
                        data: [
                            character_values['hank'], character_values['dale'], character_values['peggy'], character_values['bobby'],
                        ],
                        backgroundColor: [
                            "#F7464A",
                            "#46BFBD",
                            "#FDB45C",
                            "#4D5360",
                        ],
                        label: 'Dataset 1'
                    }],
                    labels: [
                        "Hank",
                        "Dale",
                        "Peggy",
                        "Bobby"
                    ]
                },
                options: {
                    responsive: true,
                    responsiveAnimationDuration: 2,
                    legend: {
                        display: true,
                        position: 'right',
                        align: 'middle',
                    },
                    title: {
                        display: false,
                    },
                    plugins: {
                        labels: {
                            render: 'image',
                            images: [{
                                src: '/static/images/hank.png',
                                width: 120,
                                height: 122
                            },
                                {
                                    src: '/static/images/dale.png',
                                    width: 120,
                                    height: 140
                                },
                                {
                                    src: '/static/images/peggy.png',
                                    width: 120,
                                    height: 119
                                },
                                {
                                    src: '/static/images/bobby.png',
                                    width: 120,
                                    height: 140
                                },
                            ]
                        }
                    },
                    animation: {
                        animateScale: true,
                        animateRotate: true
                    }
                }
            };

        },

        complete: function (data) {
            closeModal();
            $("#visualizations").css("display", "block");
            build_main();
            new Chart(ctx, config);

        },
        error: function (data) {
            console.log('An error occurred.');
            console.log(data);
        },
    });
});

