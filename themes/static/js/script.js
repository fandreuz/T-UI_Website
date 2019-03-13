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

  function generateObj() {
    themeXML = {};
    suggestionsXML = {};
    changeCounter = 0;
    $('label', $('.themexml')).each(function() {
      var forVal = $(this).attr('for');
      var siblingVal = $(this).siblings("input[type=color]").val();
      var siblingDefaultVal = $(this).siblings("input[type=color]").attr('defaultValue');
      var rgbaCol = 'rgba(' + parseInt(siblingVal.slice(-6, -4), 16) + ',' + parseInt(siblingVal.slice(-4, -2), 16) + ',' + parseInt(siblingVal.slice(-2), 16) + ',1)';
//      console.log(rgbaCol+" != "+siblingDefaultVal);
      if(rgbaCol != siblingDefaultVal) {
        themeXML[forVal] = siblingVal;
        if (forVal == 'overlay_color') {
          themeXML[forVal] += (Math.round(Number($(this).siblings("input[type=hidden]").val()) * 255)).toString(16);
        }
      changeCounter++;
      }
    });
    $('label', $('.suggestionsxml')).each(function() {
      if ($(this).attr('for') == 'enabled') {
        if ($(this).html() == 'enabled true') {
          suggestionsXML['show_suggestions'] = true;
        } else {
          suggestionsXML['show_suggestions'] = false;
        }
      } else if ($(this).attr('for') == 'transparent') {
        if ($(this).html() == 'transparent true') {
          suggestionsXML['transparent_suggestions'] = true;
        } else {
          suggestionsXML['transparent_suggestions'] = false;
        }
      } else {
        var forVal = $(this).attr('for');
        var siblingVal = $(this).siblings("input[type=color]").val();
        var siblingDefaultVal = $(this).siblings("input[type=color]").attr('defaultValue');
        var rgbaCol = 'rgba(' + parseInt(siblingVal.slice(-6, -4), 16) + ',' + parseInt(siblingVal.slice(-4, -2), 16) + ',' + parseInt(siblingVal.slice(-2), 16) + ',1)';
//        console.log(rgbaCol+" != "+siblingDefaultVal);
        if(rgbaCol != siblingDefaultVal) {
          suggestionsXML[forVal] = siblingVal;
          changeCounter++;
        }
      }
    });
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
//    $('#publish-online').css("display", "none");
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

  $(".checkbox").on('click change', function() {
    var getLabel = $(this).find("label");
    var getLabelValue = getLabel.html();
    var elementCurrentState = getLabelValue.split(" ");
    if (elementCurrentState[0] == 'enabled') {
      if (elementCurrentState[1] == 'true') {
        $(getLabel).html(elementCurrentState[0] + " false");
        $(".suggestions").css("display", "none");
      } else if (elementCurrentState[1] == 'false') {
        $(getLabel).html(elementCurrentState[0] + " true");
        $(".suggestions").css("display", "block");
      }
    } else if (elementCurrentState[0] == 'transparent') {
      if (elementCurrentState[1] == 'true') {
        $(getLabel).html(elementCurrentState[0] + " false");
        $(".box").css("background-color", "");
        $(this).parents('div.pallet').find("input[type=color]").each(function() {
          $(this).trigger('change');
        });
      } else if (elementCurrentState[1] == 'false') {
        $(getLabel).html(elementCurrentState[0] + " true");
        $(".box").css("background-color", "transparent");
      }
    }
  });

  function getAllEvents(element) {
    console.log(element)
    var result = [];
    for (var key in element) {
        console.log(key)
        if (key.indexOf('on') === 0) {
            result.push(key.slice(2));
        }
    }
    return result.join(' ');
  }

  $("[class='jscolor']").on('OnChange onchange change onChange onFineChange finechange FineChange', function() {
    console.log('chhh')

    var _color = this.value;
    console.log(_color)

    // for each label, find the label specified in 'for' and change the corresponding property
    $(this).siblings('label').each(function() {
      console.log('imhere')

      var finalClass = $(this).attr('for');

      // if it's a bg...
      if (finalClass.match(/bg/g) == 'bg') {
        console.log('now here')

        $("." + finalClass).css("background-color", _color);
      }
      // if it's a text color...
      else {
        console.log('hehe')

        $("." + finalClass).css("color", _color);
      }
      //$(this).parents('div.swatch').css("background-color", finalColor);

      console.log('end')
    });
  });
});
