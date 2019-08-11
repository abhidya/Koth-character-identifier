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
        "hank": ['Hank Hill', "https://cdn.jsdelivr.net/gh/abhidya/Koth-character-identifier/static/images/big_hank.gif"],
        "peggy": ['Peggy Hill', "https://cdn.jsdelivr.net/gh/abhidya/Koth-character-identifier/static/images/big_peggy.png"],
        "dale": ['Dale Gribble', "https://cdn.jsdelivr.net/gh/abhidya/Koth-character-identifier/static/images/big_dale.gif"],
        "bobby": ['Bobby Hill', "https://cdn.jsdelivr.net/gh/abhidya/Koth-character-identifier/static/images/big_bobby.gif"],

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
var mostBobby = "";
var mostHank = "";
var mostDale = "";
var mostPeggy = "";
var mostBobbyConf = -99;
var mostHankConf = -99;
var mostDaleConf = -99;
var mostPeggyConf = -99;
var leastBobby = "";
var leastHank = "";
var leastDale = "";
var leastPeggy = "";
var leastBobbyConf = 99;
var leastHankConf = 99;
var leastDaleConf = 99;
var leastPeggyConf = 99;


function findmaxmin(key, name, value) {

    switch (name) {
        case "hank":
            if (value > mostHankConf) {
                mostHankConf = value;
                mostHank = key;
            }
            if (value < leastHankConf) {
                leastHankConf = value;
                leastHank = key;
            }
            break;
        case "dale":
            if (value > mostDaleConf) {
                mostDaleConf = value;
                mostDale = key;
            }
            if (value < leastDaleConf) {
                leastDaleConf = value;
                leastDale = key;
            }
            break;
        case "peggy":
            if (value > mostPeggyConf) {
                mostPeggyConf = value;
                mostPeggy = key;
            }
            if (value < leastPeggyConf) {
                leastPeggyConf = value;
                leastPeggy = key;
            }
            break;
        case "bobby":
            if (value > mostBobbyConf) {
                mostBobbyConf = value;
                mostBobby = key;
            }
            if (value < leastBobbyConf) {
                leastBobbyConf = value;
                leastBobby = key;
            }
            break;
    }
}

function buildtweettable(key, tweets) {

    // Find a <table> element with id="myTable":
    var table = document.getElementById("tableoftweets");

// Create an empty <tr> element and add it to the 1st position of the table:
    var row = table.insertRow(table.rows.length);

// Insert new cells (<td> elements) at the 1st and 2nd position of the "new" <tr> element:
    var tweettext = row.insertCell(0);
// Add some text to the new cells:
    tweettext.innerHTML = key;
    var hank = row.insertCell(1);

    var peggy = row.insertCell(2);
    var bobby = row.insertCell(3);
    var dale = row.insertCell(4);
    var k = 0;
    for (var k = 0; k < tweets.length; k++) {
        var name = tweets[k][0];
        var value = tweets[k][1];
        value = value.toFixed(2);
        switch (name) {
            case "hank":
                hank.innerText = value;
                break;
            case "dale":
                dale.innerText = value;

                break;
            case "peggy":
                peggy.innerText = value;

                break;
            case "bobby":
                bobby.innerText = value;

                break;
        }
    }

}


function buildmaxmin() {
    $("#Most_Bobby").text(mostBobby);
    $("#Most_Bobby_conf").text("Confidence Level :   " + mostBobbyConf.toFixed(2));
    $("#Most_Dale").text(mostDale);
    $("#Most_Dale_conf").text("Confidence Level :   " + mostDaleConf.toFixed(2));
    $("#Most_Hank").text(mostHank);
    $("#Most_Hank_conf").text("Confidence Level :   " + mostHankConf.toFixed(2));
    $("#Most_Peggy").text(mostPeggy);
    $("#Most_Peggy_conf").text("Confidence Level :   " + mostPeggyConf.toFixed(2));
    $("#least_Bobby_conf").text("Confidence Level :   " + leastBobbyConf.toFixed(2));
    $("#least_Dale").text(leastDale);
    $("#least_Dale_conf").text("Confidence Level :   " + leastDaleConf.toFixed(2));
    $("#least_Hank").text(leastHank);
    $("#least_Hank_conf").text("Confidence Level :   " + leastHankConf.toFixed(2));
    $("#least_Peggy").text(leastPeggy);
    $("#least_Peggy_conf").text("Confidence Level " + leastPeggyConf.toFixed(2));
}

var ctx = document.getElementById("myChart").getContext("2d");

var response = {};
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

            response = data;
            var i;
            var k;
            var l;
            character_values = {};
            for (i = 0; i < data.length; i++) {
                Object.keys(data[i]).forEach(function (key) {
                    console.log(key);
                    var tweets = (data[i][key]);
                    var max = -2;
                    var maxName = "";
                    for (var k = 0; k < tweets.length; k++) {
                        var name = tweets[k][0];
                        var value = tweets[k][1];

                        if (max == -2) {
                            max = value;
                            maxName = name;
                        } else {
                            if (max < value) {
                                max = value;
                                maxName = name;
                            }
                        }
                        findmaxmin(key, name, value);
                        console.log(tweets[k][0], tweets[k][1]);
                        //Do something
                    }
                    character_values[maxName] = (character_values[maxName] || 0) + 1;
                    character_values[maxName] += parseFloat(1);
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
                    maintainAspectRatio: false,
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
                            // images: [{
                            //     src: '/static/images/hank.png',
                            //     width: :10vh,
                            //     height: 10vw
                            // },
                            //     {
                            //         src: '/static/images/dale.png',
                            //         width: 120,
                            //         height: 140
                            //     },
                            //     {
                            //         src: '/static/images/peggy.png',
                            //         width: 120,
                            //         height: 119
                            //     },
                            //     {
                            //         src: '/static/images/bobby.png',
                            //         width: 120,
                            //         height: 140
                            //     },
                            // ]
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
            buildmaxmin();
            var i = 0;
            for (i = 0; i < response.length; i++) {
                Object.keys(response[i]).forEach(function (key) {
                    var tweets = (response[i][key]);
                    buildtweettable(key, tweets);

                });

            }

        },
        error: function (data) {
            console.log('An error occurred.');
            console.log(data);
            alert("Twitter Search Error: Is the username correct? Check logs for more info");
        },
    });
});

