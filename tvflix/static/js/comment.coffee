"use strict"
(($)->
  $comments = $("#showComments")
  $template = $("#commentTemplate")
  $addButton = $('#showCommentsContainer button.add')
  user = User.getCurrentUser()
  $commentManager = $('<div class="commentManager"><button class="btn btn-default edit"><span class="glyphicon glyphicon-edit"></span></button> <button class="btn btn-danger delete"><span class="glyphicon glyphicon-remove"></span></button></div>')

  ###
    Check if the comment need to have its managing button
  ###
  handleAddedComment = (event, jQueryObject) ->
    if(jQueryObject.attr('data-username') != user.name)
      return
    $addButton.prop('disabled', true)
    jQueryObject.append($commentManager)
  ###
    Remove all managing button if the user logout
  ###
  handleUserLogout = (event) ->
    $comments.find('.comment .commentManager').remove()
    $addButton.prop('disabled', false)

  ###
    Check if the user have a comment for the current show and add the managing button
  ###
  handleUserLogin = (event) ->
    $comments.find('.comment').each(() ->
      handleAddedComment(null, $(this))
    )

  ###
    Transform a Comment object into a Comment DOM
  ###
  createComment = (comment) ->
    $newComment = $template.clone()
    $newComment.attr('id', 'com-' + comment.username)
    $newComment.attr('data-username', comment.username)
    $newComment.find("h3").text(comment.username)
    $newComment.find("div.avatar img").attr('src', '//robohash.org/' + comment.username + '?set=set3&size=60x60')
    $newComment.find("p").text(comment.comment)
    $newComment.removeClass('invisible')
    $newComment.attr('data-url', comment._links.self.href)
    return $newComment

  ###
    Display error message in case of failure.
  ###
  handleFailure = (jQXHR, command)->
    if(jQXHR.status == 401)
      $.notify(
        {message: "You can't "+command+" this comment. Invalid APIKey. Please log again."},
        type: 'danger'
      )
      user.clearInfo()
    else
      $.notify(
        {message: "A problem happen, can't "+command+" the comment"},
        type: 'danger'
      )
      console.error(jQXHR)
  ###
    Delete a comment. Send the request and remove it from the list
  ###
  deleteComment = (url, $comment) ->
  user.sendUserRequest(url, 'DELETE').success(()->
    $.notify(
      {message: 'Comment successfully deleted'},
      type: 'info'
    )
    $comment.fadeOut()
  ).fail((jQHXR) ->
    handleFailure(jQHXR, 'delete')
  )
  ###
    Edit the comment. Send the request and modify it on success
  ###
  editComment = (url, $comment) ->
    newComment = $("#editedComment").val()
    user.sendUserRequest(url, 'PUT',
      comment:
        newComment
    ).success(() ->
      $.notify(
        {message: 'Comment successfully edited'},
        type: 'info'
      )
      $comment.find('p').text(newComment)
    ).fail((jQXHR)->
      handleFailure(jQXHR, 'edit')
    )


  ###
    EVENTS
  ###
  $comments.on('comment.added', handleAddedComment)
  $(user).on('user.logout', handleUserLogout)
  $(user).on('user.login', handleUserLogin)

  ###
    BUTTONS
  ###
  $comments.on('click', 'button.delete', (event) ->
    event.preventDefault()
    $comment = $(this).parent().parent()
    url = $comment.attr('data-url')
    bootbox.confirm("Delete the comment ?", (result) ->
      if(result)
        deleteComment(url, $comment)
    )
  )

  $comments.on('click', 'button.edit', (event) ->
    event.preventDefault()
    $comment = $(this).parent().parent()
    url = $comment.attr('data-url')
    commentText = $comment.find('p').text()
    bootbox.dialog(
      title: 'Edit Comment'
      message: '<div class="row"><div class="col-lg-12"><textarea id="editedComment" style="width: 100%;">' + commentText + '</textarea></div></div>'
      buttons:
        success:
          label: '<span class="glyphicon glyphicon-edit">Edit</span>'
          className: 'btn-success'
          callback: () ->
            editComment(url, $comment)
    )
  )

  root = window ? this
  root.createComment = createComment) jQuery