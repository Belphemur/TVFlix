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

  root = window ? this
  root.toggleLoadingScreen = toggleLoadingScreen
) jQuery