$(document).ready(function () {
    const result_div = $('.results');
    const fileInput = $('input[name="file"]');

    $('form').submit(function (e) {
        e.preventDefault();
        // TODO Validate .wav
        let formData = new FormData(this);

        $.ajax({
            url: "/upload",
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                let response_obj = JSON.parse(response);
                let recognized_text = "";

                result_div.append('<h2>Transcription for: <b>' + fileInput.val() + '</b></h2>');
                response_obj.results.forEach(function (result) {
                    recognized_text += result.alternatives[0].transcript;
                });
                result_div.append('<p>' + recognized_text + '</p>')
            }
        });
    });
});