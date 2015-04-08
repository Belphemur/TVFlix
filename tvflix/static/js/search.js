// Generated by CoffeeScript 1.9.1
(function() {
  "use strict";
  (function($) {
    var $body, getImage, handleSearchRequest, handleSelectionShow, setShowInformations, toggleLoading;
    $body = $('body');
    toggleLoading = function() {
      if ($body.hasClass('loading')) {
        return $body.removeClass('loading');
      } else {
        return $body.addClass('loading');
      }
    };
    handleSearchRequest = function(request, responseCallback) {
      var query;
      query = request.term;
      return $.ajax({
        type: "GET",
        data: {
          query: query
        },
        url: "/tvflix/search/shows",
        dataType: "json",
        global: false
      }).success(function(json) {
        var responseArray;
        responseArray = [];
        json._embedded.forEach(function(show) {
          var toAdd;
          toAdd = {};
          $.extend(toAdd, show, {
            showLabel: show.label,
            label: show.title,
            value: show.title
          });
          return responseArray.push(toAdd);
        });
        return responseCallback(responseArray);
      }).fail(function(jqXHR) {
        if (jqXHR.status !== 404) {
          return console.error(jqXHR);
        }
      });
    };
    getImage = function(title, callback) {
      return $.ajax({
        url: 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=' + title + '+poster&start=4',
        type: 'GET',
        dataType: 'jsonp'
      }).success(function(data) {
        return callback(data.responseData.results[1].url);
      }).fail(function(XHR) {
        callback();
        return console.error(XHR);
      });
    };
    setShowInformations = function(item, callback) {
      $('#startYear').text(item.start_year);
      $('#showTitle').text(item.title);
      $('#endYear').text(item.end_year);
      $('#channel').text(item.channel);
      $('#summary').text(item.summary);
      return getImage(item.title, function(imgUrl) {
        $('#showImage img').attr('src', imgUrl);
        return callback();
      });
    };
    handleSelectionShow = function(event, ui) {
      toggleLoading();
      $('#placeholder').hide();
      return setShowInformations(ui.item, function() {
        $('#showContainer').fadeIn();
        return setTimeout(toggleLoading, 500);
      });
    };
    $("input[data-toggle='tooltip'][type='search']").tooltip();
    return $('#searchShows').autocomplete({
      source: handleSearchRequest,
      minLength: 2,
      select: handleSelectionShow
    });
  })(jQuery);

}).call(this);

//# sourceMappingURL=search.js.map