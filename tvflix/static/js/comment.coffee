"use strict"
(($)->
  $comments = $("#showComments")
  $template = $("#commentTemplate")
  user = User.getCurrentUser()
  $commentManager = $('<div class="commentManager"><button class="btn btn-default edit"><span class="glyphicon glyphicon-edit"></span></button> <button class="btn btn-danger delete"><span class="glyphicon glyphicon-remove"></span></button></div>')

  handleAddedComment = (event, jQueryObject) ->
    if(jQueryObject.attr('data-username') != user.name)
      return
    jQueryObject.append($commentManager)

  handleUserLogout = (event) ->
    $comments.find('.comment .commentManager').remove()

  handleUserLogin = (event) ->
    $comments.find('.comment').each(() ->
      handleAddedComment(null, $(this))
    )

  createComment = (comment) ->
    $newComment = $template.clone()
    $newComment.attr('id', 'com-' + comment.username)
    $newComment.attr('data-username', comment.username)
    $newComment.find("h3").text(comment.username)
    $newComment.find("div.avatar img").attr('src', '//robohash.org/' + comment.username + '?set=set3&size=60x60')
    $newComment.find("p").text(comment.comment)
    $newComment.removeClass('invisible')


  $comments.on('comment.added', handleAddedComment)
  $(user).on('user.logout', handleUserLogout)
  $(user).on('user.login', handleUserLogin)

  root = window ? this
  root.createComment = createComment
) jQuery