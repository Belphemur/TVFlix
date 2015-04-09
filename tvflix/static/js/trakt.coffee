"use strict"
traktClientId = "2d40da7a6e42cd29c4b9bbef14e7acc208fc9c27c90a8242718f45effc4c73f6"
traktApiRoot = 'http://api.staging.trakt.tv'

(($) ->
  ###
    Make request to the trakt API
  ###
  traktRequest = (endpoint, type) ->
    type = type ? 'GET'
    return $.ajax(
      url: traktApiRoot + endpoint
      type: type
      dataType: 'json'
      headers:
        'trakt-api-key': traktClientId
        'trakt-api-version': 2
    )
    root = window ? this
    root.traktRequest = traktRequest
) jQuery