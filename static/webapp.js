$(document).ready(function () {
  const result_div = $('.results');
  const fileInput = $('input[name="file"]');

  $('form').submit(function (e) {
    e.preventDefault();
    if (!fileInput.val()) return;

    const new_result = $("#template").clone();
    new_result.removeAttr('id');
    new_result.find("#filename").text(fileInput.val().split('\\').pop());
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
        response_obj.results.forEach(function (result) {
          recognized_text += result.alternatives[0].transcript;
        });
        new_result.find(".loader").replaceWith('<p>' + recognized_text + '</p>')

        const tree_wrapper = new_result.find('#response')[0];
        console.log(tree_wrapper)
        jsonTree.create(response_obj, tree_wrapper);
      },
      error: function (xhr, status, error) {
        const header = new_result.find("h2");
        header.text(header.text().replace('Transcription for', 'Error for'))
        new_result.find(".loader").replaceWith('<p class="error">' + xhr.responseText + '</p>')
      }
    });
  });
});