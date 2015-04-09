"use strict"
(($) ->
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