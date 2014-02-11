$(document).ready(function() {
    $('#id_path').change(function(){
        $('.alert').hide();
            var file = this.files[0],
                fileSizeInMegabytes = getFileSizeInMegabytes(file),
                fileLargerThan50MbsTemplate = $('#file_grt_40_mbs').html(),
                fileTooLargeTemplate = $('#file_too_large').html();
        if(fileSizeIsGreaterThan40Mbs(fileSizeInMegabytes)){
            $('form').after(fileLargerThan50MbsTemplate)
        }else if(fileSizeIsGreaterThan50Mbs(fileSizeInMegabytes)){
            $('form').after(fileTooLargeTemplate)
        }
    });


    $(function () {
        $("#id-upload-form").validate({
                rules: {
                    path: {
                    fileSize: 50
                }
            }
        });
    });

    jQuery.validator.addMethod('fileSize', function(value, element, param) {
        return this.optional(element) || (getFileSizeInMegabytes(element.files[0]) < param)
    }, "The file is too large, Please upload files not larger than 50 Megabytes");
});


function getFileSizeInMegabytes(file){
    var fileSizeInBytes = file.size / (1024*1024).toFixed(2);
    return roundOff(fileSizeInBytes, 2)
}

function fileSizeIsGreaterThan40Mbs(fileSize) {
    return fileSize >= 40 && fileSize < 50;
}

function fileSizeIsGreaterThan50Mbs(fileSize) {
    return fileSize > 50;
}

function roundOff(num, decimals) {
    return Math.round(num * Math.pow(10, decimals)) / Math.pow(10, decimals);
}
