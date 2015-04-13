"use strict"
(($)->
  ###
    FUNCTION BLOCK
  ###
  ###
      Retrieve an image from Trakt
  ###
  getShowImage = (label, callback) ->
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
  loadShow = (item, callback) ->
    $("#show").attr('data-url', item._links.self.href)
    $("#showComments").attr('data-url', item._links.comments.href)
    $('#startYear').text(item.start_year)
    $('#showTitle').text(item.title)
    $('#endYear').text(item.end_year)
    $('#channel').text(item.channel)
    $('#summary').text(item.summary)
    $("#show").trigger("show.loaded")
    getShowImage(item.showLabel, (error, imgUrl) ->
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
  displaySeasons = (seasons) ->
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
  loadSeasons = (show, callback) ->
    seasonList = $("#showSeasons ul")
    seasonList.html('')
    $.ajax(
      url: show._links.seasons.href
      type: 'GET'
      dataType: 'json'
    ).success((data)->
      displaySeasons(data._embedded.season)
    ).complete(() ->
      callback()
    )

  ###
    Get Image URL from the trakt data
  ###
  getEpImage = (traktInfo, episodeNumber) ->
    imgUrl = null
    traktInfo.every((episode) ->
      if(episode.number == episodeNumber)
        imgUrl = episode.images.screenshot.thumb;
        return false

      return true
    )
    return imgUrl

  ###
    Create the DOM element for an episode using the template given in
    the HTML code (#episodeTemplate)
  ###
  displayEpisodes = (episodes, traktInfo) ->
    $template = $("#episodeTemplate")
    $episodes = $("#showEpisodes").html('')
    nb = 0
    totalAdded = 0
    totalEpisode = episodes.length
    $rowTemplate = $('<div class="row"></div>')
    $row = $rowTemplate.clone()
    episodes.forEach((episode) ->
      $newEp = $template.clone()

      if(traktInfo)
        imageUrl = getEpImage(traktInfo, episode.number)
        if(imageUrl)
          $newEp.find("div.thumb img").attr('src', imageUrl)

      $newEp.attr('id', 'ep-' + episode.number)
      $newEp.find("h2").text(episode.title)
      $newEp.find("div.summary").text(episode.summary)
      $newEp.find("span.epBcast").text(episode.bcast_date)
      $newEp.find("span.epNumber").text(episode.number)
      $newEp.addClass('col-md-6')
      $newEp.removeClass('invisible')
      $row.append($newEp)
      if(++nb %2 == 0 || ++totalAdded == totalEpisode)
        $episodes.append($row)
        $row = $rowTemplate.clone()
    )


  displayComments = (comments) ->
    $comments = $("#showComments").html('')
    comments.forEach((comment) ->
      createComment(comment)
    )

  ###
    Load the comments for the show
  ###
  loadComments = (show, callback) ->
    $.ajax(
      url: show._links.comments.href
      type: 'GET'
      dataType: 'json'
    ).success((data)->
      displayComments(data._embedded.comment)
    ).fail(() ->
      $("#showComments").trigger("comment.no-comments")
    ).complete(() ->
      callback()
    )

  ###
    EVENTS
  ###

  $("#show").on('show.loaded', () ->
    $("#showEpisodes").html('')
  )

  ###
    LINK BLOCK
  ###
  $('#showSeasons').on('click', 'a.season', (e) ->
    e.preventDefault()
    toggleLoadingScreen()
    $link = $(e.target)
    url = $link.attr('data-episodes')
    traktUrl = url.replace('/tvflix', '') + '?extended=images'
    $.ajax(
      url: url
      type: 'GET',
      dataType: 'json'
    ).success((data) ->
      traktRequest(traktUrl).success((traktData) ->
        displayEpisodes(data._embedded.episode, traktData)
        setTimeout(toggleLoadingScreen, 500)
      ).fail(() ->
        displayEpisodes(data._embedded.episode)
        setTimeout(toggleLoadingScreen, 500)
      )
    ).fail(toggleLoadingScreen)
  )
  root = window ? this
  $.extend(root,
    loadShow: loadShow
    loadSeasons: loadSeasons
    loadComments: loadComments
  )) jQuery