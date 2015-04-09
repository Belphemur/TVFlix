"use strict"
(($) ->
  $body = $('body')
  ###
    Loading Screen function
  ###
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
    Retrieve an image from Trakt
  ###
  getImage = (label, callback) ->
    traktRequest('/shows/' + label + '?extended=images')
    .success((data)->
      callback(null, data.images.thumb.full)
    )
    .fail((XHR)->
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
    getImage(item.showLabel, (error, imgUrl) ->
      if(error)
        console.log(error)
        $('#showImage img').attr('src', '/static/image/no-image.png')
        return callback()

      $('#showImage img').attr('src', imgUrl)
      callback()
    )
  ###
    Set the HTML with the sessions information
  ###
  handleSeasonInformation = (seasons) ->
    seasonList = $("#showSeasons ul")
    seasons.forEach((season) ->
      link = $('<a>',
        class: 'season'
        href: '#'
        'data-episodes': season._links.episode.href
      ).text('Season ' + season.number)
      li = $('<li>').html(link)
      seasonList.append(li)
    )
  ###
    Do the request to get season information
  ###
  setSeasonInformation = (item, callback) ->
    seasonList = $("#showSeasons ul")
    seasonList.html('')
    $.ajax(
      url: item._links.seasons.href
      type: 'GET'
      dataType: 'json'
    ).success((data)->
      handleSeasonInformation(data._embedded.season)
    ).complete(() ->
      callback()
    )


  handleSelectionShow = (event, ui) ->
    toggleLoadingScreen()
    $('#placeholder').hide()
    setShowInformation(ui.item, () ->
      setSeasonInformation(ui.item, () ->
        $('#showContainer').fadeIn()
        setTimeout(toggleLoadingScreen, 500)
      )
    )

  $("input[data-toggle='tooltip'][type='search']").tooltip()
  $('#searchShows').autocomplete(
    source: handleSearchRequest
    minLength: 2
    select: handleSelectionShow
  )
) jQuery