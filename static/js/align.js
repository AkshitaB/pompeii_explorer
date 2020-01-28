
//load from saved file.
// var curr_overall_idx = '{{ start_idx }}'; // -1
// var curr_pic_idx = -1
// var curr_text_idx = -1

console.log("curr_idx")
console.log(curr_overall_idx)

document.onkeyup = function(e) {
    if (e.which == 37) {
        get_data_by_idx(false);
    }
    else if (e.which == 39) {
        get_data_by_idx(true);
    }
    else if (e.which == 83) {
        save_progress();
    }
    else if (e.which == 82) {
        reload();
    }
    //console.log(print(e.which))
}

function setPicture(image_data, image_path) {
    console.log('setting picture...');
    console.log(image_path);
    document.getElementById("image").src = image_data;
    $("#image_path").text(image_path);
}

function setWholePage(image_data) {
    console.log('setting page...');
    console.log(image_path);
    document.getElementById("whole_page").src = image_data;
}

function setText(text) {
    $("#image_text").text(text);
}

function setPhotoNegative(negative) {
    $("#image_negative").val(negative);
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
        url: "/get_data_by_index",
        data: {'curr_idx': idx},
        success: function (data) {
            //alert(data);
            //console.log('got data...')
            //console.log(data)
            setPicture(data['image_data'], data['image_path']);
            setText(data['raw_text']);
            setWholePage(data['page_image']);
            curr_overall_idx = idx;
            curr_pic_idx = idx;
            curr_text_idx = idx;
            //$("#curr_idx").text(idx);
        },
        error: function(xhr, status, error) {
            console.log(error)
            alert('Error. Check console log.')
        }
    });

}

function get_image_by_idx(next) {
    console.log('Get image by id')
    console.log(next)
    if (next==true) {
        var idx = curr_pic_idx + 1;
    }
    else {
        var idx = curr_pic_idx - 1; //previous
    }

    $.ajax({
        type: "GET",
        url: "/get_data_by_index",
        data: {'curr_idx': idx},
        success: function (data) {
            //alert(data);
            //console.log('got data...')
            setPicture(data['image_data'], data['image_path']);
            //setText(data['text']);
            curr_pic_idx = idx;
        },
        error: function(xhr, status, error) {
            console.log(error)
            alert('Error. Check console log.')
        }
    });

}

function get_text_by_idx(next) {
    console.log('Get text by id')
    console.log(next)
    if (next==true) {
        var idx = curr_text_idx + 1;
    }
    else {
        var idx = curr_text_idx - 1; //previous
    }

    $.ajax({
        type: "GET",
        url: "/get_data_by_index",
        data: {'curr_idx': idx},
        success: function (data) {
            //alert(data);
            //console.log('got data...')
            //setPicture(data['image_data']);
            setText(data['raw_text']);
            curr_text_idx = idx;
        },
        error: function(xhr, status, error) {
            console.log(error)
            alert('Error. Check console log.')
        }
    });

}

function save_alignment() {

    //assert that at least one of the idx matches the overall idx, to avoid errors.

    console.log('Curr Pic Idx', curr_pic_idx)
    console.log('Curr Text Idx', curr_text_idx)
    console.log('Curr Overall Idx', curr_overall_idx)
    if (curr_pic_idx > curr_text_idx) {
        var col_to_shift = 'text';
        var shift_by = curr_pic_idx - curr_overall_idx;
        var shift_at = curr_text_idx;
        var idx_to_set = curr_pic_idx;
    }
    else {
        var col_to_shift = 'image';
        var shift_by = curr_text_idx - curr_overall_idx;
        var shift_at = curr_pic_idx;
        var idx_to_set = curr_text_idx;
    }

    if (shift_by !== 0) {
        console.log('Save alignment')
        $.ajax({
        type: "GET",
        url: "/shift_alignment",
        data: {'col_to_shift': col_to_shift, 'shift_by': shift_by, 'shift_at': shift_at},
        success: function (data) {
            //alert(data);
            //console.log('got data...')
            //setPicture(data['image_data']);
            //setText(data['text']);
            curr_overall_idx = idx_to_set;
            curr_pic_idx = idx_to_set;
            curr_text_idx = idx_to_set;
            notify("Saved");
        },
        error: function(xhr, status, error) {
            console.log(error)
            alert('Error. Check console log.')
        }
    });
    }
    else {
        var idx = curr_overall_idx + 1;

        $.ajax({
            type: "GET",
            url: "/get_data_by_index",
            data: {'curr_idx': idx},
            success: function (data) {
                console.log(data)
                //alert(data);
                //console.log('got data...')
                setPicture(data['image_data'], data['image_path']);
                setText(data['raw_text']);
                setWholePage(data['page_image']);
                curr_overall_idx = idx;
                curr_pic_idx = idx;
                curr_text_idx = idx;
                //$("#curr_idx").text(idx);
            },
            error: function(xhr, status, error) {
                console.log(error)
                alert('Error. Check console log.')
            }
        });
    }
}

function save_progress() {
    console.log("Saving progress until " + curr_overall_idx);
    $.ajax({
            type: "GET",
            data: {'curr_idx': curr_overall_idx},
            url: "/save_progress",
            success: function (data) {
                notify("Saved progress on disk");
            },
            error: function(xhr, status, error) {
                console.log(error)
                alert('Error. Check console log.');
            }
        });
}

function reload() {
    console.log("Reloading " + curr_overall_idx);
    $.ajax({
            type: "GET",
            url: "/reload",
            success: function (data) {
                notify("Reloaded csv from disk");
                var idx = data['index_to_load'] - 1;
                curr_overall_idx = idx;
                curr_pic_idx = idx;
                curr_text_idx = idx;

            },
            error: function(xhr, status, error) {
                console.log(error)
                alert('Error. Check console log.');
            }
        });
}