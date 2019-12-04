
//load from saved file.
var curr_overall_idx = -1
var curr_pic_idx = -1
var curr_text_idx = -1

function setPicture(image_data) {
    //console.log('setting picture...');
    document.getElementById("image").src = image_data;
}

function setText(text) {
    $("#image_text").text(text);
}

function setPhotoNegative(negative) {
    $("#image_negative").val(negative);
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
            setPicture(data['image_data']);
            setText(data['text']);
            curr_overall_idx = idx;
            curr_pic_idx = idx;
            curr_text_idx = idx;
            //$("#curr_idx").text(idx);
        },
        error: function(xhr, status, error) {
            console.log(error)
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
            setPicture(data['image_data']);
            //setText(data['text']);
            curr_pic_idx = idx;
        },
        error: function(xhr, status, error) {
            console.log(error)
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
            setText(data['text']);
            curr_text_idx = idx;
        },
        error: function(xhr, status, error) {
            console.log(error)
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
        },
        error: function(xhr, status, error) {
            console.log(error)
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
                //alert(data);
                //console.log('got data...')
                setPicture(data['image_data']);
                setText(data['text']);
                curr_overall_idx = idx;
                curr_pic_idx = idx;
                curr_text_idx = idx;
                //$("#curr_idx").text(idx);
            },
            error: function(xhr, status, error) {
                console.log(error)
            }
        });
    }
}