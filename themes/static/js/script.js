$(document).ready(function() {

  function toastMe(msg, time) {
    $(".toastMe").html(msg);
    $(".toastMe").removeClass("toastHide");
    $(".toastMe").removeClass("animated fadeOut");
    $(".toastMe").addClass("animated fadeIn");
    setTimeout(function(){$(".toastMe").removeClass("animated fadeIn");$(".toastMe").addClass("animated fadeOut");}, time);
  }

  $(document).on("click", ".themeString", function() {
    var $temp = $("<input>");
    $("body").append($temp);
    $temp.val($.trim($(this).text().replace('$ ', ''))).select();
    document.execCommand("copy");
    toastMe('copied to clipboard', 2000);
    $temp.remove();
  });

  function downloadZIP() {
    var zip = new JSZip();
    var readme = 'You downloaded a new t-ui theme.\r\n\r\nTo apply:\r\n$ theme -zipapply theme.zip\r\n\r\nOtherwise, you can extract manually the xml files and move them into the t-ui folder.\r\n\r\nHappy theming!';
    zip.file("Readme.txt", readme);
    zip.file("theme.xml", getXmlString(themeXML, "theme"));
    zip.file("suggestions.xml", getXmlString(suggestionsXML, "suggestions"));
    zip.generateAsync({
        type: "blob"
      })
      .then(function(blob) {
        saveAs(blob, "theme.zip");
      });
  }

  function getXmlString(arr, type, i = 1, flag = false) {
    var sp = "";
    var xmlString = '<?xml version="1.0" encoding="utf-8" ?>\r\n';
    xmlString += '<' + type + '>\r\n';
    for (var j = 0; j <= i; j++) {
      sp += " ";
    }
    $.each(arr, function(key, val) {
      xmlString += sp + "<" + key;
      if ($.isArray(val)) {
        if (!flag) {
          xmlString += ">\r\n";
        }
        artoxml(val, i + 5);
        xmlString += sp + "</" + key + ">\r\n";
      } else {
        xmlString += " value='" + val + "'/>\r\n";
      }
    });
    return xmlString + '</' + type + '>\r\n';
  }

  // pack a themeXML and a suggestionsXML dict
  function generateObj(themeElement) {
    themeXML = {};
    suggestionsXML = {};
    // counts the number of non-default options
    changeCounter = 0;

    // gather values from theme.xml inputs
    $('label', $('.themexml')).each(function() {
      var forVal = $(this).attr('for');

      // the current value of the jscolor input
      var siblingVal = $(this).siblings("[class='jscolor']").val();
      // default value
      var siblingDefaultVal = $(this).siblings("[class='jscolor']").attr('defaultValue');

      if(siblingVal != siblingDefaultVal) {
        themeXML[forVal] = '#' + siblingVal;
        changeCounter++;
      }
    });

    // gather values from suggestions.xml inputs
    var enabled = $("[value='show_suggestions']").prop('checked');
    suggestionsXML['show_suggestions'] = enabled;
    if(enabled) {
      var transparent = $("[value='transparent_suggestions']").prop('checked');
      suggestionsXML['transparent_suggestions'] = transparent;

      $('label', $('.suggestionsxml')).each(function() {
        var forVal = $(this).attr('for');
        if(transparent && forVal.includes('bg')) return;
        else {
          var siblingVal = $(this).siblings("[class='jscolor']").val();
          var siblingDefaultVal = $(this).siblings("[class='jscolor']").attr('defaultValue');

          if(siblingVal != siblingDefaultVal) {
            suggestionsXML[forVal] = '#' + siblingVal;
            changeCounter++;
          }
        }
      });
    }
  }

  $("#publish-online").on('click', function() {
    $('.user-form').css("display", "block");
    $('.links').css("display", "none");
  });

  $("#cancelSendData").on('click', function() {
    $('.user-form').css("display", "none");
    $('.saved').css("display", "none");
    $('.links').css("display", "block");
  });

  $("#zip-download, #zip-download-published").on('click', function() {
    generateObj();
    downloadZIP();
    $('.user-form').css("display", "none");
    $('.links').css("display", "block");
  });

  // checks if the theme name is good
  function checkname(response)
  {
    var name = $("#theme_name").val();
    var theme_name_used = response.includes(name);
    if(name.length<5) {
      $('.themeString code pre').text("Theme name must be 5 characters long.").css("color","#FF0000");
      $('.saved').css("display", "block");
      $('#cancelSendData').css("display", "inline-block");
    }
    else if(!isNaN(name.charAt(0))) {
      $('.themeString code pre').text("Theme name cannot start with a Number.").css("color","#FF0000");
      $('.saved').css("display", "block");
      $('#cancelSendData').css("display", "inline-block");
    }
    else if(theme_name_used) {
      $('.themeString code pre').text("Theme name already used try a different name.").css("color","#FF0000");
      $('.saved').css("display", "block");
      $('#cancelSendData').css("display", "inline-block");
    }
    else {
      var files = {};
      generateObj();
      files["SUGGESTIONS"] = suggestionsXML;
      files["THEME"] = themeXML;
      if(changeCounter>3){
//        console.log(changeCounter);
        $.ajax({
          url: "./test.php",
          type: "POST",
          data: {"author_name":$("#author_name").val(),"downloads":0,"files":files,"name":name,"published":true},
          datatype: 'json',
          success: function(result) {
            $('.themeString code pre').text(result).css("color","#14FF00");
            $('#sendData').css("display", "none");
            $('#cancelSendData').css("display", "none");
          },
          error: function(xhr, resp, text) {
            $('.themeString code pre').text("Error sending data. Please try again.").css("color","#FF0000");
            $('#cancelSendData').css("display", "inline-block");
          }
        });
        $('.saved').css("display", "block");
      }
      else {
        $('.themeString code pre').text("Few more customizations needed to qualify for Publishing.").css("color","#FF0000");
        $('.saved').css("display", "block");
        $('#cancelSendData').css("display", "inline-block");
      }
    }
  }

  $("#sendData").on('click', function() {
    var name = $("#theme_name").val();
    $.ajax({
      url: "./show_data.php",
      type: "POST",
      data: {"data_type":"json","theme_list":"view"},
      datatype: 'json',
      success: checkname,
      error: function(xhr, resp, text) {
        $('.themeString code pre').text("Error sending data. Please try again.").css("color","#FF0000");
        $('#cancelSendData').css("display", "inline-block");
      }
    });
  });

  $("[type='checkbox']").on('click change', function() {
    var value = $(this).prop('value');
    var checked = $(this).prop('checked');

    if(value == "show_suggestions") {
      var show;
      if(checked) show = "block";
      else show = "none";

      $(".suggestions").css("display", show);
    } else if(value == "transparent_suggestions") {
      if(!checked) {
        $(".box").css("background-color", "");
        $(this).parents('div.pallet').find("[class='jscolor']").each(function() {
          $(this).trigger('change');
        });
      } else {
        $(".box").css("background-color", "transparent");
      }
    }
  });

  // triggered whenever a color is changed
  $("[class='jscolor']").on('keyup keypress blur change', function() {
    var _color = this.value;

    // for each label, find the label specified in 'for' and change the corresponding property
    $(this).siblings('label').each(function() {
      var finalClass = $(this).attr('for');

      // if it's a bg...
      if (finalClass.match(/bg/g) == 'bg') {
        $("." + finalClass).css("background-color", _color);
      }
      // if it's a text color...
      else {
        $("." + finalClass).css("color", _color);
      }
      $(this).parents('div.swatch').css("background-color", _color);
    });
  });
});
