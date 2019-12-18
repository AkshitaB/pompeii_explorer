
//load from saved file.
// var curr_overall_idx = '{{ start_idx }}'; // -1
// var curr_pic_idx = -1
// var curr_text_idx = -1

console.log("curr_idx")
console.log(curr_overall_idx)

document.onkeyup = function(e) {
    if (e.which == 77) {
        mark_page();
    }
    else if (e.which == 85) {
        unmark_page();
    }
    //console.log(print(e.which))
}

function setPicture(image_data, image_path) {
    console.log('setting picture...');
    console.log(image_path);
    document.getElementById("image").src = image_data;
    $("#image_path").text(image_path);
}

function setWholePage(image_data, image_path) {
    console.log('setting page...');
    console.log(image_path);
    document.getElementById("whole_page").src = image_data;
    $("#raw_image_path").text(image_path);
}

function notify(message) {
    var notification = document.querySelector('.mdl-js-snackbar');
    var data = {
      message: message,
      //actionHandler: function(event) {},
      //actionText: 'Undo',
      timeout: 1000
    };
    notification.MaterialSnackbar.showSnackbar(data);
}

function get_data_by_idx(next) {

    //save_alignment();
    console.log('Get data by id')
    console.log(next)
    if (next==true) {
        var idx = curr_overall_idx + 1;
    }
    else {
        var idx = curr_overall_idx - 1; //previous
    }

    $.ajax({
        type: "GET",
        url: "/get_raw_data_by_index",
        data: {'curr_idx': idx},
        success: function (data) {
            //alert(data);
            //console.log('got data...')
            setPicture(data['image_data'], data['image_path']);
            setWholePage(data['page_image'], data['page_path']);
            curr_overall_idx = idx;
        },
        error: function(xhr, status, error) {
            console.log(error)
            alert('Error. Check console log.')
        }
    });

}


function mark_page() {
    var image_path = $("#raw_image_path").text();
    //var page = image_path.replace('page_', '').replace('.jpg').split('_')[0];
    console.log("Marking page " + image_path);
    $.ajax({
            type: "GET",
            data: {'page': image_path},
            url: "/mark_page",
            success: function (data) {
                notify("Marked "+image_path);
            },
            error: function(xhr, status, error) {
                console.log(error)
                alert('Error. Check console log.');
            }
        });
}

function unmark_page() {
    var image_path = $("#raw_image_path").text();
    //var page = image_path.replace('page_', '').replace('.jpg').split('_')[0];
    console.log("Marking page " + image_path);
    $.ajax({
            type: "GET",
            data: {'page': image_path},
            url: "/unmark_page",
            success: function (data) {
                notify("Unarked "+image_path);
            },
            error: function(xhr, status, error) {
                console.log(error)
                alert('Error. Check console log.');
            }
        });
}

function save_progress() {
    console.log("Saving progress until " + curr_overall_idx);
    $.ajax({
            type: "GET",
            data: {'curr_idx': curr_overall_idx},
            url: "/save_raw_progress",
            success: function (data) {
                notify("Saved progress on disk");
            },
            error: function(xhr, status, error) {
                console.log(error)
                alert('Error. Check console log.');
            }
        });
}