$(document).ready(function () {
  const result_div = $('.results');
  const fileInput = $('input[name="file"]');
  const langInput = $('input[name="language"]');

  $('form').submit(function (e) {
    e.preventDefault();
    if (!fileInput.val()) return;

    const new_result = $("#template").clone();
    new_result.removeAttr('id');
    new_result.find("#filename").text(fileInput.val().split('\\').pop());
    const lang_label = document.querySelector("#languages option[value='"+langInput.val()+"']").text;
    new_result.find("#result-lang").text(lang_label);
    result_div.prepend(new_result);
    new_result.show();
    result_div.show();

    const formData = new FormData(this);

    $.ajax({
      url: "/upload",
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      success: function (response) {
        const response_obj = JSON.parse(response);
        let recognized_text = "";
        let confidence = 0;
        response_obj.results.forEach(function (result) {
          recognized_text += result.alternatives[0].transcript;
          confidence += result.alternatives[0].confidence;
        });
        new_result.find(".loader").replaceWith('<p>' + recognized_text + '</p>');
        new_result.find("progress").val(confidence / response_obj.results.length);
        jsonTree.create(response_obj, new_result.find('#response')[0]);
        new_result.find(".success").show();
      },
      error: function (xhr, status, error) {
        const header = new_result.find("h2");
        header.text(header.text().replace('Transcription for', 'Error for'))
        new_result.find(".loader").replaceWith('<p class="error">' + xhr.responseText + '</p>')
      }
    });
  });
});