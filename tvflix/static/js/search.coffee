"use strict"
(($) ->
  $body = $('body')
  toggleLoading = () ->
    if $body.hasClass('loading')
      $body.removeClass('loading')
    else
      $body.addClass('loading')

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

  getImage = (title, callback) ->
    $.ajax(
      url: 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q='+title+'+poster&start=4'
      type: 'GET'
      dataType: 'jsonp'
    ).success((data)->
      callback(data.responseData.results[1].url)
    ).fail((XHR)->
      callback()
      console.error(XHR)
    )
  setShowInformations = (item, callback) ->
    $('#startYear').text(item.start_year)
    $('#showTitle').text(item.title)
    $('#endYear').text(item.end_year)
    $('#channel').text(item.channel)
    $('#summary').text(item.summary)
    getImage(item.title, (imgUrl) ->
      $('#showImage img').attr('src', imgUrl)
      callback()
    )


  handleSelectionShow = (event, ui) ->
    toggleLoading()
    $('#placeholder').hide()
    setShowInformations(ui.item, ()->
      $('#showContainer').fadeIn()
      setTimeout(toggleLoading, 500)
    )

  $("input[data-toggle='tooltip'][type='search']").tooltip()
  $('#searchShows').autocomplete(
    source: handleSearchRequest
    minLength: 2
    select: handleSelectionShow
  )) jQuery