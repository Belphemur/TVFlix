"use strict"
(($) ->
  handleSearchRequest = (request, responseCallback) ->
    query = request.term
    $.ajax(
      type: "GET"
      data: {query:query}
      url: "/tvflix/search/shows",
      dataType: "json"
    ).success( (json) ->
      responseArray = []
      json._embedded.forEach((show) ->
        toAdd = {}
        $.extend(toAdd,show,
          showLabel: show.label
          label:show.title
          value:show.label
        )
        responseArray.push(toAdd)
      )
      responseCallback(responseArray)
    ).fail(( jqXHR ) ->
      if jqXHR.status != 404
        console.error(jqXHR)
    )

  handleSelectionShow = (event, ui) ->
    console.log(ui.item)

  $("input[data-toggle='tooltip'][type='search']").tooltip()
  $('#searchShows').autocomplete(
    source: handleSearchRequest
    minLength: 2
    select: handleSelectionShow
  )) jQuery