var result_div = null, fileInput = null, langInput = null;

$(document).ready(function () {
  result_div = $('.results');
  fileInput = $('input[name="files"]');
  langInput = $('input[name="language"]');

  $('#form-api').submit(function (e) {
    e.preventDefault();
    if (!fileInput.val()) return;

    for (file of fileInput[0].files) {
      transcribe_file(this, file);
    }
    result_div.show();
  });
});

function transcribe_file(form, file) {
  const new_result = $("#template").clone();
  const lang_label = document.querySelector("#languages option[value='" + langInput.val() + "']").text;

  new_result.removeAttr('id');
  new_result.find("#filename").text(file.name);
  new_result.find("#result-lang").text(lang_label);
  new_result.find("audio")[0].src = URL.createObjectURL(file);

  result_div.prepend(new_result);
  new_result.show();

  const formData = new FormData(form);
  formData.append('file', file);

  $.ajax({
    url: "/api/upload/",
    type: "POST",
    data: formData,
    processData: false,
    contentType: false,
    success: response => load_result(response, new_result),
    error: function (xhr, status, error) {
      new_result.find("h2").append('<span>Error</span>');
      new_result.find(".loader").replaceWith('<p class="error">' + xhr.responseText + '</p>')
    }
  });
}

function load_result(response, new_result) {
  const response_obj = JSON.parse(response);

  let recognized_text = "";
  let confidence = 0;
  const results = response_obj.results ? response_obj.results : [];
  results.forEach(function (result) {
    recognized_text += result.alternatives[0].transcript;
    confidence += result.alternatives[0].confidence;
  });
  new_result.find(".loader").replaceWith('<p>' + recognized_text + '</p>');
  new_result.find("progress").val(confidence / Math.max(results.length, 1));
  jsonTree.create(response_obj, new_result.find('#response')[0]);

  initButtons(new_result);

  new_result.find(".success").show();
}

function initButtons(result) {
  const audio = result.find("audio")[0];
  const play_btn = result.find("button[name='play']");
  const mute_btn = result.find("button[name='mute']");

  audio.onended = event => pause(play_btn, audio);
  play_btn.click(e => audio.paused ? play(play_btn, audio) : pause(play_btn, audio));
  mute_btn.click(e => mute(mute_btn, audio));
}

function play(button, audio) {
  $(button).find("i").addClass('fa-pause').removeClass('fa-play');
  audio.play()
}

function pause(button, audio) {
  $(button).find("i").removeClass('fa-pause').addClass('fa-play');
  audio.pause()
}

function mute(button, audio) {
  let icon = $(button).find("i");
  icon.removeClass('fa-volume-off').removeClass('fa-volume-up');
  audio.muted = !audio.muted;
  audio.muted ? icon.addClass('fa-volume-up') : icon.addClass('fa-volume-off');
}