"use strict"
(($) ->
  ###
    Loading Screen function
  ###
  $body = $('body')
  toggleLoadingScreen = () ->
    if $body.hasClass('loading')
      $body.removeClass('loading')
    else
      $body.addClass('loading')
  ###
    Do the API Call on the search and process the results.
    AutoComplete need to have an object with value and label set
  ###
  handleSearchRequest = (request, responseCallback) ->
    query = request.term
    $.ajax(
      type: "GET"
      data: {query: query}
      url: "/tvflix/search/shows",
      dataType: "json"
      global: false
    ).success((json) ->
      responseArray = []
      json._embedded.forEach((show) ->
        toAdd = {}
        $.extend(toAdd, show,
          showLabel: show.label
          label: show.title
          value: show.title
        )
        responseArray.push(toAdd)
      )
      responseCallback(responseArray)
    ).fail((jqXHR) ->
      if jqXHR.status != 404
        console.error(jqXHR)
    )
  ###
    Retrieve an image from Google
  ###
  getImage = (title, callback) ->
    $.ajax(
      url: 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=' + title + '+poster&start=1'
      type: 'GET'
      dataType: 'jsonp'
    ).success((data)->
      callback(null, data.responseData.results[0].url)
    ).fail((XHR)->
      callback(XHR)
    )
  ###
    Set the Show information (HTML)
  ###
  setShowInformation = (item, callback) ->
    $('#startYear').text(item.start_year)
    $('#showTitle').text(item.title)
    $('#endYear').text(item.end_year)
    $('#channel').text(item.channel)
    $('#summary').text(item.summary)
    getImage(item.title, (error, imgUrl) ->
      if(error)
        console.log(error)
        $('#showImage img').attr('src', '/static/image/no-image.png')
        return callback()

      $('#showImage img').attr('src', imgUrl)
      callback()
    )


  handleSelectionShow = (event, ui) ->
    toggleLoadingScreen()
    $('#placeholder').hide()
    setShowInformation(ui.item, ()->
      $('#showContainer').fadeIn()
      setTimeout(toggleLoadingScreen, 500)
    )

  $("input[data-toggle='tooltip'][type='search']").tooltip()
  $('#searchShows').autocomplete(
    source: handleSearchRequest
    minLength: 2
    select: handleSelectionShow
  )) jQuery