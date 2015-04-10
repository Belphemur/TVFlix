"use strict"
###
  Handle the Login using Username and ApiKey
###
(($) ->
  currentUser = User.getCurrentUser()
  $loginModalButton = $("#loginButton")
  $userLoginButton = $('#userLoginButton')
  ###
    Activate tooltips on links
  ###
  $("a[data-toggle='tooltip']").tooltip()

  ###
    FUNCTION BLOCK
  ###
  setLogout = ->
    $userLoginButton.html("Logout").attr('data-logout', true)
  ###
    Retrieve the user info
  ###
  getUserInfo = ->
    username = $("#username").val()
    apikey = $("#apikey").val()
    admin = $("#adminCheck").is(":checked")

    if !username || !apikey
      $("#emptyAlert").fadeIn()
      return false
    else
      $("#emptyAlert").fadeOut();

    #Save in local storage
    currentUser.setInfo(username, apikey, admin)
    return true
  ###
    Remove data from the localstorage and logout the user
  ###
  handleLogout = ->
    currentUser.clearInfo()
  ###
    check if already logged in with LocalStorage
  ###
  if currentUser.isValid()
    $("#username").val(currentUser.name)
    $("#apikey").val(currentUser.apikey)
    if currentUser.admin
      $("#adminCheck").prop('checked', true)
    setLogout()

  ###
    BUTTON MANAGEMENT
  ###

  $loginModalButton.click (e) ->
    e.preventDefault()
    if getUserInfo()
      $("#loginModal").modal("hide")
      setLogout()

  $userLoginButton.click (e) ->
    e.preventDefault()
    if $(this).attr("data-logout")
      handleLogout()
    else
      $("#loginModal").modal("show")

  $(currentUser).on('user.logout', () ->
    $userLoginButton.html("Login").removeAttr('data-logout')
  )
) jQuery